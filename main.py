import os

import cv2
import numpy

import sys
import hashlib


# sprite3_json_format =

class Sprite3:
    def __init__(self):
        self.isStage = False
        self.name = "words"
        self.variables = {}


def str2object(line_str):
    line_str = line_str.replace("\n", "")
    line_str = line_str.replace("char ", "")
    line_str = ' '.join(line_str.split())

    obj = {}
    result = line_str.split(' ')
    for item in result:
        values = item.split('=')
        obj[values[0]] = values[1]

    return obj


def letter2img(letter, fnt, img1):
    fntLetter = fnt.letters[ord(letter)]

    I = numpy.zeros((fnt.lineHeight, fntLetter.xoffset + fntLetter.width, 4), dtype=numpy.uint8)

    x1 = fntLetter.x
    w1 = fntLetter.x + fntLetter.width
    y1 = fntLetter.y
    h1 = fntLetter.y + fntLetter.height
    yoffset = fntLetter.yoffset
    xoffset = fntLetter.xoffset

    lettera_img = img1[y1: h1, x1: w1]

    I[yoffset:yoffset + fntLetter.height, xoffset: xoffset + fntLetter.width] = lettera_img

    # I[22, 22] = [255, 255, 255,0]
    # op = I[22, 22, 3]
    # print(op)
    # cv2.imshow(letter, I)
    return I


def gen_word_img(word, _fnt, img1):
    imglists = []
    for _letter in word:
        imglists.append(letter2img(_letter, _fnt, img1))

    # TODO 字组合间距调整 http://www.2cto.com/uploadfile/2012/0903/20120903112659845.jpg
    word_img = cv2.hconcat(imglists)
    return word_img


class FntLetter:
    def __init__(self, id, letter, x, y, width, height, xoffset, yoffset, xadvance):
        self.id = id
        self.letter = letter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.xadvance = xadvance

    def __init__(self, obj):
        self.id = int(obj['id'])
        self.letter = obj['letter']
        self.x = int(obj['x'])
        self.y = int(obj['y'])
        self.width = int(obj['width'])
        self.height = int(obj['height'])
        self.xoffset = int(obj['xoffset'])
        self.yoffset = int(obj['yoffset'])
        self.xadvance = int(obj['xadvance'])


class Fnt:
    letters: {int: FntLetter} = {}

    def __init__(self, url):
        print(url)
        f = open(url)
        f.readline()
        line2 = f.readline()
        line2 = line2.replace("\n", "")
        line2_item = line2.split(' ')
        self.lineHeight = int(line2_item[1].split("=")[1])
        f.readline()
        f.readline()
        line = f.readline()
        while len(line) > 2:
            obj = str2object(line)
            self.letters[int(obj['id'], base=10)] = FntLetter(obj)
            line = f.readline()


fnt = Fnt("po_FZLanTinYuanS-EB_GB.fnt")

# print(fnt.lineHeight)

file_md5_map = {}

img = cv2.imread('po_FZLanTinYuanS-EB_GB.png', cv2.IMREAD_UNCHANGED)

result = gen_word_img("word", fnt, img)

cv2.imshow("word", result)
cv2.imwrite("word.png", result, [cv2.IMWRITE_PNG_COMPRESSION, 0])
file_name = "word.png"
with open(file_name, 'rb') as fp:
    data = fp.read()
file_md5 = hashlib.md5(data).hexdigest()
file_md5_map["word"] = file_md5
os.rename("word.png", file_md5 + ".png")

print(file_md5)
# char id=97     x=203   y=817   width=62    height=69    xoffset=2     yoffset=45    xadvance=63    page=0 chnl=0 letter="a"
# char id=98     x=516   y=442   width=68    height=100   xoffset=5     yoffset=13    xadvance=69    page=0 chnl=0 letter="b"
# char id=99     x=2     y=817   width=67    height=69    xoffset=3     yoffset=44    xadvance=65    page=0 chnl=0 letter="c"
# info face="FZLanTingYuanS-EB-GB" size=120 bold=0 italic=0 charset="" unicode=0 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=2,2


# I=numpy.zeros((206,210),dtype=numpy.uint8)
# print(I.shape)
# I=cv2.hconcat([img1,img2])#水平拼接
# cv2.imwrite("img_dir.png", I, [cv2.IMWRITE_PNG_COMPRESSION, 0])
# cv2.imshow("aa",img1)
cv2.waitKey(0)
