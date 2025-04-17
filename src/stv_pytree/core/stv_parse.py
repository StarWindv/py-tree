import argparse
from stv_pytree.utils.change_text import parse_text

def stv_parse():
    """
    args parse
    :return: Namespace
    """
    pt = parse_text()
    parser = argparse.ArgumentParser(description=pt[0])
    parser.add_argument('-a', '--all', action='store_true', help=pt[1])
    parser.add_argument('-d', '--dir-only', action='store_true', help=pt[2])
    parser.add_argument('-L', '--level', type=int, help=pt[3])
    parser.add_argument('-f', '--full-path', action='store_true', help=pt[4])
    parser.add_argument('-I', '--exclude', action='append', default=[], help=pt[5])
    parser.add_argument('-P', '--pattern', help=pt[6])
    parser.add_argument('--color', choices=['always', 'auto', 'never'], default='auto', help=pt[7])
    parser.add_argument('directory', nargs='?', default='.', help=pt[8])

    args = parser.parse_args()
    return args