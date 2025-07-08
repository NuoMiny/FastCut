import tkinter as tk
import ImageLoader
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os
import color


class ImageCropper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("快裁  --村里最好的裁缝")
        self.geometry("1200x700")
        self.config(bg=color.yellow[3])

        self.width = 1200
        self.height = 700

        self.source_dir = ""
        self.export_dir = ""
        self.current_image_path = ""
        self.original_image = None
        self.current_image = None
        self.cropped_image = None
        self.crop_rect = None
        self.image_files = []
        self.current_image_index = 0
        self.export_num = 0
        self.crop_ratio = 1.0
        self.crop_has_been_saved = False

        self.create_widgets()

        # 绑定事件
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<Key-space>", self.save_cropped_image)
        self.canvas.bind("<Key-a>", self.prev_image)
        self.canvas.bind("<Key-d>", self.next_image)

    def create_widgets(self):
        # 创建画布用于显示图片
        self.canvas = tk.Canvas(self, width=900, height=650, bg=color.yellow[2])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建右侧的信息和控制面板
        right_frame = tk.Frame(self, bg=color.yellow[3])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # 图片信息文本框
        self.info_text = tk.Text(right_frame, width=45, height=5, font=('Arial', 13), bg=color.yellow[2])
        self.info_text.pack(pady=10)

        # 源目录输入框
        self.source_dir_entry = tk.Entry(right_frame, width=45)
        self.source_dir_entry.pack(pady=5)
        self.source_dir_button = tk.Button(right_frame, text="选择源目录", command=self.set_source_dir)
        self.source_dir_button.pack(pady=5)

        # 输出目录输入框
        self.export_dir_entry = tk.Entry(right_frame, width=45)
        self.export_dir_entry.pack(pady=5)
        self.export_dir_button = tk.Button(right_frame, text="选择输出目录", command=self.set_export_dir)
        self.export_dir_button.pack(pady=5)

        # 裁剪比例输入框
        self.crop_ratio_entry = tk.Entry(right_frame, width=10)
        self.crop_ratio_entry.insert(0, "1.0")
        self.crop_ratio_entry.pack(pady=5)

        # 显示当前配置的文本框
        self.config_text = tk.Text(right_frame, width=45, height=5, font=('Arial', 13), bg=color.yellow[2])
        self.config_text.pack(pady=10)

        # 小画布用于显示输出图片预览
        self.preview_canvas = tk.Canvas(right_frame, width=200, height=200, bg=color.yellow[2])
        self.preview_canvas.pack(pady=10)

        # 保存成功提示
        self.save_tip_label = tk.Label(right_frame, width=30, height=1, bg=color.yellow[2], font=('Arial', 16))
        self.save_tip_label.pack(pady=10)

    def set_source_dir(self):
        """选择源目录并更新显示配置的文本框"""
        dir_path = str(self.source_dir_entry.get())
        if dir_path:
            self.source_dir = dir_path
            self.update_config_label()
            self.current_image_index = 0
            self.load_images()

    def set_export_dir(self):
        """选择输出目录并更新显示配置的文本框"""
        dir_path = str(self.export_dir_entry.get())
        if dir_path:
            self.export_dir = dir_path
            self.update_config_label()
            self.export_num = self.count_dir_image(dir_path)

    def count_dir_image(self, directory):
        count = 0
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                count += 1
        return count

    def update_config_label(self):
        """更新显示配置的文本框"""
        config_txt = f"源目录: {self.source_dir or '未设置'}\n"
        config_txt += f"输出目录: {self.export_dir or '未设置'}\n"
        config_txt += f"裁剪比例: {self.crop_ratio or '未设置'}"
        self.config_text.delete(1.0, tk.END)
        self.config_text.insert(1.0, config_txt)

    def load_images(self):
        self.image_loader = ImageLoader.ImageLoader(self.source_dir)
        self.image_files = self.image_loader.image_files
        self.load_image(self.current_image_index)

    def load_image(self, index):
        self.original_image = self.image_loader.get_image(index)

        # 获取图片原始大小
        original_width, original_height = self.original_image.size

        # 获取画布大小
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 计算放大比例，保持图片的比例不变
        # 假设我们想要图片的长边触及画布边缘
        scale_width = canvas_width / original_width
        scale_height = canvas_height / original_height
        scale = min(scale_width, scale_height)

        # 计算放大后的图片大小
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        self.image = self.original_image.resize((new_width, new_height))

        # 计算图片在画布上的位置，使得至少一边触及边缘
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        self.photo_x, self.photo_y = x, y

        # 在画布上绘制图片
        self.current_photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(x, y, image=self.current_photo, anchor=tk.NW)

        # 更新画布上的裁剪框（C:\Users\admin\Desktop\杂物\壁纸如果有的话）
        # ...

        # 更新当前图片路径
        self.current_image_path = self.image_files[index]

        # 刷新画布
        self.canvas.update()

        self.update_image_info()

    def update_image_info(self):
        info_txt = f"图片名称: {self.image_files[self.current_image_index] or '未设置'}\n"
        info_txt += f"图片序号: {self.current_image_index + 1}\n"
        info_txt += f"图片大小: {self.image.size}"
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_txt)

    # 开始裁剪，记录起始点
    # 省略代码...
    def start_crop(self, event):
        # 记录鼠标按下时的位置
        self.canvas.focus_set()
        self.start_x = event.x
        self.start_y = event.y
        self.cropping = True
        self.canvas.bind("<B1-Motion>", self.do_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

    def do_crop(self, event):
        # 用户正在拖拽鼠标选择截图区域
        if self.cropping:
            self.canvas.delete('crop_rect')
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
            x2, y2 = self.crop_rect_xy(x2, y2)
            self.crop_rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color.yellow[15], tag='crop_rect', width=3)

    def crop_rect_xy(self, x, y):
        x_min, y_min = self.photo_x, self.photo_y
        x_max, y_max = self.image.size
        x_max += x_min
        y_max += y_min

        x = max(x, x_min)
        x = min(x, x_max)
        y = max(y, y_min)
        y = min(y, y_max)

        if x < x_min or x > x_max or abs(x - self.start_x) * self.crop_ratio < abs(y - self.start_y):
            x_len = abs(y - self.start_y) / self.crop_ratio
            if x - self.start_x < 0: x_len *= -1
            x_out = self.start_x + x_len
            y_out = y

            if x_out < x_min or x_out > x_max:
                x_out = (x_min if x_out < x_min else x_max)
                y_len = abs(x_out - self.start_x) * self.crop_ratio
                if y - self.start_y < 0: y_len *= -1
                y_out = self.start_y + y_len
        else:
            y_len = abs(x - self.start_x) * self.crop_ratio
            if y - self.start_y < 0: y_len *= -1
            y_out = self.start_y + y_len
            x_out = x

            if y_out < y_min or y_out > y_max:
                y_out = (y_min if y_out < y_min else y_max)
                x_len = abs(y_out - self.start_y) / self.crop_ratio
                if x - self.start_x < 0: x_len *= -1
                x_out = self.start_x + x_len


        return x_out, y_out


    def end_crop(self, event):
        # 用户释放鼠标，结束截图选择
        if self.cropping:
            self.cropping = False
            self.canvas.unbind("<B1-Motion>")
            # 获取截图区域的坐标
            if self.crop_rect == None:
                return None
            x1, y1, x2, y2 = self.canvas.coords('crop_rect')
            # print(x1, y1, x2, y2)
            # 删除临时绘制的矩形
            self.canvas.delete('crop_rect')
            # 裁剪图片
            self.cropped_image = self.crop_image(x1, y1, x2, y2)
            # 显示裁剪后的图片
            self.show_cropped_image()
            self.crop_has_been_saved = False

    def show_cropped_image(self):

        # 获取图片原始大小
        original_width, original_height = self.cropped_image.size

        # 获取画布大小
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        # 计算放大比例，保持图片的比例不变
        # 假设我们想要图片的长边触及画布边缘
        scale_width = canvas_width / original_width
        scale_height = canvas_height / original_height
        scale = min(scale_width, scale_height)

        # 计算放大后的图片大小
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        image = self.cropped_image.resize((new_width, new_height))

        # 计算图片在画布上的位置，使得至少一边触及边缘
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        # 在画布上绘制图片
        self.preview_photo = ImageTk.PhotoImage(image)
        self.preview_canvas.create_image(x, y, image=self.preview_photo, anchor=tk.NW)

        # 刷新画布
        self.preview_canvas.update()

        self.save_tip_label.config(text="未保存")

    def crop_image(self, x1, y1, x2, y2):

    # 将画布坐标转换为图片坐标（考虑缩放比例）
        original_width, original_height = self.original_image.size
        image_width, image_height = self.current_photo.width(), self.current_photo.height()
        # 计算缩放比例        
        scale_width = 1.0 * original_width / image_width
        scale_height = 1.0 * original_height / image_height

        x1_img = int((x1 - self.photo_x) * scale_width)
        y1_img = int((y1 - self.photo_y) * scale_height)
        x2_img = int((x2 - self.photo_x) * scale_width)
        y2_img = int((y2 - self.photo_y) * scale_height)
        area = (min(x1_img, x2_img), min(y1_img, y2_img), max(x1_img, x2_img), max(y1_img, y2_img))
        print(x1_img, y1_img, x2_img, y2_img, "||", image_height, original_height)

        # 裁剪图片
        cropped_image = self.original_image.crop(area)
        # cropped_image.show()
        return cropped_image

    def save_cropped_image(self, event):
        if self.crop_has_been_saved:
            return None
        if self.export_dir == "":
            messagebox.showerror("错误", "未指定文件保存路径" )
        form = "." + self.current_image_path.split(".")[-1]
        path = self.export_dir + "\\" + str(self.export_num) + form
        self.export_num += 1
        try:
            self.cropped_image.save(path)
            self.save_tip_label.config(text="保存成功")
            self.crop_has_been_saved = True
        except Exception as e:
            try:
                self.cropped_image = self.cropped_image.convert('RGB')
                self.cropped_image.save(path)
                self.save_tip_label.config(text="保存成功")
                self.crop_has_been_saved = True
            except Exception as e:
                messagebox.showerror("错误", "保存图片时出错: " + str(e))

    def next_image(self, event):
        if self.current_image_index == len(self.image_files) - 1:
            return None
        self.load_image(self.current_image_index + 1)
        self.image_loader.forward()
        self.current_image_index += 1

        # 加载源目录中的上一张图片
        # 省略代码...

    def prev_image(self, event):
        if self.current_image_index == 0:
            return None
        self.load_image(self.current_image_index - 1)
        self.image_loader.backward()
        self.current_image_index -= 1
        # 加载源目录中的下一张图片
        # 省略代码...

    # 其他辅助函数...
