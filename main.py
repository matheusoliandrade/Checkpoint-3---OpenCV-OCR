import cv2
import pytesseract

class Blocos_Separaçao:
    def __init__(self, x, y, h, w, img):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.img = img
        self.img_roi()

    def img_roi(self):
        self.roi = self.img[self.y:self.y+self.w, self.x:self.x+self.h]
        xy = (self.x,self.y)
        hw = (self.x+self.h,self.y+self.w)
        co = (0, 255, 0) 
        cv2.rectangle(img, xy, hw, co, 2)  
    
pytesseract.pytesseract.tesseract_cmd = "c:/Program Files/Tesseract-OCR/tesseract.exe"

img = cv2.imread("./cnh.webp")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

blured_image = cv2.GaussianBlur(thresholded, (3,3), 0)

Nome = Blocos_Separaçao(160,140,560,30,blured_image)
N_Doc = Blocos_Separaçao(160,475,220,30,blured_image)
Rg = Blocos_Separaçao(410,196,280,27,blured_image)
Cpf = Blocos_Separaçao(410,243,180,30,blured_image)
Data_Nasc = Blocos_Separaçao(600,243,130,30,blured_image)
Cat_H = Blocos_Separaçao(655,425,80,30,blured_image)
Data_Val = Blocos_Separaçao(400,475,150,30,blured_image)
Data_Emi = Blocos_Separaçao(575,823,150,30,blured_image)
Obs = Blocos_Separaçao(160,566,570,80,blured_image)
Ass = Blocos_Separaçao(170,735,400,45, blured_image)
Foto = Blocos_Separaçao(175,200,190,235,img)

infos_names = ["Nome", "Numero do documento", "RG", "CPF", "Data de Nascimento", 
               "Categoria da habilitação", "Data de Validade", "Data de Emissão", "Observações"]
infos_text = [Nome, N_Doc, Rg, Cpf, Data_Nasc, Cat_H, Data_Val, Data_Emi, Obs]
with open("./infos_extraidas/infos_texto.txt", "w+") as arquivo:
    for name, info in zip(infos_names, infos_text):
        if pytesseract.image_to_string(info.roi):
            arquivo.writelines(f"{name} = {pytesseract.image_to_string(info.roi, config=r'--oem 3 --psm 6')}")
        else:
            arquivo.writelines(f"{name} = Não identificado")
            arquivo.writelines("\n")
    arquivo.close()

cv2.imwrite("./infos_extraidas/Assinatura.png", cv2.Canny(Ass.roi, 100, 200))
cv2.imwrite("./infos_extraidas/Foto.png", Foto.roi)

cv2.imshow("Cnh",img)
cv2.waitKey(0)
cv2.destroyAllWindows()


    
