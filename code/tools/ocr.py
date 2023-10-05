# import ddddocr
# ocr = ddddocr.DdddOcr()
# with open(r'c:\soft\1.png','rb') as f:
#     img_bytes = f.read()
# res = ocr.classification(img_bytes)
# print(res)

from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls = True,lang='ch')

img = r'c:\soft\1.png'

result = ocr.ocr(img,cls=True)
print(result[0])

boxes = []
txts = []
scores = []
for line in result[0]:
    boxes.append(line[0])
    txts.append(line[1][0])
    scores.append(line[1][1])
print("scores:")
for i in range(len(scores)):
    print (scores[i])
print("txts:")
for i in range(len(txts)):
	#原格式文本输出
    print (txts[i])
    #输出不换行
    #print (txts[i],end = "")
print("boxes:")
for i in range(len(boxes)):
    print (boxes[i])


import easyocr

#设为中英文混合识别：ch_sim en
reader = easyocr.Reader(['ch_sim','en'], gpu = False)
#路径改为用户需要识别的图片的路径
result = reader.readtext(r"c:\soft\1.png", detail = 0)
print(result)

for i in result:
    print(i, end = '')
