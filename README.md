FileSorter 文件整理助手

一个桌面文件整理工具，一键按类型归类，支持批量重命名。

功能

- 一键整理：按文件类型自动归类到不同文件夹
- 支持格式：图片、Word、Excel、PPT、PDF、文本、视频、音乐、压缩包、程序
- 自定义分类名：整理前可以修改文件夹名称
- 批量重命名：整理完成后可继续重命名文件
- 选择文件夹：整理后勾选要重命名的分类文件夹
- 不支持的格式不移动，保持原位

使用方法

1. 双击 FileSorter.exe 打开程序
2. 点击选择文件夹，选中要整理的目录
3. 点击自定义分类名称，修改文件夹名字（可选）
4. 点击开始整理
5. 整理完成后弹窗询问是否继续重命名

开发环境

Python 3.12 + ttkbootstrap

安装依赖：
pip install ttkbootstrap pillow pyinstaller

打包命令：
pyinstaller --onefile --windowed --name "FileSorter" file_sorter.py

许可证

MIT
