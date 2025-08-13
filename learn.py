import tkinter as tk

def button_click(btn_text):
    text_box.insert(tk.END, f"Button {btn_text} clicked!\n")

# 创建主窗口
root = tk.Tk()
root.title("3x3 Button Grid")
root.geometry("500x400")

# 创建文本框
text_box = tk.Text(root, height=10, width=60)
text_box.pack(pady=10)

# 创建按钮框架（3x3网格）
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 生成3x3按钮
for row in range(3):
    for col in range(3):
        btn_text = f"{row+1}-{col+1}"  # 按钮标签（如1-1, 1-2,...）
        button = tk.Button(
            button_frame, 
            text=btn_text, 
            command=lambda t=btn_text: button_click(t),
            width=8, height=2
        )
        button.grid(row=row, column=col, padx=5, pady=5)

# 运行主循环
root.mainloop()