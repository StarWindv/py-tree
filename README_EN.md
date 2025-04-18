# 🌳 py-tree - Directory Tree Generator

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/starwindv/py-tree)

A Python implementation of `tree`-like utility with colorful output, path filtering, depth control, and multilingual support.

[中文文档](./README.md)

---

## ✨ Features

- **Color Highlighting**  
  Distinguish directories, executables, symlinks with different colors
- **Smart Filtering**  
  - `-P` wildcard pattern matching  
  - `-I` multi-pattern exclusion for files/dirs  
  - Show hidden files (`-a`) and directory-only mode (`-d`)
- **Path Display**  
  Toggle between full path (`-f`) and relative path
- **Multilingual Support**  
  Auto-display help messages in Chinese/English based on system language
- **Depth Control**  
  Limit traversal depth with `-L` parameter

---

## 📦 Installation

```bash
pip install stv_pytree
```

*Use via entry point command `pytree`*

---

## 🚀 Usage Examples

### Basic Usage

```bash
pytree [directory]
```

### Show Hidden Files

```bash
pytree -a ~/projects
```

### Limit Depth to 2

```bash
pytree -L 2 /usr
```

### Directories Only & Full Path

```bash
pytree -d -f /var/log
```

### Combined Filtering

```bash
# Show Python files starting with "test" (exclude .log files)
pytree -P "*.py" -I "*.log" -a src/
```

---

## 📌 Command-line Options

```text
usage: pytree [-h] [-a] [-d] [-L LEVEL] [-f] [-I EXCLUDE] [-P PATTERN] [--color {always,auto,never}] [directory]

Options:
  -h, --help         show help message
  -a, --all          Show hidden files
  -d, --dir-only     Show directories only
  -L LEVEL           Max traversal depth
  -f, --full-path    Display full paths
  -I EXCLUDE         Exclusion patterns (multi-use)
  -P PATTERN         Filename matching pattern
  --color            Color mode: always/auto/never (default: auto)
```

---

## 🖼️ Demo

![Example Screenshot](https://github.com/starwindv/py-tree/blob/main/example/pytree.bmp?raw=True)

---

## 🤝 Contributing

Issues and PRs are welcome!

---

## 📄 License

[MIT License](https://github.com/starwindv/py-tree/blob/main/LICENSE)
