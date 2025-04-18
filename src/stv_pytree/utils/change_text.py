from stv_utils import is_ch
from stv_pytree.utils.lang_utils import language_config


def parse_text(check = True):
    check = language_config() if check else check

    if is_ch() or check:  # 检测是否为中文，调用stv_utils库的is_ch()函数即可
        title = "Python目录树命令"
        hidden_help = "显示隐藏文件"
        only_dir_help = "仅显示目录"
        level_help = "最大显示深度"
        full_path_help = "显示完整路径"
        exclude = "排除模式"
        pattern = "包含的文件名模式"
        color = "彩色输出"
        directory_help = "起始目录"

        version_help = "输出项目版本"
        license_help = "输出项目所用许可证"

    else:
        title = "Python tree command"
        hidden_help = "Show hidden files"
        only_dir_help = "List directories only"
        level_help = "Max display depth"
        full_path_help = "Print full paths"
        exclude = "Exclusion patterns"
        pattern = "Filename pattern to include"
        color = "Color output"
        directory_help = "Starting directory"

        version_help = "Print project version"
        license_help = "Print project license"

    language_help = "设置参数语言为中文"
    clear_language_setting_help = "clear the language setting"

    array = [title, hidden_help, only_dir_help,
             level_help, full_path_help, exclude,
             pattern, color, directory_help,
             version_help, license_help, language_help,
             clear_language_setting_help]

    return array
