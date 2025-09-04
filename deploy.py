import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import paramiko
import threading
import os
import time
from queue import Queue

import shlex
from pathlib import PurePosixPath

import yaml
import components.y_button as my_button
import components.y_text as my_text

from components.remote_run import remote_run

ui_config = "./ui_config.yaml"
remote_host = "ubuntu@zhuli.cool"
remote_key_entry = os.path.expanduser("~/.ssh/id_rsa")

ui_root = tk.Tk()
ui_root.resizable(False, False)
# ui_root.attributes('-topmost', True)

ui_text = tk.Text(ui_root, wrap=tk.CHAR, height=45, width=250, state="disabled")
ui_text.pack(padx=10, pady=10)

ui_frame = ttk.Frame(ui_root, padding=10)
ui_frame.pack()
ui_queue = Queue()

def load_ui():

    with open(ui_config) as config_contents:
        yd = yaml.safe_load(config_contents)
        if type(yd) != list:
            raise RuntimeError("UI配置格式错误: 非列表对象")
        for item in yd:
            if type(item) != dict:
                raise RuntimeError(f"非对象类型: {item}")
                continue
            if item["type"] == "button":
                btn = my_button.generate_with(ui_frame, item)
                btn.config(command=lambda item=item: worker(item["script"]))
                all_buttons.append(btn)
            if item["type"] == "label":
                lb = my_text.generate_with(ui_frame, item)


all_buttons=[]
def disnable_all_buttons():
    for btn in all_buttons:
        btn.state(['disabled'])

def enable_all_buttons():
    for btn in all_buttons:
        btn.state(['!disabled'])

def append_text(txt):
    current_end = ui_text.index("end-1c")
    ui_text.config(state="normal")
    ui_text.insert(current_end, txt)
    ui_text.config(state="disabled")
    ui_text.see("end")

def generic_event_check(event):
    while ui_queue.qsize() > 0:
        qitem = ui_queue.get()
        if qitem.out is None:
            append_text(f"done: {qitem.exit_code}\n")
            enable_all_buttons()
        else:
            append_text(qitem.out)
    pass


def post_object(obj):
    ui_queue.put(obj)
    ui_root.event_generate("<<generic_interrupt>>", when="now")


def worker(remote_python_script = "/home/ubuntu/Tmp/hw.py", remote_host = "ubuntu@zhuli.cool", key_path=os.path.expanduser("~/.ssh/id_rsa")):
    disnable_all_buttons()
    if not remote_python_script:
        print("invalid scritp")
        return
    print(remote_python_script)
    threading.Thread(target=remote_run, args=[post_object], kwargs={"remote_python_script": remote_python_script}, daemon=True).start()
    

# ui interface
ui_root.bind("<<generic_interrupt>>", generic_event_check)


if __name__ == "__main__":
    load_ui()    
    ui_root.mainloop()
