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
                btn.config(command=lambda: worker(item["script"]))
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


def generic_event_check(event):
    while ui_queue.qsize() > 0:
        qitem = ui_queue.get()
        if qitem.out is None:
            print(f"done: {qitem.exit_code}")
            enable_all_buttons()
        else:
            print(qitem.out, end='')
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
ui_root = tk.Tk()
ui_root.geometry("720x480")
ui_root.bind("<<generic_interrupt>>", generic_event_check)
ui_root.attributes('-topmost', True)
ui_frame = ttk.Frame(ui_root, padding=10)
ui_frame.grid()

ui_queue = Queue()


if __name__ == "__main__":
    load_ui()    
    ui_root.mainloop()
