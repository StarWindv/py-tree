import os


COLORS = {
    'reset': '\033[0m',
    'dir': '\033[94m',
    'exec': '\033[92m',
    'link': '\033[96m',
    'special': '\033[95m',
}

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