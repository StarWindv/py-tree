import os
import sys
import argparse
from fnmatch import fnmatch
from stat import S_ISDIR, S_IXUSR


COLORS = {
    'reset': '\033[0m',
    'dir': '\033[94m',
    'exec': '\033[92m',
    'link': '\033[96m',
    'special': '\033[95m',
}

def should_ignore(name, patterns):
    return any(fnmatch(name, p) for p in patterns)

def get_color(path, name):
    if os.path.islink(path):
        return COLORS['link']
    if os.path.isdir(path):
        return COLORS['dir']
    if os.access(path, os.X_OK):
        return COLORS['exec']
    if os.path.ismount(path) or os.stat(path).st_mode & 0o7000:
        return COLORS['special']
    return ''

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

def main():
    parser = argparse.ArgumentParser(description='Python tree command')
    parser.add_argument('-a', '--all', action='store_true', help='Show hidden files')
    parser.add_argument('-d', '--dir-only', action='store_true', help='List directories only')
    parser.add_argument('-L', '--level', type=int, help='Max display depth')
    parser.add_argument('-f', '--full-path', action='store_true', help='Print full paths')
    parser.add_argument('-I', '--exclude', action='append', default=[], help='Exclusion patterns')
    parser.add_argument('-P', '--pattern', help='Filename pattern to include')
    parser.add_argument('--color', choices=['always', 'auto', 'never'], default='auto', help='Color output')
    parser.add_argument('directory', nargs='?', default='.', help='Starting directory')
    
    args = parser.parse_args()

    if args.color == 'auto':
        args.color = sys.stdout.isatty()
    else:
        args.color = args.color == 'always'


    config = argparse.Namespace(
        all=args.all,
        dir_only=args.dir_only,
        level=args.level,
        full_path=args.full_path,
        exclude=args.exclude,
        pattern=args.pattern,
        color=args.color,
        base_path=os.path.abspath(args.directory),
        root_name=os.path.abspath(args.directory) if args.full_path else args.directory,
        ignore_case=True
    )

    try:
        result = [config.root_name]
        result.extend(tree(config.base_path, config))
        print('\n'.join(result))
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    main()
