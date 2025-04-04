import threading
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import filedialog
import os
import datetime
import tkinter as tk
import subprocess
import pystray
from PIL import Image

# 创建主窗口
root = tk.Tk()
root.title("定时提醒工具")
# 设置窗口图标
try:
    root.iconphoto(True, tk.PhotoImage(file="resources/eye-protect.png"))
except:
    pass

# 修改minimize_to_tray函数，使其成为全局变量
icon = None

# 最小化到系统托盘的函数
def minimize_to_tray():
    global icon
    root.withdraw()
    image = Image.open("resources/eye-protect.png")
    menu = (pystray.MenuItem('显示窗口', lambda: [root.deiconify(), rebuild_menu(), icon.stop()]),
            pystray.MenuItem('退出', lambda: [root.destroy(), icon.stop()]))
    icon = pystray.Icon("name", image, "定时提醒工具", menu)
    icon.run()

def rebuild_menu():
    # 重建菜单栏
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # 创建统计菜单
    statistics_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="功能区", menu=statistics_menu)
    
    # 添加统计功能入口
    statistics_menu.add_command(label="统计报表", command=show_statistics_report)
    statistics_menu.add_command(label="查看定时任务列表", command=show_reminder_tasks)
    # statistics_menu.add_command(label="放置到系统托盘", command=minimize_to_tray)

# 创建输入框和标签
label_task_type = tk.Label(root, text="定时任务类型:")
label_task_type.pack()

# 定义定时任务类型选项
TASK_TYPES = ["普通定时任务", "定制定时任务 - 护眼任务", "定时喝水任务"]
var_task_type = tk.StringVar(root)
var_task_type.set(TASK_TYPES[0])

# 创建下拉框
option_menu_task_type = tk.OptionMenu(root, var_task_type, *TASK_TYPES)
option_menu_task_type.pack()

label_duration = tk.Label(root, text="提醒间隔 (分钟):")
label_duration.pack()
entry_duration = tk.Entry(root)
entry_duration.pack()

label_message = tk.Label(root, text="提醒信息:")
label_message.pack()
entry_message = tk.Entry(root)
entry_message.pack()

# 创建启动按钮# 修改start_reminder函数，记录定时任务信息
# 修改start_reminder函数，根据选择的任务类型设置默认时间和图标
def start_reminder():
    try:
        task_type = var_task_type.get()
        duration_str = entry_duration.get()
        if not duration_str:
            messagebox.showerror("错误", "请输入提醒间隔时间")
            return
        duration = int(duration_str) * 60
        message = entry_message.get()
        # 显示toast提示
        # root = tk.Tk()  注释掉这行，避免创建新的主窗口
        # root.withdraw()  注释掉这行
        if task_type == "定制定时任务 - 护眼任务":
            messagebox.showinfo("提示", "护眼任务创建成功！")
            # 设置默认值
            entry_duration.delete(0, tk.END)
            entry_duration.insert(0, "2")
            entry_message.delete(0, tk.END)
            entry_message.insert(0, "开始护眼")
            
            # 加载图片
            img = PhotoImage(file="resources/eye-protect.png")
            # 创建一个新的顶层窗口
            top = tk.Toplevel()
            top.title("提示")
            # 设置窗口始终处于最前台
            top.attributes('-topmost', True)
            # 获取屏幕宽度和高度
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            
            # 获取图片宽度和高度
            img_width = img.width()
            img_height = img.height()
            
            # 计算图片居中的位置
            x = (screen_width - img_width) // 2
            y = (screen_height - img_height) // 2
            
            # 设置窗口位置
            top.geometry(f"{img_width}x{img_height}+{x}+{y}")
            
            # 初始时隐藏窗口
            top.withdraw()
            
            # 定义取消隐藏窗口的函数
            def unhide_window(event):
                top.deiconify()
            
            # 绑定空格键事件
            top.bind("<space>", unhide_window)
            # 显示图片
            label_img = tk.Label(top, image=img)
            label_img.image = img
            label_img.pack()
        elif task_type == "定时喝水任务":
            duration = 60 * 60  # 默认1小时
            entry_duration.delete(0, tk.END)
            entry_duration.insert(0, "60")
            message = "该喝水啦！"
            messagebox.showinfo("提示", "提醒已启动！喝水提醒每隔1小时触发一次。")
            # 加载图片
            img = PhotoImage(file="resources/eye-protect.png")
            # 创建一个新的顶层窗口
            top = tk.Toplevel()
            top.title("提示")
            # 设置窗口始终处于最前台
            top.attributes('-topmost', True)
            # 获取屏幕宽度和高度
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            
            # 获取图片宽度和高度
            img_width = img.width()
            img_height = img.height()
            
            # 计算图片居中的位置
            x = (screen_width - img_width) // 2
            y = (screen_height - img_height) // 2
            
            # 设置窗口位置
            top.geometry(f"{img_width}x{img_height}+{x}+{y}")
            
            # 初始时隐藏窗口
            top.withdraw()
            
            # 定义取消隐藏窗口的函数
            def unhide_window(event):
                top.deiconify()
            
            # 绑定空格键事件
            top.bind("<space>", unhide_window)
            # 显示图片
            label_img = tk.Label(top, image=img)
            label_img.image = img
            label_img.pack()
        else:
            messagebox.showinfo("提示", "普通定时任务创建成功！")
            # 加载图片
            img = PhotoImage(file="resources/eye-protect.png")
            # 创建一个新的顶层窗口
            top = tk.Toplevel()
            top.title("提示")
            # 设置窗口始终处于最前台
            top.attributes('-topmost', True)
            # 获取屏幕宽度和高度
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            
            # 获取图片宽度和高度
            img_width = img.width()
            img_height = img.height()
            
            # 计算图片居中的位置
            x = (screen_width - img_width) // 2
            y = (screen_height - img_height) // 2
            
            # 设置窗口位置
            top.geometry(f"{img_width}x{img_height}+{x}+{y}")
            
            # 初始时隐藏窗口
            top.withdraw()
            
            # 定义取消隐藏窗口的函数
            def unhide_window(event):
                top.deiconify()
            
            # 绑定空格键事件
            top.bind("<space>", unhide_window)
            # 显示图片
            label_img = tk.Label(top, image=img)
            label_img.image = img
            label_img.pack()
        # root.destroy()  注释掉这行
        # 清空输入框内容
        entry_duration.delete(0, tk.END)
        entry_message.delete(0, tk.END)
        global start_time
        start_time = datetime.datetime.now()
        t = threading.Thread(target=remind_after_time, args=(duration, message))
        t.start()
        # 将新的定时任务添加到列表中
        reminder_threads.append(t)
        # 记录定时任务信息
        reminder_tasks.append({"task_type": task_type, "duration": duration_str, "message": message, "start_time": start_time})
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 创建一个列表来存储多个定时任务
reminder_threads = []
# 用于存储定时任务信息的列表
reminder_tasks = []
start_time = None
# 定义记录文件的目录
statistics_dir = 'statistics'
def remind_after_time(duration, message):
    try:
        time.sleep(duration)
        # 记录定时任务执行情况
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        log_file = os.path.join(statistics_dir, f'{date_str}.log')
        with open(log_file, 'a') as f:
            f.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")}: {message}\n')
        
        # 在主线程中执行GUI操作
        def show_reminder():
            try:
                # 检查窗口是否被隐藏（在系统托盘中）
                if not root.winfo_viewable():
                    root.deiconify()
                
                # 根据任务类型显示相应内容
                current_task_type = var_task_type.get()
                if current_task_type == "定制定时任务 - 护眼任务":
                    # 创建全屏遮罩窗口
                    mask = tk.Toplevel()
                    mask.attributes('-fullscreen', True)
                    mask.attributes('-topmost', True)
                    
                    # 根据遮罩类型设置不同效果
                    if mask_type.get() == "color":
                        mask.configure(bg=mask_color.get() if mask_color.get() else default_mask_color)
                    else:
                        try:
                            img_path = mask_image_path.get() if mask_image_path.get() else "resources/eye-protect.png"
                            if not os.path.exists(img_path):
                                raise FileNotFoundError(f"图片文件不存在: {img_path}")
                            img = PhotoImage(file=img_path)
                            label = tk.Label(mask, image=img)
                            label.image = img
                            label.pack(fill="both", expand=True)
                        except Exception as e:
                            print(f"加载遮罩图片出错: {e}")
                            mask.configure(bg=default_mask_color)
                            # 确保窗口仍然可见
                            mask.deiconify()
                    
                    # 添加提示文字
                    label = tk.Label(mask, text="该休息眼睛了！", font=('Arial', 48), bg='#C7EDCC')
                    label.place(relx=0.5, rely=0.5, anchor='center')
                    
                    # 设置点击或按任意键关闭
                    mask.bind('<Button-1>', lambda e: mask.destroy())
                    mask.bind('<Key>', lambda e: mask.destroy())
                    mask.focus_set()
                elif current_task_type == "定时喝水任务":
                    try:
                        img = PhotoImage(file="resources/eye-protect.png")
                        label_img = tk.Label(top, image=img)
                        label_img.image = img
                        label_img.pack()
                    except Exception as e:
                        print(f"加载图片时出错: {e}")
            except Exception as e:
                print(f"显示提醒时出错: {e}")
        
        # 确保GUI操作在主线程执行
        if root.winfo_exists():
            try:
                root.after(0, show_reminder)
            except RuntimeError as e:
                if "main thread is not in main loop" in str(e):
                    # 如果主线程不在主循环中（如在系统托盘模式下），则重建窗口
                    root.deiconify()
                    root.after(0, show_reminder)
                else:
                    raise
    except Exception as e:
        print(f"定时任务执行出错: {e}")

button_start = tk.Button(root, text="启动提醒", command=start_reminder)
button_start.pack()

# 创建菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)

# 创建统计菜单
statistics_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="统计", menu=statistics_menu)

# 创建遮罩设置菜单
mask_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="遮罩设置", menu=mask_menu)

# 添加全局变量记录遮罩类型
mask_type = tk.StringVar(root)
mask_type.set("color")  # 默认使用颜色遮罩

# 添加遮罩颜色变量
default_mask_color = "#C7EDCC"
mask_color = tk.StringVar(root)
mask_color.set(default_mask_color)

# 添加遮罩图片路径变量
mask_image_path = tk.StringVar(root)
mask_image_path.set("resources/eye-protect.png")

# 定义统计功能函数
def show_statistics_report():
    try:
        # 调用 statistics_report.py 脚本
        subprocess.run(['python3', 'statistics_report.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"统计报表生成失败: {e}")

# 定义查看定时任务列表的函数
def show_reminder_tasks():
    task_list = []
    # 创建一个新列表来存储未完成的任务
    active_tasks = []
    for task in reminder_tasks:
        elapsed_time = (datetime.datetime.now() - task['start_time']).total_seconds()
        remaining_time = int(int(task['duration']) * 60 - elapsed_time)
        if remaining_time > 0:
            task_info = f"任务类型: {task['task_type']}, 提醒间隔: {task['duration']} 分钟, 提醒信息: {task['message']}, 剩余时间: {remaining_time} 秒"
            task_list.append(task_info)
            active_tasks.append(task)
    # 更新reminder_tasks列表，只保留未完成的任务
    reminder_tasks[:] = active_tasks
    if not task_list:
        task_list = ["暂无定时任务。"]
    task_list_str = "\n\n".join(task_list)
    messagebox.showinfo("定时任务列表", task_list_str)
# 添加统计功能入口
statistics_menu.add_command(label="统计报表", command=show_statistics_report)
# 添加查看定时任务列表的功能选项
statistics_menu.add_command(label="查看定时任务列表", command=show_reminder_tasks)
# 添加放置到系统托盘的功能选项
statistics_menu.add_command(label="放置到系统托盘", command=minimize_to_tray)

# 添加遮罩设置功能
mask_menu.add_radiobutton(label="颜色遮罩", variable=mask_type, value="color", command=lambda: [wallpapers_menu.entryconfig(0, state='disabled')])
# 定义更新遮罩图片的函数
def update_mask_image():
    try:
        img_path = mask_image_path.get()
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"图片文件不存在: {img_path}")
        
        # 验证图片格式
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        if not img_path.lower().endswith(valid_extensions):
            raise ValueError(f"不支持的图片格式: {img_path}")
            
        img = PhotoImage(file=img_path)
        # 这里可以添加更新遮罩图片的逻辑
    except FileNotFoundError as e:
        print(f"更新遮罩图片出错: {e}")
        messagebox.showerror("错误", f"图片文件不存在: {img_path}")
    except ValueError as e:
        print(f"更新遮罩图片出错: {e}")
        messagebox.showerror("错误", f"不支持的图片格式: {img_path}")
    except Exception as e:
        print(f"更新遮罩图片出错: {e}")
        messagebox.showerror("错误", f"加载图片时出错: {e}")

# 添加wallpapers目录图片选项
wallpapers_menu = tk.Menu(mask_menu, tearoff=0)
mask_menu.add_cascade(label="壁纸选择", menu=wallpapers_menu)

# 遍历resources/wallpapers目录并添加图片选项
wallpapers_dir = os.path.join('resources', 'wallpapers')
if os.path.exists(wallpapers_dir):
    for img_file in os.listdir(wallpapers_dir):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(wallpapers_dir, img_file)
            wallpapers_menu.add_command(label=img_file, command=lambda p=img_path: [mask_image_path.set(p), update_mask_image()])
# 确保菜单栏功能完整
root.config(menu=menubar)

# 运行主循环
root.mainloop()

