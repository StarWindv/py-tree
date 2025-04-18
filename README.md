# 🌳 py-tree - 目录树生成工具

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/starwindv/py-tree)

一个Python实现的类 Linux `tree`命令工具，支持彩色输出、路径过滤、深度控制等功能，适配中英文环境。

[English](./README_EN.md)

---

## ✨ 功能特性

- **彩色高亮**  
  区分目录、可执行文件、符号链接等类型
- **智能过滤**  
  - 支持 `-P` 通配符匹配包含文件  
  - 支持 `-I` 多模式排除文件/目录  
  - 支持隐藏文件显示（`-a`）和仅目录模式（`-d`）
- **路径显示**  
  可选完整路径模式（`-f`）或相对路径
- **多语言适配**  
  自动根据系统语言显示中/英文帮助信息
- **深度控制**  
  通过 `-L` 参数限制遍历层级

---

## 📦 安装

```bash
pip install stv_pytree
```

*通过入口点命令 `pytree` 直接调用*

---

## 🚀 使用示例

### 基础用法

```bash
pytree [目录]
```

### 显示隐藏文件（包括.开头文件）

```bash
pytree -a ~/projects
```

### 限制遍历深度为2

```bash
pytree -L 2 /usr
```

### 仅显示目录 & 完整路径

```bash
pytree -d -f /var/log
```

### 组合过滤

```bash
# 显示所有test开头的Python文件（排除.log结尾文件）
pytree -P "*.py" -I "*.log" -a src/
```

---

## 📌 命令行选项

```text
usage: pytree [-h] [-a] [-d] [-L LEVEL] [-f] [-I EXCLUDE] [-P PATTERN] [--color {always,auto,never}] [directory]

选项说明：
  -a, --all                     显示隐藏文件
  -d, --dir-only                仅显示目录
  -L LEVEL                      最大遍历深度
  -f, --full-path               显示完整路径
  -I EXCLUDE                    排除模式（可多次使用）
  -P PATTERN                    文件名匹配模式
  --color                       颜色模式：always/auto/never（默认auto）
  -sc, --set_Chinese            强制设置显示语言为中文
  -cl, --clear_language_setting 清除强制语言设置
```

---

## 🖼️ 效果演示

![示例截图](https://github.com/starwindv/py-tree/blob/main/example/pytree.bmp?raw=True)

---

## 🤝 贡献指南

欢迎通过Issue报告问题或提交Pull Request！  

---

## 📄 许可证

[MIT License](https://github.com/starwindv/py-tree/blob/main/LICENSE)
