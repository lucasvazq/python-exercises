image_path = 'test.jpg'


import copy
import json
import re
import cv2
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output

# Preprocessing

img = cv2.imread(image_path,0)
thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
cv2.imwrite('pre_processed.jpg', thresh)


"""
ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,120,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,120,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,120,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,120,255,cv2.THRESH_TOZERO_INV)
thresh6 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
thresh7 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
ret,thresh8 = cv2.threshold(img,195,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
blur = cv2.GaussianBlur(img,(5,5),0)
ret, thresh9 = cv2.threshold(blur,195,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
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
]
for i, info in enumerate(data):
	plt.subplot(4,3,i+1),plt.imshow(info[1],'gray',vmin=0,vmax=255)
	plt.title(info[0])
	plt.xticks([]),plt.yticks([])

plt.show()
"""

# Text Detection

preprocessed_img = cv2.imread('pre_processed.jpg')
d = pytesseract.image_to_data(preprocessed_img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
	x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
	preprocessed_img = cv2.rectangle(preprocessed_img, (x, y), (x + w, y + h), (0, 0, 255), 1)

cv2.imwrite('text_detection.jpg', preprocessed_img)

# Text Recognition

text_detected_img = copy.deepcopy(thresh)
extracted_text = pytesseract.image_to_string(text_detected_img)
default = '\n'.join(line for line in extracted_text.rsplit('\n') if line.strip())
print(default)
"""
PAN LACTAL SALVADO ~
PAN DE IGA PAGUETE
2 [PAN DE MIGA Fag SALVADO.
PAN HAMBURGUESA PAQUETE RA
‘PAN CHORIN
PAN FARA PEANIL PAGUETE NG
PAR PANCHGS PAGUIETE X 6:
RAN HAMBURGUESA [ROR BOISE]
PAN DE LOMO PAQUETEX? —
~ PAN TORPERQ ee
[GRISINES TALIANOS
PAN DE VIENA - LARGGS=CORTOE
--- |@RiGinEs COMUNES a
Biz
“AN DE LOMO K6O1Sa CUADRABO
GRISINES CHATOS SABORIZADOS ~
PAN PERNICCHICO (B/aniSay — [GRISINES CON SEMALLAS
sony =F [SRISWNES SALWADD — = —
IMEDIALUN AS SALADAS. JGAULETITAS CON SEMILLAS L
IMADIALUNAS DULEES ~ JPAQUETETOSTADAS——_—-=-—
EACTURAS GRANDES -
BIZCOCHOS OF AGUA SALVADO = —
~ [PACTURAS DULCE LECHE VAZLICAR
PAN DE MIGAENTERO "= —
FACTURAS HOUALORE =
PAN DE MIGAENTERO SALVADD<
 FACTURAS-ViGRANTES ~~ PRE PIZZAS:
+ [PACTURAS©SACRAMENTOS. PUETAS CHICAS =
/[FAGTORAG Citas. 7 = — == TARTELETAS ==
PATITAS® CHURRINCHIS ~ ~— —_ - fFORTA BIZCOCHUELG:
DONAS—~" + [TORTA MIxTA =
a a ~~ TORTAHOJALDRE
BIZCOCHOS DULCES-—_— Ai." FTORTA POR PORCION.-
[BIZCOCHOS MEMBRILLO AP, rans Cou, =
[BIZCOCHOS CREMA PASTELERA ‘A = |MASASFINAS ~
IBIZCOCHOS BATATA = —~ == = =
aIZCOCHOS CRIOLUTOS =
BIZCOCHUELOSSIN NADA
BIZCOCHOS CASERITOS (GRASA}
SCONES =~
[BIZCOCHOS SALADOS DE AGUA
BIZCOCHOS SALADOS HOJALORE:
BIZCOCHOS~= DE QUESD.
CHICHARONES,
\LFAJORES MADRILENOS:
LFAJORES SANTAFESINOS—
LFAJORES MAICENA -"_-
ALMERITAS . —
|ASITAS:SABORIZADAS *—
ERENGUES CHICOS CON DULCE:
ERENGADOS “GRANDES:
TA FROLAS GRANDES
TA FROLAS CHICAS:
INES. * ~ _
"""