import tkinter as tk
from tkinter import ttk

def generate_with(parent, d):
    item = ttk.Button(parent)
    if type(d) != dict:
        print("非法对象类型")

    col = 0
    row = 0
    text = "Button"

    for k in d:
        v = d[k]
        print(k, v)
        if k == "text":
            text = v
        if k == "column":
            col = int(v)
        if k == "row":
            row = int(v)
            
    item.grid(column=col, row=row)
    item.config(text=text)
    return item
