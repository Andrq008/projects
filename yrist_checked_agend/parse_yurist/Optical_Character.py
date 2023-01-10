from time import sleep
from pytesseract import pytesseract
import cv2

#path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path_to_tesseract = "/bin/tesseract"
pytesseract.tesseract_cmd = path_to_tesseract

def optical_img():
    sleep (1)
    img = cv2.imread("/home/specit/parse_yurist/test.jpg")
#    print('step 1')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU |
                                              cv2.THRESH_BINARY_INV)
    sleep(0.3)
    cv2.imwrite('/home/specit/parse_yurist/test.jpg',thresh1)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 3)
    sleep(0.3)
#    print('step 2')
    cv2.imwrite('/home/specit/parse_yurist/test.jpg',dilation)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)
#    print('step 3')
    im2 = img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Рисуем ограничительную рамку на текстовой области
        rect=cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Обрезаем область ограничительной рамки
        cropped = im2[y:y + h, x:x + w]

        cv2.imwrite('/home/specit/parse_yurist/test.jpg',rect)


        # Использование tesseract на обрезанной области изображения для получения текста
        text = pytesseract.image_to_string(cropped, lang='rus')
#        text = pytesseract.image_to_string(cropped)
#        print(text.replace(" ", "")[:-2])
        return text.replace(" ", "")[:-2].replace("\n","").replace("\r","")
#optical_img()
