import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import cv2
import numpy as np
import os

from PIL import Image, ImageChops
from tkinter import ttk, DISABLED
from os.path import expanduser

app = tk.Tk()
app.resizable(True, True)

app.title("貼り付けくん")
app.geometry('500x500')

fYtp = [("", "*.png")]

filenames = []
filename2=  ""
savefolderName = ""

i=0

PADDING = 20

FRAME_X = 6
FRAME_Y = 58
FRAME_WIDTH = 285
FRAME_HEIGHT = 191


def autocrop(image):
    # getpixel(0, 0) で左上の色を取得し、背景色のみの画像を作成する
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))

    # 背景色画像と元画像の差分を取得
    diff = ImageChops.difference(image, bg)
    #diff.show()
    diff = ImageChops.add(diff, diff, 2.0, -100)
    #diff.show()
    # 黒背景の境界Boxを取り出す
    if(diff.getbbox() == None): 
        cropped = diff
    else:
        bbox = diff.getbbox()

        offset = PADDING
        bbox2 = (bbox[0] - offset, bbox[1] - offset,
        bbox[2] + offset, bbox[3] + offset)
        
        # 元画像を切り出す
        cropped = image.crop(bbox2)
    
    return cropped

def chooseFiles():
    global filenames
    filenames = tkinter.filedialog.askopenfilenames(
        filetypes=[("", "*.png"), ("", "*.jpg")])

    fileDone1 = tk.Label(frame_3, text="ファイル選択完了")
    fileDone1.grid(column=0, row=4, padx=5, pady=15)

def chooseFile2():
    global filename2
    filename2 = tkinter.filedialog.askopenfilename(
        filetypes=[("", "*.png"), ("", "*.jpg")])

    fileDone2 = tk.Label(frame_3, text=filename2)
    fileDone2.grid(column=0, row=6, padx=5, pady=15)

def chooseFolder():
    global savefolderName
    savefolderName = tkinter.filedialog.askdirectory(
        title="保存先フォルダを選択", mustexist=True, initialdir=os.getcwd())
    
    savefolderName = savefolderName + os.sep
    
    folderDone = tk.Label(frame_3, text=savefolderName)
    folderDone.grid(column=0, row=8, padx=5, pady=15)


# resize cropped image
def scale_to_width(img, width):
    height = round(img.height * width / img.width)
    return img.resize((width, height), Image.LANCZOS)


def scale_to_height(img, height):
    width = round(img.width * height / img.height)
    return img.resize((width, height), Image.LANCZOS)


def item2frame(item_image, bg):

    frame = bg.copy()
    # get image width and height
    im_width, im_height = item_image.size

    if im_width >= im_height:
        scaled_im1 = scale_to_width(item_image, FRAME_WIDTH)
        # get center coordinates
        w_c, h_c = scaled_im1.size
        x = 0
        y = (FRAME_HEIGHT - h_c) // 2

    else:
        scaled_im1 = scale_to_height(item_image, FRAME_HEIGHT)
        # get center coodinates
        w_c, h_c = scaled_im1.size
        x = (FRAME_WIDTH - w_c)//2
        y = 0

    frame.paste(scaled_im1, (FRAME_X+x, FRAME_Y+y))

    return frame


def save_img(img):
    global i

    basename = os.path.splitext(os.path.basename(filenames[i]))[0]

    img.load()  # required for png.split()

    save_path = ""

    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])  # 3 is the alpha channel

    save_path = savefolderName + basename + "-" + janTxt.get() + ".jpg"
    bg.save(save_path, "JPEG", quality=95)


def makeImage():
    global i
    i=0

    # check file
    if filenames[0] == "" or filename2 == "":
        tkinter.messagebox.showerror(title="Error", message="ファイルを選択してください。")
        return

    # check folder
    if savefolderName == "":
        tkinter.messagebox.showerror(title="Error", message="保存先フォルダを選択してください。")
        return
    
    for i in range(len(filenames)):

        basewidth = 300

        im1 = Image.open(filenames[i]).convert("RGBA")
        im2 = Image.open(filename2).convert("RGBA")
        bg = Image.new('RGBA', (basewidth, basewidth), "white")

        # crop image

        cropped_im1 = autocrop(im1)

        frame = bg.copy()
        final_img = item2frame(cropped_im1, frame)

        final_img.paste(im2, (0, 0), im2)

        save_img(final_img)


titleLabel = tk.Label(text="貼り付けくん", font=("Helvetica", 20))
titleLabel.grid(column=0, row=0, pady=10, sticky=tk.W + tk.E)

frame_1 = tk.LabelFrame(app)
frame_1.grid(row=1, column=0, sticky=tk.W + tk.E, padx=20)
frame_2 = tk.LabelFrame(app)
frame_2.grid(row=2, column=0, sticky=tk.W + tk.E, padx=20)
frame_3 = tk.LabelFrame(app)
frame_3.grid(row=3, column=0, sticky=tk.W + tk.E, padx=20)
frame_4 = tk.LabelFrame(app)
frame_4.grid(row=4, column=0, sticky=tk.W + tk.E, padx=20)

filesLabel = tk.Label(frame_3, text=u"下レイヤーは複数選択可能です")
filesLabel.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)
fileButton1 = tk.Button(frame_3, text="ファイル選択(下レイヤー)", command=chooseFiles)
fileButton1.grid(column=0, row=3, padx=10, pady=10, sticky=tk.E)

fileButton2 = tk.Button(frame_3, text="ファイル選択(上レイヤー)", command=chooseFile2)
fileButton2.grid(column=0, row=5, padx=10, pady=10, sticky=tk.E)

folderButton = tk.Button(frame_3, text="保存先フォルダ選択", command=chooseFolder)
folderButton.grid(column=0, row=7, padx=10, pady=10, sticky=tk.E)

janLabel = tk.Label(frame_4, text=u"保存ファイル名 (元のファイル名に付加されます)")
janLabel.grid(column=0, row=0, padx=10, pady=10)

janTxt = tk.Entry(frame_4, width=30)
janTxt.grid(column=1, row=0, padx=10, pady=10)

createButton = tk.Button(text="  画像生成  ", font=(
    "Helvetica", 15), command=makeImage)
createButton.grid(column=0, row=5, padx=10, pady=10,
                  sticky=tk.S)

tk.mainloop()