import os
import argparse
from sys import stdout
from collections import deque

try:
    from colorama import Fore, init
except ImportError:
    class Fore:
        RESET = BLUE = GREEN = RED = YELLOW = MAGENTA = CYAN = WHITE = ''
    init = lambda: None

class TreeGenerator:
    def __init__(self,
                 show_hidden=False,
                 dir_only=False,
                 level=-1,
                 exclude_dirs=None,
                 exclude_files=None,
                 output_file=None):
        
        self.show_hidden = show_hidden
        self.dir_only = dir_only
        self.level = level
        self.exclude_dirs = set(exclude_dirs or [])
        self.exclude_files = set(exclude_files or [])
        self.output_file = output_file
        self.indent_prefix = '│   '
        self.indent_connector = '├── '
        self.indent_last = '└── '
        self.output_handle = None

    def _should_skip(self, name, is_dir):
        if name.startswith('.') and not self.show_hidden:
            return True
        if is_dir and name in self.exclude_dirs:
            return True
        if not is_dir and name in self.exclude_files:
            return True
        return False

    def _get_color(self, is_dir, is_executable=False):
        if is_dir:
            return Fore.BLUE
        if is_executable:
            return Fore.GREEN
        return Fore.RESET

    def _walk(self, root, current_level=0):
        if self.level != -1 and current_level > self.level:
            return

        try:
            entries = sorted(os.listdir(root))
        except PermissionError:
            self.output_handle.write(f"{Fore.RED}[Permission denied] {root}{Fore.RESET}\n")
            return
        except FileNotFoundError:
            return

        dirs, files = [], []
        for entry in entries:
            full_path = os.path.join(root, entry)
            is_dir = os.path.isdir(full_path)
            if self._should_skip(entry, is_dir):
                continue
            if is_dir:
                dirs.append(entry)
            else:
                if not self.dir_only:
                    files.append(entry)

        entries = dirs + files
        total = len(entries)
        for index, entry in enumerate(entries):
            is_last = index == total - 1
            full_path = os.path.join(root, entry)
            is_dir = os.path.isdir(full_path)

            yield entry, full_path, is_dir, is_last, current_level

    def generate(self, root_dir='.'):
        if self.output_file:
            self.output_handle = open(self.output_file, 'w')
        else:
            self.output_handle = stdout

        init()  # Initialize colorama
        queue = deque([(root_dir, 0, [])])
        while queue:
            current_dir, current_level, parent_prefix = queue.popleft()
            

            if current_dir == root_dir:
                self.output_handle.write(f".\n")
            else:

                self.output_handle.write(''.join(parent_prefix))
                dir_name = os.path.basename(current_dir)
                color = self._get_color(True)
                self.output_handle.write(f"{color}{dir_name}{Fore.RESET}\n")

            entries = list(self._walk(current_dir, current_level))
            if not entries:
                continue

            for index, (entry, full_path, is_dir, is_last, level) in enumerate(entries):

                if is_last:
                    prefix = self.indent_last
                    next_indent = '    '
                else:
                    prefix = self.indent_connector
                    next_indent = self.indent_prefix

                current_indent = ''.join(parent_prefix)
                line = current_indent + prefix
                
                color = self._get_color(is_dir)
                self.output_handle.write(f"{line}{color}{entry}{Fore.RESET}\n")

                if is_dir:
                    new_prefix = parent_prefix.copy()
                    new_prefix.append(next_indent)
                    queue.append((full_path, level + 1, new_prefix))

        if self.output_file:
            self.output_handle.close()

def main():
    parser = argparse.ArgumentParser(description='Python implementation of tree command')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to tree')
    parser.add_argument('-a', '--all', action='store_true', help='Include hidden files')
    parser.add_argument('-d', '--dirs-only', action='store_true', help='List directories only')
    parser.add_argument('-L', '--level', type=int, default=-1, help='Descend only level directories deep')
    parser.add_argument('--exclude-dir', action='append', help='Exclude directories matching pattern')
    parser.add_argument('--exclude-file', action='append', help='Exclude files matching pattern')
    parser.add_argument('-o', '--output', help='Output to file instead of stdout')
    args = parser.parse_args()

    generator = TreeGenerator(
        show_hidden=args.all,
        dir_only=args.dirs_only,
        level=args.level,
        exclude_dirs=args.exclude_dir,
        exclude_files=args.exclude_file,
        output_file=args.output
    )
    generator.generate(args.directory)

if __name__ == '__main__':
    main()
