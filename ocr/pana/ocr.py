# Requires spanish trained data https://github.com/tesseract-ocr/tessdata_best/blob/master/spa.traineddata


image_path = 'test.jpg'
tesseract_config = '--oem 3'


import copy
import json
import re
import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
from pytesseract import Output

# Preprocessing

## - Rotate the image
# https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
angle = -(90 + angle) if angle < -45 else -angle
h, w = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite('rotated.png', rotated)


img = cv2.imread('rotated.png', 0) if angle else cv2.imread(image_path, 0)
thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imwrite('pre_processed.jpg', thresh)

"""
# Compare thresholding methods
thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,5,5)
thresh2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
thresh3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,11)
thresh4 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15, 15)
data = [
	('ADAPT BIN (5, 5)', thresh1),
	('ADAPT BIN (11, 2)', thresh2),
	('ADAPT BIN (11, 11)', thresh3),
	('ADAPT BIN (15, 15)', thresh4),
]
for i, info in enumerate(data):
	plt.subplot(2,2,i+1),plt.imshow(info[1],'gray',vmin=0,vmax=255)
	plt.title(info[0])
	plt.xticks([]),plt.yticks([])

plt.show()
"""

# Text Detection

preprocessed_img = cv2.imread('pre_processed.jpg')
d = pytesseract.image_to_data(preprocessed_img, output_type=Output.DICT, config=tesseract_config)
n_boxes = len(d['level'])
for i in range(n_boxes):
	x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
	preprocessed_img = cv2.rectangle(preprocessed_img, (x, y), (x + w, y + h), (0, 0, 255), 1)

cv2.imwrite('text_detection.jpg', preprocessed_img)

# Text Recognition

text_detected_img = copy.deepcopy(thresh)

## - Spanish lang
extracted_text = pytesseract.image_to_string(text_detected_img, lang='spa', config=tesseract_config)
formatted_text = '\n'.join(line for line in extracted_text.rsplit('\n') if line.strip())
print(formatted_text)
"""
[EAN LACTAL SALVADO “
PAN DE MICA PAQUETE
2 [PAN DE MIGA TAO SALVADO:
PAN HAMBURGUESA PAQUETE RA
"IBAN CHOI
[PAN PARA PERNIL PAQUETE X 6.
[PAN PANCHOS PAQUETE X 6:
AN HAMBURGUESA (FOR BOLSA]
PAN DE LOMO PAQUETEX 2 —
- [PAN TORPEDO
[GRISINES ¡TALANOS
DAN DE VIENA LARGOS CORTOS
-—- |GRÍSINES COMUNES -
E
CAN DE LOMO KEOLSA CUADRADO —
[GRISINES CHATOS SABORIZADOS -
PAN PERNILCRICO (P/eDi5A) — [GRISINES CON SEMILLAS
PO == ISRISINES SALVADO —_-—
IMEDIALUNAS SALADAS. [GALLETITAS CON SEMILLAS
MADIALUNAS DULCES PAQUETE TOSTADAS. — ——!
FACTURAS GRANDES -
BIZCOCHOS DE AGUA- SALVADO
- [FACTURAS DULCE LECHE Y AZUCAR.
PAÑDE MIGA ENTERO “> —
FACTURAS HOJALDRE -
PÁN DE MIGA ENTERO SALVADO -
r [EACTURAS VIGILANTES ——— [PRE PIZZAS
| [EACTURAS= SACRAMENTOS. PIZETAS EIC
“ [FACTURAS CHICAS ———— TARTELETAS ———  -—
PATITAS: CHURRINCAIS — ———- [ORTA BIZCOCHUELO:
OONAS—- + [TORTA MIXTA ——
E -— |TORTAHOJALDRE — ——
BIZCOCHOS DULCES: —— 273: [TORTA POR PORCIÓN.
[BIZCOCHOS MEMBRILLO E iTANTÁS DUES —
[BIZCOCHOS CREMA PASTELERA A — [MASAS FINAS -
BIZCOCHOS BATATA =— — - -
BizcOcHOS CRIOLUTOS -
EIZCOCHUELOS SIN NADA
BIZCOCHOS CASERITOS (GRASA)
SCONES” ——
BIZCOCHOS SALADOS DE AGUÁ:
BIZCOCHOSSALADOS HOJALORE:
BIZCOCHOS= DE QUESO —
CHICHARONES
ILFAJORES MADRILEÑOS:
LEAJORES SANTAFESINOS:-
LEAJORES MAICENA :
ALMERITAS:: ——
ASITAS:SABORIZADAS -—
ERENGUES CHICOS CON DULCE:
ERENGADOS GRANDES:
TA FROLAS GRANDES
TA FROLAS CHICAS: +
INES. — —
"""

## - Default lang
extracted_text = pytesseract.image_to_string(text_detected_img, config=tesseract_config)
formatted_text = '\n'.join(line for line in extracted_text.rsplit('\n') if line.strip())
print(formatted_text)
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

## - Comparison: default lang trained data generates better results than the spanish one.
