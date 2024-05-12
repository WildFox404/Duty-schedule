import cv2
import os
import numpy as np
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# 假设图片的宽度是每天课程的数量（4节课），高度是周的天数（5天）
DAYS_PER_WEEK = 5
CLASSES_PER_DAY = 4


# 函数来识别无课时间段
def find_empty_slots(image, threshold_value=200):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用阈值化，将像素值低于阈值的设为0（黑色），高于或等于阈值的设为255（白色）
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    # cv2.imshow('Gray', thresh)
    # cv2.waitKey(0)  # 等待任意键继续
    # 计算每个格子的大小（可能需要四舍五入到最接近的整数）
    cell_height = thresh.shape[0] // 4
    cell_width = thresh.shape[1] // 5

    # 找出无课的时间段
    empty_slots = []
    for day in range(DAYS_PER_WEEK):
        for class_hour in range(CLASSES_PER_DAY):
            # 计算格子位置（注意可能需要调整以避免索引越界）
            y_start = day * cell_height
            y_end = min(y_start + cell_height, thresh.shape[0])
            x_start = class_hour * cell_width
            x_end = min(x_start + cell_width, thresh.shape[1])

            # 计算格子内白色（无课）像素的数量
            white_pixels = np.sum(thresh[y_start:y_end, x_start:x_end] == 255)
            # 计算格子内黑色（有课）像素的数量
            black_pixels = (y_end - y_start) * (x_end - x_start) - white_pixels
            # 提取格子内的图像
            slot_image = thresh[y_start:y_end, x_start:x_end]

            # 如果需要显示
            # 创建一个窗口来显示格子图像
            window_name = f'Slot {day + 1}-{class_hour + 1}'
            # cv2.imshow(window_name, slot_image)

            # # 等待一段时间，比如100毫秒，然后关闭窗口
            # cv2.waitKey(0)
                # 如果白色像素数量多于黑色像素数量，则认为该格子无课
            if white_pixels > black_pixels:
                empty_slots.append((class_hour+1, day + 1))  # 加1以符合题目要求

    return empty_slots


# 主函数
def process_images_folder(folder_path, output_excel_path):
    # 创建一个Excel工作簿
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Empty Slots"])

    # 遍历文件夹中的图片
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            name, _ = os.path.splitext(filename)
            image_path = os.path.join(folder_path, filename)
            print(image_path)

            # 读取图片
            image = cv2.imdecode(np.fromfile(image_path,dtype=np.uint8),-1)
            if image is None:
                print(f"Error reading image: {image_path}")
                continue

                # 识别无课时间段
            empty_slots = find_empty_slots(image)

            # 将结果添加到Excel工作表
            ws.append([name, str(empty_slots)])

            # 保存Excel文件
    wb.save(output_excel_path)

if __name__ == '__main__':
    # 调用主函数
    process_images_folder('.\course', 'output.xlsx')