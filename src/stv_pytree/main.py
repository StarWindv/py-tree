from stv_pytree.core.stv_parse import stv_parse
from stv_pytree.core.tree import tree
import argparse
import sys
import os

__version__ = "0.0.6"


def main(__version__ = __version__):
    args = stv_parse()

    if args.version:
        print(__version__)
        return

    if args.license:
        try:
            from stv_pytree.utils.lic import return_mit
            print(f"\033[33m{return_mit()}\033[0m")
        except ImportError:
            print("\033[96mThis Project Follow MIT License\033[0m")
        return

    if args.set_Chinese:
        from stv_pytree.utils.lang_utils import set_cn
        set_cn("zh-cn")
        return

    if args.clear_language_setting:
        from stv_pytree.utils.lang_utils import set_cn
        set_cn("rm")
        return

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

    if args.no_stream:
        try:
            """
            # print the whole tree at once
            # when using this mode,
            # function tree's arg named "stream" must be False
            """

            result = [config.root_name]
            result.extend(tree(config.base_path, config, stream=False, follow_symlinks=args.follow_symlinks))
            print(result[0])
            for i in result[1:]:
                print("\n".join(i))
                """
                # print(f'\033[31mDEBUG Type:{type(i)}\033[0m')
                """

        except TypeError:
            """
            # print(f"\033[31mTypeError:Type of {i} is {type(i)}\n\033[0m")
            # This error occurs because the counters for the directory and file returned integers.
            # But we don't need to worry about it.
            """

        except KeyboardInterrupt:
            return

    else:
        try:
            """
            # streaming output 
            # when using this mode, 
            # function tree's arg named "stream" must be True
            """

            print(config.root_name)
            tree(config.base_path, config, stream=True, follow_symlinks=args.follow_symlinks)
        except KeyboardInterrupt:
            return
    """
    # 如你所见，文件夹计数器并不会包括目录"."。
    """
    print(f"\033[90mThe folder counter does not include the current directory(root).\033[0m")
    """
    # print()
    果然最后还是没有换行好看一些嘛...
    """
