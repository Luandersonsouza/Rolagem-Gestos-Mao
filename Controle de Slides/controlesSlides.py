import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

video = cv2.VideoCapture(0)

video.set(3,1280)
video.set(4,720)


kb = Controller()


detector = HandDetector(detectionCon=0.8)
estadoAtual = [0,0,0,0,0]

while True:
    _, img = video.read()
    hands, img = detector.findHands(img)
 
    if hands:
        estado = detector.fingersUp(hands[0])
        #print(estado)

        if estado != estadoAtual and estado == [0,1,0,0,0]:
            print("Passando slide")
            kb.press(Key.right)
            kb.release(Key.right)

        if estado != estadoAtual and estado == [1,0,0,0,0]:
            print("Voltando slide")
            kb.press(Key.left)
            kb.release(Key.left)

        if estado == estadoAtual and estado == [0,1,0,0,0]:
            print('Slide avançado')        

        
        if estado == estadoAtual and estado == [1,0,0,0,0]:
            print('Slide retrocedido') 

        
        estadoAtual = estado
        
    cv2.imshow('img', cv2.resize(img,(640, 420)))
    if cv2.waitKey(1) & 0xFF == 27:  
        break