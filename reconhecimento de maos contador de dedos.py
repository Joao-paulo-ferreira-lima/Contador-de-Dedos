#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import mediapipe as mp

# vincular a webcam ao python
webcam = cv2.VideoCapture(0) # cria a conexão com a webcam (0)= indice da webcam a ser usada

# inicializando o mediapipe com modelo de reconhecimento de mãos
reconhecimento_maos = mp.solutions.hands
desenho_mp = mp.solutions.drawing_utils

# reconhecer numero de mãos, em nosso caso 1 mão
maos = reconhecimento_maos.Hands(max_num_hands=1)

# o que aconteceria se ele não tivesse conseguido conectar com a webcam
if webcam.isOpened():
    # vou ler a minha webcam (webcam.read())
    validacao, frame = webcam.read()
    # segundo problema -> entender o que é o webcam.read() -> 1 frame
    
    #temos que fazer ele pegar vários frames ENTÃO  precisamos de um loop infinito
    while validacao:
        # pegar o próximo frame da tela
        validacao, frame = webcam.read()
        
        # converte BGR (padrão do opencv) em RGB (padrão do mediapipe)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        #Salvar variaveis h e w para enumerar os pontos da mão
        h, w, _ = frame.shape
        
        # Criar lista vazia para armazenar os pontos
        pontos = []
        
        # desenhar a mão
        lista_maos = maos.process(frameRGB)
        if lista_maos.multi_hand_landmarks:
            for mao in lista_maos.multi_hand_landmarks:
                
                # Enumerar e desenhar pontos da mao
                desenho_mp.draw_landmarks(frame, mao, reconhecimento_maos.HAND_CONNECTIONS)
                for id, cord in enumerate(mao.landmark):
                    cx, cy = int(cord.x * w), int(cord.y * h)
                    
                    # exibir pontos enumerados como texto
                    cv2.putText(frame, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    pontos.append((cx,cy))
            
            # criando lista com o numero da ponta dos 4 dedos exeto polegar
            dedos = [8,12,16,20]
            
            # criando variavel contador
            contador = 0
            
            # criando a logica para o polegar
            if pontos:
                if pontos[4][0] > pontos[3][0]:
                    contador += 1
                    
                # criando a logica para os demais dedos    
                for x in dedos:
                    if pontos[x][1] < pontos[x-2][1]:
                        contador +=1
            # criando variavel quantia para o display do contador
            quantia = 'Dedos'
            if contador == 1:
                quantia = 'Dedo'
            if contador == 0:
                contador = ''
                quantia = 'Zero'
                
            # desenhando o display do contador um retangulo com o texto dentro
            cv2.rectangle(frame, (5,0), (160,40), (0,255,0), -1)
            cv2.putText(frame,f'{str(contador)} {quantia}',(20,30),cv2.FONT_HERSHEY_PLAIN,2,(139,0,0),3)
        
        # mostrar o frame da webcam que o python ta vendo
        cv2.imshow("Video da Webcam", frame)
        
        # mandar o python esperar um pouquinho -> de um jeito inteligente
        tecla = cv2.waitKey(1)
        
        # mandar ele parar o código se eu clicar no ESC
        if tecla == 27:
            break

# primeiro problema -> Se ele continua conectado na webcam
webcam.release()
cv2.destroyAllWindows()


# In[ ]:




