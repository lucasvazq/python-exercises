# https://nanonets.com/blog/receipt-ocr/
# Requires:
# - tesseract-ocr https://github.com/tesseract-ocr/tesseract
# - DEU trained data (only for this test) https://github.com/tesseract-ocr/tessdata/blob/master/deu.traineddata
# - pytesseract https://pypi.org/project/pytesseract/
# - opencv-python https://pypi.org/project/opencv-python/
# - numpy (included in opencv-python) https://numpy.org/install/
# - matplotlib https://matplotlib.org/


image_path = 'receipt.jpg'


import copy
import json
import re
from collections import namedtuple
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from pytesseract import Output


# Preprocessing

img = cv2.imread(image_path,0)

""""
# Thresholding
# https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
ret,thresh1 = cv2.threshold(img,195,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,195,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,195,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,195,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,195,255,cv2.THRESH_TOZERO_INV)
thresh6 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2) # 11
thresh7 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2) # 11
ret,thresh8 = cv2.threshold(img,195,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
blur = cv2.GaussianBlur(img,(5,5),0)
ret, thresh9 = cv2.threshold(blur,195,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret,thresh10 = cv2.threshold(img,195,255,cv2.THRESH_OTSU)
data = [
	('Original Image', img),
	('BINARY',thresh1),
	('BINARY_INV', thresh2),
	('TRUNC', thresh3),
	('TOZERO',thresh4),
	('TOZERO_INV', thresh5),
	('ADAPT_MEAN_BINARY', thresh6),
	('ADAPT_GAUSS_BINARY', thresh7),
	('BINARY+OTSU', thresh8),
	('BLUR', blur),
	('BINARY+OTSU w BLUR', thresh9),
	('OTSU', thresh10),
]
for i, info in enumerate(data):
	plt.subplot(4,3,i+1),plt.imshow(info[1],'gray',vmin=0,vmax=255)
	plt.title(info[0])
	plt.xticks([]),plt.yticks([])

plt.show()
"""

# ret,thresh = cv2.threshold(img,195,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret,thresh = cv2.threshold(img,195,255,cv2.THRESH_BINARY)
cv2.imwrite('pre_processed.jpg', thresh)

# Text Detection

preprocessed_img = cv2.imread('pre_processed.jpg')
# preprocessed_img = copy.deepcopy(thresh)
# preprocessed_img = cv2.imread('receipt.jpg')

d = pytesseract.image_to_data(preprocessed_img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
	x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
	preprocessed_img = cv2.rectangle(preprocessed_img, (x, y), (x + w, y + h), (0, 0, 255), 1)

cv2.imwrite('text_detection.jpg', preprocessed_img)


# Text Recognition

# text_detected_img = cv2.imread('text_detection.jpg')
# text_detected_img = copy.deepcopy(preprocessed_img)
text_detected_img = copy.deepcopy(thresh)
# text_detected_img = preprocessed_img

extracted_text = pytesseract.image_to_string(text_detected_img, lang = 'deu')
deu = '\n'.join(line for line in extracted_text.rsplit('\n') if line.strip())
print(deu)
"""
Berahotel
Grosse Scheidegg
3818 Grindelwald
Familie R. Müller
Rech. Nr. 4572 30.07. 2007/13:29: 17
Bar Tisch 7/01
2xLatte Macchiato da 4.50 CHF 9.00
1xGloki äa 5.00 CHF 5,00
1xSchweinschnitzel a 22.00 CHF 22.00
1xChässpätz 1i a 18.50 CHF 18,50
Total : CHF 54 .50
Incl. 7.6% MwSt 54.50 CHF: 3.85
Entspricht in Euro 36.33 EUR
Es bediente Sie: Ursula
MwSt Nr.: 430 234
Tel.: 033 853 67 16
Fax.: 033 853 67 19
E-mail: grossescheidegg@bluewin. ch
"""

extracted_text = pytesseract.image_to_string(text_detected_img)
default = '\n'.join(line for line in extracted_text.rsplit('\n') if line.strip())
print(default)
"""
Ber ghote]
Grosse Scheidegg
3818 Grindelwald
Familie R. Miller
Rech.Nr. 4572 30.07. 2007/ 13:29:17
Bar Tisch 7/01
axLatte Macchiato a 4.50 CHF 9.00
\xGloki 4 5.00 CHF 5.00
IxSchweinschnitzel a 22.00 CHF 22.00
IxChasspatz li a 18.50 CHF 18,50
Total: CHF 54,50
Incl. 7.6% MwSt 54.50 CHF: 3.85
Entspricht in Euro 36.33 EUR
Es bediente Sie: Ursula
MwSt Nr. : 430 234
Tel.: 033 853 67 16
Fax.: 033 853 67 19
E-mail: grossescheidegg@b|uewin. ch
"""

# Information Extraction

splited_info = deu.splitlines()
data = {}

data['name'] = f'{splited_info[0]} {splited_info[1]}'

date_regex = '(?P<date>(\d+ *. *){2} *\d+ *\/ *( *\d+ *:){2} *\d+)'
search = re.search(date_regex, deu)
data['date'] = ''.join(getattr(search, 'group', lambda: '')().split())

data['items'] = []
data['total'] = None

lines_with_chf = []
for line in splited_info:
  if re.search(r'CHF',line):
    lines_with_chf.append(line)

item_data_regex = re.compile(
	'(?P<item_amount>\d+)x(?P<item_name>.*)'					# 2xFoo 1 bar
	' .?(a|ä).? '									# da | &ä | äa
	'(?P<item_price>\d+( ?[\.,] ?\d+)?) CHF (?P<item_total>\d+( ?[\.,] ?\d+)?)'	# 2.50 CHF 5 .00
)
for line in lines_with_chf:
	if 'Total' in line:
		search = re.search('(?P<item_price>\d+( ?[\.,] ?\d+)?)', line)
		if search:
			data['total'] = ''.join(search.group().split()).replace(',', '.')
		break
	search = re.search(item_data_regex, line)
	if search:
		item_data = search.groupdict()
		item_data['item_price'] = ''.join(item_data['item_price'].split()).replace(',', '.')
		item_data['item_total'] = ''.join(item_data['item_total'].split()).replace(',', '.')
		data['items'].append(item_data)

# Data Dump

print(json.dumps(data, indent=4))
"""
{
    "name": "Berahotel Grosse Scheidegg",
    "date": "30.07.2007/13:29:17",
    "items": [
        {
            "item_amount": "2",
            "item_name": "Latte Macchiato",
            "item_price": "4.50",
            "item_total": "9.00"
        },
        {
            "item_amount": "1",
            "item_name": "Gloki",
            "item_price": "5.00",
            "item_total": "5.00"
        },
        {
            "item_amount": "1",
            "item_name": "Schweinschnitzel",
            "item_price": "22.00",
            "item_total": "22.00"
        },
        {
            "item_amount": "1",
            "item_name": "Ch\u00e4ssp\u00e4tz 1i",	# Chässpätz 1i
            "item_price": "18.50",
            "item_total": "18.50"
        }
    ],
    "total": "54.50"
}
"""