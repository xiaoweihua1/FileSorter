#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, datetime, tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

CATEGORIES = [
    ("📷 图片", ['.jpg','.jpeg','.png','.gif','.bmp','.webp','.svg','.ico','.tiff']),
    ("📝 Word", ['.doc','.docx']),
    ("📊 Excel", ['.xls','.xlsx','.csv']),
    ("📽️ PPT", ['.ppt','.pptx']),
    ("📄 PDF", ['.pdf']),
    ("📄 文本", ['.txt','.md']),
    ("🎬 视频", ['.mp4','.avi','.mkv','.mov','.wmv','.flv','.webm']),
    ("🎵 音乐", ['.mp3','.wav','.flac','.aac','.ogg','.wma']),
    ("📦 压缩包", ['.zip','.rar','.7z','.tar','.gz']),
    ("💻 程序", ['.exe','.msi','.apk']),
]

def organize(folder, names, log):
    if not os.path.exists(folder): log("❌ 文件夹不存在"); return 0
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files: log("⚠️ 文件夹为空"); return 0
    n = 0
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        for display, _ in names:
            exts = [e for c, e in CATEGORIES if c == display][0]
            if ext not in exts: continue
            target = os.path.join(folder, display)
            os.makedirs(target, exist_ok=True)
            dst = os.path.join(target, f)
            if os.path.exists(dst):
                name, e = os.path.splitext(f)
                dst = os.path.join(target, f"{name}_副本{e}")
            shutil.move(os.path.join(folder, f), dst)
            n += 1
            log(f"  ✅ {f} → {display}")
            break
    log(f"\n📊 共整理 {n} 个文件")
    return n

def rename(folder, prefix, start, log):
    if not os.path.exists(folder): log("❌ 文件夹不存在"); return
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files: log("⚠️ 文件夹为空"); return
    ds = datetime.date.today().strftime("%Y%m%d")
    for idx, f in enumerate(sorted(files), 1):
        name, ext = os.path.splitext(f)
        nn = f"{prefix}_{ds}_{start + idx - 1 if start is not None else idx:03d}{ext}"
        src = os.path.join(folder, f)
        dst = os.path.join(folder, nn)
        if os.path.exists(dst):
            dst = os.path.join(folder, f"{os.path.splitext(nn)[0]}_{idx}{ext}")
        os.rename(src, dst)
        log(f"  ✅ {f} → {nn}")
    log(f"\n📊 共重命名 {len(files)} 个文件")

class ConfigWin:
    def __init__(self, parent, names):
        self.result = None
        self.win = tb.Toplevel(parent)
        self.win.title("设置分类名称")
        self.win.geometry("500x450")
        self.win.resizable(False, False)
        tb.Label(self.win, text="自定义每个分类的文件夹名称", font=("Microsoft YaHei", 12, "bold")).pack(pady=10)
        tb.Label(self.win, text="不改则使用默认名称", font=("Microsoft YaHei", 9), bootstyle="secondary").pack()
        f = tb.Frame(self.win); f.pack(fill=BOTH, expand=True, padx=20, pady=10)
        self.es = {}
        for d, c in names:
            r = tb.Frame(f); r.pack(fill=X, pady=3)
            tb.Label(r, text=d, width=12, anchor=W).pack(side=LEFT)
            e = tb.Entry(r, bootstyle="info"); e.insert(0, c); e.pack(side=LEFT, fill=X, expand=True)
            self.es[d] = e
        bf = tb.Frame(self.win); bf.pack(pady=15)
        tb.Button(bf, text="✅ 确定", command=self.ok, bootstyle="success", width=15, padding=5).pack(side=LEFT, padx=5)
        tb.Button(bf, text="❌ 取消", command=self.win.destroy, bootstyle="secondary", width=15, padding=5).pack(side=LEFT, padx=5)
        self.win.transient(parent); self.win.grab_set(); parent.wait_window(self.win)
    def ok(self):
        self.result = [(d, e.get().strip() or d) for d, e in self.es.items()]
        self.win.destroy()

class App:
    def __init__(self):
        self.root = tb.Window(title="文件整理助手", themename="superhero")
        self.root.geometry("820x680"); self.root.minsize(700, 600)
        self.path = tk.StringVar(value="未选择文件夹")
        self.names = [(d, d) for d, _ in CATEGORIES]
        self.ui()

    def log(self, m):
        self.tx.insert(tk.END, m + "\n"); self.tx.see(tk.END); self.root.update()

    def sel(self):
        f = filedialog.askdirectory(title="选择文件夹")
        if f: self.path.set(f); self.pl.configure(bootstyle="success"); self.log(f"📂 已选择: {f}")

    def cfgs(self):
        w = ConfigWin(self.root, self.names)
        if w.result: self.names = w.result; self.cl.configure(text=self._ct()); self.log("✅ 分类名称已更新")

    def _ct(self): return "  |  ".join([f"{d}→{c}" if d != c else d for d, c in self.names])

    def org(self):
        p = self.path.get()
        if p == "未选择文件夹": messagebox.showwarning("提示", "请先选择文件夹"); return
        self.tx.delete(1.0, tk.END); self.log("🚀 开始整理...\n")
        n = organize(p, self.names, self.log)
        self.log(f"\n✅ 整理完成！")
        self.names = [(d, d) for d, _ in CATEGORIES]; self.cl.configure(text=self._ct())
        if n > 0:
            w = self._ask()
            if w:
                pf = simpledialog.askstring("重命名", "请输入文件名前缀：", parent=self.root)
                if pf:
                    self.log(f"📁 正在重命名所选文件夹..."); self.rn(pf, w)

    def _ask(self):
        p = self.path.get()
        if not os.path.exists(p): return None
        subs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d)) and not d.startswith('.')]
        if not subs: return None
        win = tb.Toplevel(self.root); win.title("选择要重命名的文件夹")
        win.geometry("400x350"); win.resizable(False, False)
        tb.Label(win, text="选择要重命名的文件夹：", font=("Microsoft YaHei", 10, "bold")).pack(pady=10)
        f = tb.Frame(win); f.pack(fill=BOTH, expand=True, padx=20)
        vs = [(d, tb.BooleanVar(value=True)) for d in subs]
        for d, v in vs: tb.Checkbutton(f, text=d, variable=v, bootstyle="info").pack(anchor=W, pady=3)
        r = []
        def ok(): nonlocal r; r = [d for d,v in vs if v.get()]; win.destroy() if r else messagebox.showwarning("","请至少选一个")
        def sk(): r = []; win.destroy()
        bf = tb.Frame(win); bf.pack(pady=15)
        tb.Button(bf, text="✅ 确定", command=ok, bootstyle="success", width=15, padding=5).pack(side=LEFT, padx=5)
        tb.Button(bf, text="⏭ 跳过", command=sk, bootstyle="secondary", width=10, padding=5).pack(side=LEFT, padx=5)
        win.transient(self.root); win.grab_set(); self.root.wait_window(win); return r

    def rn(self, pf, folders=None):
        p = self.path.get(); sn = 1
        if folders:
            for fo in folders:
                fp = os.path.join(p, fo)
                if os.path.isdir(fp):
                    self.log(f"\n📁 {fo}"); rename(fp, pf, sn, self.log)
        else:
            rename(p, pf, sn, self.log)
        self.log("\n✅ 重命名完成！")

    def rn_btn(self):
        p = self.path.get()
        if p == "未选择文件夹": messagebox.showwarning("提示", "请先选择文件夹"); return
        pf = simpledialog.askstring("重命名", "请输入文件名前缀：", parent=self.root)
        if pf:
            self.tx.delete(1.0, tk.END); self.log("✏️ 开始重命名...\n"); self.rn(pf)

    def ui(self):
        h = tb.Frame(self.root); h.pack(fill=X, padx=20, pady=15)
        tb.Label(h, text="📂 文件整理助手", font=("Microsoft YaHei", 20, "bold")).pack(anchor=W)
        tb.Label(h, text="识别图片/Word/Excel/PPT/PDF/视频/音乐等", font=("Microsoft YaHei", 10), bootstyle="secondary").pack(anchor=W)

        pf = tb.LabelFrame(self.root, text="① 选择文件夹"); pf.pack(fill=X, padx=20, pady=5)
        pr = tb.Frame(pf); pr.pack(fill=X, padx=10, pady=10)
        self.pl = tb.Label(pr, textvariable=self.path, font=("Microsoft YaHei", 9), bootstyle="info")
        self.pl.pack(side=LEFT, fill=X, expand=True)
        tb.Button(pr, text="📁 选择文件夹", command=self.sel, bootstyle="primary-outline", width=15).pack(side=RIGHT, padx=5)

        ff = tb.Frame(self.root); ff.pack(fill=BOTH, expand=True, padx=20, pady=10)
        left = tb.LabelFrame(ff, text="🔧 ② 一键整理"); left.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        lf = tb.Frame(left); lf.pack(fill=BOTH, expand=True, padx=10, pady=10)
        tb.Label(lf, text="当前分类名称：", font=("Microsoft YaHei", 9)).pack(anchor=W)
        self.cl = tb.Label(lf, text=self._ct(), font=("Microsoft YaHei", 8), bootstyle="secondary")
        self.cl.pack(anchor=W, pady=5)
        tb.Button(lf, text="⚙️ 自定义分类名称", command=self.cfgs, bootstyle="info-outline", width=25).pack(pady=5)
        tb.Button(lf, text="🚀 开始整理", command=self.org, bootstyle="success", width=25, padding=8).pack(pady=10)

        right = tb.LabelFrame(ff, text="✏️ ③ 批量重命名"); right.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        rf = tb.Frame(right); rf.pack(fill=BOTH, expand=True, padx=10, pady=10)
        tb.Label(rf, text="整理完后自动弹窗让您选择", font=("Microsoft YaHei", 9), bootstyle="secondary").pack(anchor=W, pady=5)
        tb.Label(rf, text="也可以手动点击下方按钮：", font=("Microsoft YaHei", 9), bootstyle="secondary").pack(anchor=W)
        tb.Button(rf, text="✏️ 开始重命名", command=self.rn_btn, bootstyle="warning", width=25, padding=8).pack(pady=10)

        lf2 = tb.LabelFrame(self.root, text="📋 执行日志"); lf2.pack(fill=BOTH, expand=True, padx=20, pady=5)
        lf3 = tb.Frame(lf2); lf3.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.tx = tk.Text(lf3, height=8, font=("Consolas", 9), bg="#1a1a2e", fg="#e0e0e0", relief="flat", padx=10, pady=10)
        self.tx.pack(side=LEFT, fill=BOTH, expand=True)
        sc = tb.Scrollbar(lf3, orient=VERTICAL, command=self.tx.yview); sc.pack(side=RIGHT, fill=Y)
        self.tx.configure(yscrollcommand=sc.set)

    def run(self): self.root.mainloop()

if __name__ == "__main__":
    App().run()
