from stv_utils import is_ch

def parse_text():
    if is_ch():  # 检测是否为中文，调用stv_utils库的is_ch()函数即可
        title = "Python目录树命令"
        hidden_help = "显示隐藏文件"
        only_dir_help = "仅显示目录"
        level_help = "最大显示深度"
        full_path_help = "显示完整路径"
        exclude = "排除模式"
        pattern = "包含的文件名模式"
        color = "彩色输出"
        directory_help = "起始目录"

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

    array = [title, hidden_help, only_dir_help,
             level_help, full_path_help, exclude,
             pattern, color, directory_help]

    return array