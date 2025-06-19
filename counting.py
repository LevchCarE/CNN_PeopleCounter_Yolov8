# Importación de bibliotecas necesarias
import cv2  # OpenCV para procesamiento de imágenes y video
import pandas as pd  # Pandas para manejo de datos tabulares
import numpy as np  # NumPy para operaciones numéricas
from ultralytics import YOLO  # YOLO para detección de objetos
from tracker import*  # Importación del módulo de seguimiento personalizado
import cvzone  # Biblioteca para facilitar el uso de OpenCV
# import datetime

# URL del video (comentada por seguridad)
url = "#########################################/video"

# Carga del modelo YOLO pre-entrenado
model=YOLO('yolov8n.pt')

# Función para manejar eventos del mouse y mostrar coordenadas
def RGB(event, x, y, flags, param):
    if(event==cv2.EVENT_MOUSEMOVE):
        point = [x,y]
        print(point)

# Configuración de la ventana y callback del mouse
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Inicialización de la captura de video desde la cámara
# cap=cv2.VideoCapture(0)
cap=cv2.VideoCapture('vidp.mp4')


# Configuración del escritor de video para guardar el resultado
output = cv2.VideoWriter('output_final.avi',cv2.VideoWriter_fourcc(*'MPEG'),30,(1020,500))

# Lectura de las clases de COCO dataset
file = open('coco.names', 'r')
data = file.read()
class_list = data.split('\n')

# Inicialización de variables para el conteo
count=0
persondown={}  # Diccionario para personas que bajan
tracker=Tracker()  # Inicialización del tracker
counter1=[]  # Lista para contar personas que bajan

personup={}  # Diccionario para personas que suben
counter2=[]  # Lista para contar personas que suben
cy1=194  # Coordenada Y de la primera línea de conteo
cy2=220  # Coordenada Y de la segunda línea de conteo
offset=12  # Margen de error para el conteo

# CSV_in={}
# CSV_in[datetime.datetime.now()]=[len(counter1)]

# Bucle principal de procesamiento
while True:
    ret, frame = cap.read()  # Lectura del frame de la cámara
    if not ret:
        break

    count+=1
    if (count%2 != 0):  # Procesar cada tercer frame para optimizar rendimiento
        continue

    frame=cv2.resize(frame, (1020,500))  # Redimensionar el frame a un tamaño fijo

    # Realizar predicción con el modelo YOLO
    results=model.predict(frame)

    # Procesar resultados de la predicción
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")

    list=[]

    # Procesar cada detección encontrada
    for index,row in px.iterrows():
        x1=int(row[0])  # Coordenada X inicial
        y1=int(row[1])  # Coordenada Y inicial
        x2=int(row[2])  # Coordenada X final
        y2=int(row[3])  # Coordenada Y final
        d=int(row[5])   # ID de la clase detectada

        c=class_list[d]
        if 'person' in c:  # Solo procesar detecciones de personas
            list.append([x1,y1,x2,y2])
    
    # Actualizar el tracker con las nuevas detecciones
    bbox_id=tracker.update(list)
    
    # Procesar cada bounding box con su ID
    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2  # Calcular centro X del bounding box
        cy=int(y3+y4)//2  # Calcular centro Y del bounding box
        cv2.circle(frame,(cx,cy),4,(255,0,255),-1)  # Dibujar punto central

        # Lógica para detectar personas que bajan
        if (cy1<(cy+offset) and (cy1>cy-offset)):
            cv2.rectangle(frame, (x3,y3),(x4,y4),(0,0,255),2)  # Dibujar rectángulo rojo
            cvzone.putTextRect(frame,f'{id}', (x3,y3), 1,2)  # Mostrar ID
            persondown[id]=(cx,cy)  # Guardar posición

        # Verificar si la persona ha cruzado la segunda línea
        if (id in persondown):
            if (cy2<(cy+offset) and (cy2>cy-offset)):
                cv2.rectangle(frame, (x3,y3),(x4,y4),(0,255,255),2)  # Dibujar rectángulo amarillo
                cvzone.putTextRect(frame,f'{id}', (x3,y3), 1,2)
                if counter1.count(id)==0:  # Evitar conteo duplicado
                    counter1.append(id)
        
        # Lógica para detectar personas que suben
        if (cy2<(cy+offset) and (cy2>cy-offset)):
            cv2.rectangle(frame, (x3,y3),(x4,y4),(0,255,0),2)  # Dibujar rectángulo verde
            cvzone.putTextRect(frame,f'{id}', (x3,y3), 1,2)
            personup[id]=(cx,cy)  # Guardar posición

        # Verificar si la persona ha cruzado la primera línea
        if (id in personup):
            if (cy1<(cy+offset) and (cy1>cy-offset)):
                cv2.rectangle(frame, (x3,y3),(x4,y4),(0,255,255),2)  # Dibujar rectángulo amarillo
                cvzone.putTextRect(frame,f'{id}', (x3,y3), 1,2)
                if counter2.count(id)==0:  # Evitar conteo duplicado
                    counter2.append(id)

    # Dibujar líneas de conteo
    cv2.line(frame,(3,cy1), (1018,cy1),(0,255,0),2)  # Línea verde
    cv2.line(frame,(5,cy2), (1019,cy2),(0,255,255),2)  # Línea amarilla

    # Calcular conteos finales
    downcount=len(counter1)  # Personas que bajan
    upcount=len(counter2)    # Personas que suben
    
    # Mostrar conteos en pantalla
    cvzone.putTextRect(frame, f'Down: {downcount}', (50,60), 2,2)
    cvzone.putTextRect(frame, f'Up: {upcount}', (50,160), 2,2)
    
    # Guardar frame en el video de salida
    output.write(frame)
    # Mostrar frame en ventana
    cv2.imshow('RGB', frame)
    
    # Salir si se presiona ESC (código 27)
    if cv2.waitKey(1) & 0xff==27:
        break

# Liberar recursos
cap.release()  # Liberar la cámara
cv2.destroyAllWindows()  # Cerrar todas las ventanas



