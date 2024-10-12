import pytesseract
import cv2
import numpy as np
from PIL import Image
import pyautogui
from ctypes import windll
import time

# 待比较的两个数
a = 0
b = 0

# 获取图片
def get_image():
    # 截屏返回result对象
    result = pyautogui.screenshot()
    # 保存图像
    result.save('./img/screenshot.jpg')
    # 裁剪图像
    # region设置截图区域[x,y,w,h]，以(x,y)为左上角顶点，截宽w，高h的区域
    result = pyautogui.screenshot(imageFilename='./img/result.jpg', region=[110,300,310,100])

# 图片预处理
def reprocess_image():
    # 图像对象格式转换
    image = Image.open('./img/result.jpg')
    image_np = np.array(image)
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # 二值化处理
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    # 去噪处理
    #denoised_image = cv2.medianBlur(binary_image, 3) # 二值化就够识别了
    return binary_image

# OCR识别
def ocr_image():
    global a, b
    binary_image = reprocess_image()
    # 使用Tesseract进行文字识别
    s = pytesseract.image_to_string(binary_image, config='--psm 6')
    # 针对特定的识别错误进行处理
    str = ''
    if 'T/' in s or ')' in s:
        for i in s:
            if i=='T':
                str += '1'
            elif i=='/':
                str += '7'
            elif i==')':
                str += '5'
            else:
                str += i
    else:
        str = s
    print(f'OCR结果：{str}', end='')
    # 取出待比较的两个数字
    a = 0
    b = 0
    for i in str:
        if i>='0' and i<='9':
            a = 10*a+int(i)
        else:
            break
    idx = str.rfind(' ')
    str = str[idx+1:-1]
    for i in str:
        if i>='0' and i<='9':
            b = 10*b+int(i)
    print(f'    取得数字：{a} {b}')
    return a, b

# 绘制答案
def write_answer():
    # 待比较数字
    a, b = ocr_image()
    # 设置每次鼠标操作之间的暂停时间
    pyautogui.PAUSE = 0.0005
    # 答案
    if a>b:
        x, y = 200, 700
        for i in range(20):
            x += 1
            y += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        for i in range(20):
            x -= 1
            y += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        # 弹起鼠标，提交答案
        pyautogui.mouseUp()
    elif a<b:
        x, y = 200, 700
        for i in range(20):
            x -= 1
            y += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        for i in range(20):
            x += 1
            y += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        # 弹起鼠标，提交答案
        pyautogui.mouseUp()
    else:
        x, y = 200, 700
        for i in range(20):
            x += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        x, y = 200, 710
        for i in range(20):
            x += 1
            windll.user32.SetCursorPos(x, y)
            pyautogui.click()
        # 弹起鼠标，提交答案
        pyautogui.mouseUp()
    
# 主函数
def main():
    """
    # 单人挑战，考虑误差
    while(1):
        # 获取图像
        get_image()
        # 预处理
        reprocess_image()
        # 写答案
        write_answer()
        # 给答案上传时间
        time.sleep(0.6)
        if a==0 and b==0:
            break
    """
    
    # PK对战，卡bug直接ak
    # 没开始之前，识别为0 0，上锁
    flag = True
    while(1):
        # 获取图像
        get_image()
        # 预处理
        reprocess_image()
        # 取数
        a, b = ocr_image()
        if a!=0 and b!=0:
            # 写答案
            write_answer()
            # 解锁
            flag = False
        # PK结束，再次识别为0 0，此时已解锁，退出
        if a==0 and b==0 and flag==False:
            break
    

if __name__=='__main__':
    main()
    