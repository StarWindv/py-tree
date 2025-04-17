import os
from stv_pytree.utils.colors import COLORS, get_color
from stv_pytree.utils.utils import should_ignore
from fnmatch import fnmatch


def tree(start_path, config, prefix='', depth=0):
    lines = []
    try:
        entries = os.listdir(start_path)
    except PermissionError:
        lines.append(f"{prefix}[Permission denied]")
        return lines
    except OSError as e:
        lines.append(f"{prefix}[Error: {str(e)}]")
        return lines

    # 过滤和排序处理
    entries = [e for e in entries if config.all or not e.startswith('.')]
    entries = [e for e in entries if not should_ignore(e, config.exclude)]
    if config.pattern:
        entries = [e for e in entries if fnmatch(e, config.pattern)]
    if config.dir_only:
        entries = [e for e in entries if os.path.isdir(os.path.join(start_path, e))]
    entries.sort(key=lambda x: x.lower() if config.ignore_case else x)

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
        lines.append(f"{prefix}{connector}{color}{display_name}{end_color}")

        if os.path.isdir(full_path) and not os.path.islink(full_path):
            if config.level is None or depth < config.level:
                new_prefix = prefix + ('    ' if is_last else '│   ')
                lines.extend(
                    tree(full_path, config, new_prefix, depth+1)
                )

    return lines