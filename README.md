# 📂 FileSorter 文件整理助手

一个简单好用的桌面文件整理工具，一键按类型归类，支持批量重命名。

## ✨ 功能

- **一键整理** — 按文件类型（图片/Word/Excel/PPT/PDF/文本/视频/音乐/压缩包/程序）自动归类到不同文件夹
- **自定义分类名** — 整理前可以修改每个分类的文件夹名称
- **批量重命名** — 整理完成后自动询问是否重命名，支持自定义前缀 + 日期 + 序号
- **选择文件夹** — 整理后可以勾选要对哪些分类文件夹进行重命名
- **无需配置** — 双击即用，不需要安装 Python 或任何环境

## 📥 下载

- [点此下载 FileSorter.exe（最新版）](https://github.com/AWEI/FileSorter/releases/latest)

## 🖥️ 使用方法

1. 双击 `FileSorter.exe` 打开程序
2. 点击「选择文件夹」选中要整理的目录
3. （可选）点击「自定义分类名称」修改文件夹名字
4. 点击「开始整理」
5. 整理完自动弹窗询问是否重命名

## 📋 支持的文件类型

| 分类 | 格式 |
|------|------|
| 📷 图片 | jpg, jpeg, png, gif, bmp, webp, svg, ico, tiff |
| 📝 Word | doc, docx |
| 📊 Excel | xls, xlsx, csv |
| 📽️ PPT | ppt, pptx |
| 📄 PDF | pdf |
| 📄 文本 | txt, md |
| 🎬 视频 | mp4, avi, mkv, mov, wmv, flv, webm |
| 🎵 音乐 | mp3, wav, flac, aac, ogg, wma |
| 📦 压缩包 | zip, rar, 7z, tar, gz |
| 💻 程序 | exe, msi, apk |

> 不支持的格式不会移动，保持原位。

## 🛠️ 开发

基于 Python + ttkbootstrap 开发。

```bash
pip install ttkbootstrap pillow pyinstaller
pyinstaller --onefile --windowed --name "FileSorter" file_sorter.py
```

## 📄 许可证

MIT
