import os
from stv_pytree.utils.colors import COLORS, get_color
from stv_pytree.utils.utils import should_ignore
from fnmatch import fnmatch


def tree(start_path, config, prefix='', depth=0, visited=None, stream=True, follow_symlinks=True):
    """
    generate a tree structure of the directory starting from start_path

    :param start_path: 起始路径
    :param config: 配置对象
    :param prefix: 前缀字符串，用于生成树形结构
    :param depth: 当前递归深度
    :param visited: 用于检测循环链接的已访问路径集合
    :param stream: 流式输出模式（直接打印）
    :param follow_symlinks: 是否跟随符号链接进入目录
    :return: None if stream else list
    """
    if follow_symlinks:
        if visited is None:
            visited = set()
        real_path = os.path.realpath(start_path)
        if real_path in visited:
            line = f"{prefix}[循环链接跳过: {os.path.basename(start_path)}]"
            if stream:
                print(line)
                return
            else:
                return [line]
        visited.add(real_path)
    else:
        visited = None

    try:
        entries = os.listdir(start_path)
    except PermissionError:
        line = f"{prefix}[Permission denied]"
        if stream:
            print(line)
            return [] if not stream else None
        else:
            return [line]
    except OSError as e:
        line = f"{prefix}[Error: {str(e)}]"
        if stream:
            print(line)
            return [] if not stream else None
        else:
            return [line]

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

        if os.path.islink(full_path):
            try:
                link_target = os.readlink(full_path)
                display_name += f' -> {link_target}'
            except OSError:
                display_name += ' -> [broken link]'

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

        is_dir = os.path.isdir(full_path)
        is_link = os.path.islink(full_path)

        if is_dir:
            if follow_symlinks or not is_link:
                if config.level is None or depth < config.level:
                    new_prefix = prefix + ('    ' if is_last else '│   ')
                    new_visited = visited.copy() if follow_symlinks else None
                    if stream:
                        tree(full_path, config, new_prefix, depth + 1, new_visited, stream=True, follow_symlinks=follow_symlinks)
                    else:
                        sub_lines = tree(full_path, config, new_prefix, depth + 1, new_visited, stream=False, follow_symlinks=follow_symlinks)
                        lines.extend(sub_lines)

    return lines if not stream else None
