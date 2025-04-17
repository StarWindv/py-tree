from stv_pytree.core.stv_parse import stv_parse
from stv_pytree.core.tree import tree
import argparse
import sys
import os


def main():
    args = stv_parse()
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
        return