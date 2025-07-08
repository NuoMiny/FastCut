import os
from PIL import Image


class ImageLoader:
    def __init__(self, image_directory):
        self.image_directory = image_directory
        self.image_files = self.get_image_files(image_directory)
        self.preload_dict = {}
        self.current_index = 0
        self.load_images_around_index(self.current_index)

    def get_image_files(self, directory):
        image_files = []
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_files.append(filename)
        return image_files

    def load_image(self, filename):
        image_path = os.path.join(self.image_directory, filename)
        return Image.open(image_path)

    def load_images_around_index(self, index):
        start_index = max(0, index - 2)
        end_index = min(len(self.image_files) - 1, index + 2)
        for i in range(start_index, end_index + 1):
            if i not in self.preload_dict:
                self.preload_dict[i] = self.load_image(self.image_files[i])
                # Remove images that are too far away if they exist
        for i in list(self.preload_dict.keys()):
            if i < start_index - 1 or i > end_index + 1:
                del self.preload_dict[i]

    def get_image(self, index):
        if index < 0 or index >= len(self.image_files):
            raise IndexError("Index out of range")
        if index not in self.preload_dict:
            self.load_images_around_index(index)
        return self.preload_dict[index]

    def set_current_index(self, index):
        if index < 0 or index >= len(self.image_files):
            raise IndexError("Index out of range")
        self.current_index = index
        self.load_images_around_index(self.current_index)

    def forward(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_images_around_index(self.current_index)

    def backward(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_images_around_index(self.current_index)

        # 使用示例

if __name__ == "__main__":

    image_directory = 'path/to/your/images'  # 替换为你的图片源文件目录
    image_loader = ImageLoader(image_directory)

    # 获取第一张图片
    image = image_loader.get_image(0)
    image.show()

    # 向前移动
    image_loader.forward()
    image = image_loader.get_image(image_loader.current_index)
    image.show()

    # 向后移动
    image_loader.backward()
    image = image_loader.get_image(image_loader.current_index)
    image.show()