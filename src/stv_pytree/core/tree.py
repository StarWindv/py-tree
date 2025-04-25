import os
from stv_pytree.utils.colors import COLORS, get_color
from stv_pytree.utils.utils import should_ignore
from fnmatch import fnmatch


def tree(start_path, config, prefix='', depth=0, visited=None, stream=True, follow_symlinks=False):
    """
    Generate a tree structure of the directory starting from start_path

    :param start_path: 起始路径
    :param config: 配置对象
    :param prefix: 前缀字符串，用于生成树形结构
    :param depth: 当前递归深度
    :param visited: 用于检测循环链接的已访问路径集合
    :param stream: 流式输出模式（直接打印）
    :param follow_symlinks: 是否跟随符号链接进入目录
    :return: None if stream else list
    """
    # 处理符号链接循环检测
    if follow_symlinks:
        if visited is None:
            visited = set()
        real_path = os.path.realpath(start_path)
        if real_path in visited:
            line = f"{prefix}[循环链接跳过: {os.path.basename(start_path)}]"
            if stream:
                print(line)
                return 0, 0
            else:
                return [line], 0, 0
        visited.add(real_path)
    else:
        visited = None

    # 初始化统计变量
    current_dirs = 0
    current_files = 0

    # 异常处理
    try:
        entries = os.listdir(start_path)
    except PermissionError:
        line = f"{prefix}[Permission denied]"
        if stream:
            print(line)
            return 0, 0
        else:
            return [line], 0, 0
    except OSError as e:
        line = f"{prefix}[Error: {str(e)}]"
        if stream:
            print(line)
            return 0, 0
        else:
            return [line], 0, 0

    # 过滤和排序
    entries = [e for e in entries if config.all or not e.startswith('.')]
    entries = [e for e in entries if not should_ignore(e, config.exclude)]
    if config.pattern:
        entries = [e for e in entries if fnmatch(e, config.pattern)]
    if config.dir_only:
        entries = [e for e in entries if os.path.isdir(os.path.join(start_path, e))]
    entries.sort(key=lambda x: x.lower() if config.ignore_case else x)

    lines = [] if not stream else None

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        full_path = os.path.join(start_path, entry)
        display_name = os.path.join(config.root_name, full_path[len(config.base_path)+1:]) if config.full_path else entry

        # 判断是否为符号链接并统计
        is_link = os.path.islink(full_path)
        if is_link:
            current_files += 1
        else:
            if os.path.isdir(full_path):
                current_dirs += 1
            else:
                current_files += 1

        # 处理符号链接显示
        if os.path.islink(full_path):
            try:
                link_target = os.readlink(full_path)
                display_name += f' -> {link_target}'
            except OSError:
                display_name += ' -> [broken link]'

        # 颜色处理
        color = ''
        end_color = ''
        if config.color:
            color = get_color(full_path, entry)
            end_color = COLORS['reset']

        connector = '└── ' if is_last else '├── '
        line = f"{prefix}{connector}{color}{display_name}{end_color}"

        if stream:
            print(line)
        else:
            lines.append(line)

        # 递归处理子目录
        is_dir = os.path.isdir(full_path)
        if is_dir and (follow_symlinks or not os.path.islink(full_path)):
            if config.level is None or depth < config.level:
                new_prefix = prefix + ('    ' if is_last else '│   ')
                new_visited = visited.copy() if follow_symlinks else None
                if stream:
                    sub_dirs, sub_files = tree(full_path, config, new_prefix, depth + 1, new_visited, stream=True, follow_symlinks=follow_symlinks)
                    current_dirs += sub_dirs
                    current_files += sub_files
                else:
                    sub_lines, sub_dirs, sub_files = tree(full_path, config, new_prefix, depth + 1, new_visited, stream=False, follow_symlinks=follow_symlinks)
                    lines.extend(sub_lines)
                    current_dirs += sub_dirs
                    current_files += sub_files

    # 流式模式根目录添加统计行
    if stream and depth == 0:
        print(f"\n{current_dirs} directories, {current_files} files")
        return current_dirs, current_files
    elif not stream and depth == 0:
        lines.append(f"\n{current_dirs} directories, {current_files} files")
        return lines, current_dirs, current_files
    else:
        return (lines, current_dirs, current_files) if not stream else (current_dirs, current_files)
