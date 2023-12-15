from email.mime import image
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils
from matplotlib import pyplot as plt


#Creamos la ventana principal
root = Tk()


def elegir_imagen():
    #Especificar tipos de archivos, para elegir solo las imagenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpg"),
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jfif")])
    
    if len(path_image) > 0:
        global image

        #leer la imagen de entrada
        image = cv2.imread(path_image)
        image = imutils.resize(image, height=380)

        #Visualizar imagen en la entrada de la GUI
        imageToShow = imutils.resize(image, width=180)
        imageToShow= cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img # type: ignore

        #Imagen de entrada
        lblInfo1 = Label(root, text = "IMAGEN DE ENTRADA")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)

def contar_fichas_por_color():

    # Cargar la imagen
    imagen = cv2.imread(image_cv)

    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir los rangos de color para las fichas blancas y negras
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])

    # Crear máscaras para las fichas blancas y negras
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # Encontrar contornos en las máscaras
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos basados en el área
    min_area = 130  # Área mínima del contorno para considerar
    filtered_contours_white = [cnt for cnt in contours_white if cv2.contourArea(cnt) > min_area]
    filtered_contours_black = [cnt for cnt in contours_black if cv2.contourArea(cnt) > min_area]

    # Crear una lista vacía para almacenar el número de fichas por color
    fichas_por_color = []

    # Recorrer los contornos de cada color y contarlos
    for color, contours in zip(["blancas", "negras"], [filtered_contours_white, filtered_contours_black]):
        # Inicializar el contador de fichas para el color actual
        fichas = len(contours)
        # Añadir el contador de fichas a la lista
        fichas_por_color.append(fichas)
        # Dibujar los contornos en la imagen
        #cv2.imshow(image_cv)  # Reemplazar cv2.imshow() con cv2_imshow()
        finalImage= cv2.drawContours(imagen, contours, -1, (2, 180, 0), 2)
        imageToShowOutput = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

        im = Image.fromarray(imageToShowOutput)
        img = ImageTk.PhotoImage(image=im)
        lblOutputImage.configure(image=img)
        lblOutputImage.image = img # type: ignore

        cadena = 'blancas '+', negras '.join(map(str, fichas_por_color))
        lblResultado.config(text="Fichas por color: " + cadena, font="bold")

        #Label imagen de salida
        lblInfo3 = Label(root, text="IMAGEN DE SALIDA", font="bold")
        lblInfo3.grid(column=1, row=0, padx=5, pady=5)

    # Mostrar los resultados
    #cv2.imshow(image_cv) # Reemplazar cv2.imshow() con cv2_imshow()
    #print("Fichas por color:", fichas_por_color)


def contar_fichas_por_fila():
    img = cv2.imread(image_cv)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un filtro pasa-bajas
    gaus = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar el algoritmo de Canny para detectar los bordes de las fichas
    canny = cv2.Canny(gaus, 102, 322) #113-323 #115, 328 #102-322          #116, 318

    # Encontrar los contornos de las fichas
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en una imagen vacía
    img_contours = np.zeros_like(img)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

    # Calcular el centroide de cada contorno
    centroids = []
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centroids.append((cx, cy))
            cv2.circle(img_contours, (cx, cy), 8, (0, 0, 255), -1) #5

    # Sort the centroids by their x and y coordinates
    centroids.sort(key=lambda x: (x[1], x[0]))

    # Group the centroids into rows
    rows = []
    row = []
    prev_y = centroids[0][1]
    for cx, cy in centroids:
        if abs(cy - prev_y) < 25 : # Threshold for determining if two centroids are in the same row
            row.append((cx, cy))
        else:
            rows.append(row)
            row = [(cx, cy)]
        prev_y = cy
    rows.append(row) # Add the last row

    # Contar el número de fichas por cada fila
    counts = []
    for row in rows:
        counts.append(len(row))

    
    imageToShowOutput = cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(imageToShowOutput)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img # type: ignore

    cadena = ', '.join(map(str, counts))
    lblResultado.config(text="Fichas por color: " + cadena, font="bold")

        #Label imagen de salida
    lblInfo3 = Label(root, text="IMAGEN DE SALIDA", font="bold")
    lblInfo3.grid(column=1, row=0, padx=5, pady=5)

    # Mostrar el número de fichas por cada fila en la consola
    print('Número de fichas por cada fila:')
    for i, count in enumerate(counts):
        print(f'Fila {i+1}: {count}')


# Ruta de la imagen
image = None
image_cv = "D:/ComputerVision/table4.jfif"


#Label donde se muestra la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

#Label donde se muestra la imagen de salida
lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=4)

lblResultado = Label(root)
lblResultado.grid(column=1, row=5)

#Label
lblInfo2 = Label(root, text="Elige una funcion", width=25)
lblInfo2.grid(column=0, row=3, padx=5, pady=5)

#Creamos los radiobuttons y su posicion
selected = IntVar()
rad1= Radiobutton(root, text="Contar por colores", width=25, value=1, variable=selected, command=contar_fichas_por_color)
rad2= Radiobutton(root, text="Contar por filas", width=25, value=2, variable=selected, command=contar_fichas_por_fila)
rad1.grid(column=0, row=4)
rad2.grid(column=0, row=5)

#Boton para elegir la imagen
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

root.mainloop()