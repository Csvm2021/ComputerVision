import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('/content/drive/MyDrive/mo.jpg')
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

# Mostrar la imagen con los contornos y los centroides
plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB))
plt.show()

# Mostrar el número de fichas por cada fila en la consola
print('Número de fichas por cada fila:')
for i, count in enumerate(counts):
 print(f'Fila {i+1}: {count}')