import os
from stv_utils import system_check

def get_config_path(show_info = False):
    if system_check():
        config_path = os.path.join(os.environ['LOCALAPPDATA'], "stv_language.config")
    else:
        config_path = os.path.join(os.environ['HOME'], "stv_language.config")
    if show_info: print(f'config path is {config_path}')
    return config_path


def language_config(show_info = False):

    config_path = get_config_path()

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "chinese" in content or "zh-cn" in content:
            if show_info: print(f"config content is {content}")
            return True
    return False


def set_cn(code, show_info = False):
    available_path = ["zh-cn", "chinese"]
    config_path = get_config_path()
    if code.lower() in available_path:
        with open(config_path, 'w', encoding="utf-8") as f:
            f.write(code)
        if show_info: print("\033[96m已将语言设置为中文\033[0m")
    elif "rm" in code.lower():
        with open(config_path, 'w', encoding="utf-8") as f:
            f.write("")
        if show_info: print("\033[96m已清除语言设置\033[0m")
    else:
        print("\033[31mUn Available Language Code!\033[0m")
        print(available_path, end='\n\n')
