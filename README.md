# 🌳 py-tree - 目录树生成工具

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/starwindv/py-tree)

一个Python实现的类`tree`命令工具，支持彩色输出、路径过滤、深度控制等功能，适配中英文环境。

---

## ✨ 功能特性

- **彩色高亮**  
  区分目录、可执行文件、符号链接等类型（支持自动检测终端颜色）
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
pip install py-tree
```

*通过入口点命令 `ptree` 直接调用*

---

## 🚀 使用示例

### 基础用法

```bash
ptree [目录]
```

### 显示隐藏文件（包括.开头文件）

```bash
ptree -a ~/projects
```

### 限制遍历深度为2

```bash
ptree -L 2 /usr
```

### 仅显示目录 & 完整路径

```bash
ptree -d -f /var/log
```

### 组合过滤

```bash
# 显示所有test开头的Python文件（排除.log结尾文件）
ptree -P "*.py" -I "*.log" -a src/
```

---

## 📌 命令行选项

```text
usage: ptree [-h] [-a] [-d] [-L LEVEL] [-f] [-I EXCLUDE] [-P PATTERN] [--color {always,auto,never}] [directory]

选项说明：
  -a, --all         显示隐藏文件
  -d, --dir-only    仅显示目录
  -L LEVEL          最大遍历深度
  -f, --full-path   显示完整路径
  -I EXCLUDE        排除模式（可多次使用）
  -P PATTERN        文件名匹配模式
  --color           颜色模式：always/auto/never（默认auto）
```

---

## 🖼️ 效果演示

![示例截图](https://via.placeholder.com/600x300.png/CCCCCC?text=Colorized+Output+Example)  
*（截图区域建议补充实际效果图）*

---

## 🤝 贡献指南

欢迎通过Issue报告问题或提交Pull Request！  
开发环境建议使用Python 3.8+，遵循PEP8代码规范。

---

## 📄 许可证

[MIT License](https://github.com/starwindv/py-tree/blob/main/LICENSE)