import serial
import time
import threading
from pynput.mouse import Controller, Listener, Button

import mss
from PIL import ImageGrab, Image
import numpy as np
import cv2
import torch 
import pathlib
import pyautogui
import sys

import os

import ctypes

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def queryMousePosition():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    position = [pt.x, pt.y]
    return position

def get_next_filename():
    index = 1
    while os.path.exists(f"video{index}.avi"):
        index += 1
    return f"video{index}.avi"

output_filename = get_next_filename()


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load(r'E:\Installers\yolov5','custom',force_reload=True,path='best.pt',source='local') 



screen_size = (600, 600)  # Change this to match your screen resolution
crop_area = (660, 240, 1260, 840)
crop_top_left = (660, 240)

fps = 30


fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)

capture_duration = 300  # Capture screen for 180 seconds
start_time_loop = time.time()


# Initialize serial port
#ser = serial.Serial('COM4', 115200)



# Create a Controller instance
mouse = Controller()

posicao = []
prev_posicao = []
cont = 0
coord = [0,0,0,0]

flagPressed = False
deltas =[0,0]

def on_click(x, y, button, pressed):
    global flagPressed
    if button == Button.right:
        if pressed:
            flagPressed = True
            #print('Left button pressed')

        else:
            flagPressed = False
            #print('Left button released')


# Define function to execute when a mouse button is clicked
'''
def on_move(x, y):

    # Get the current position of the mouse
    global posicao
    global prev_posicao
    global cont
    global coord
    global flagPressed
    global deltas
    global crop_area

    #position = mouse.position
    position = queryMousePosition()
    print("Posicao200")
    print(position)
    x1 = position[0] - crop_area[0]
    
    y1 = position[1] - crop_area[1]

    hex_x1 = hex(x1)
    hex_x_high = x1 >> 8
    hex_x_low = x1 & 0x00FF
    #print("Hexa X")
    #print(hex_x_high, hex_x_low)


    hex_y1 = hex(y1)
    hex_y_high = y1 >> 8
    hex_y_low = y1 & 0x00FF

    #print("Hexa Y")
    #print(hex_y_high, hex_y_low)
   # print("Len posicao")
   # print(len(posicao))
    posicao = [x1,y1]
    print("Posicao1")
    print(posicao)
  #  print("Prev Posicao")
  #  print(prev_posicao)
  #  print("Cont")
   # print(cont)

    
    if cont == 0:
        
        prev_posicao = posicao
       # print("Cont1")
       # print(cont)
        cont += 1
        

    elif  cont >= 1:
        #print("Cont2")
        #print(cont)
        delta_x = prev_posicao[0] - posicao[0]
        delta_y = prev_posicao[1] - posicao[1]
        cont = 0
        #print("Delta X")
        #print(delta_x)
        #print("Delta Y")
        #print(delta_y)
        #print("FlagPressed")
        #print(flagPressed)
        deltas = [delta_x,delta_y]


    

    #ser.write(hex_x_high)
    #ser.write(hex_x_low)
    #ser.write(hex_y_high)
    #ser.write(hex_y_low)
'''

    
def loop():
    cont = 0


    while True:
        if(int(time.time() - start_time_loop) < capture_duration ):
            global posicao
            global coord
            global flagPressed
            global crop_area
            # Start the timer
            start_time = time.time()


            #coord = [delta_x, delta_y]
            #print("Deltas: X, Y")
            #print(coord)
            # Capture screen content
            #screenshot = pyautogui.screenshot()

            #frame_img = Image.fromarray(np.array(screenshot))

            #cropped_frame = screenshot.crop(crop_area)

            #frame = np.array(cropped_frame)

            with mss.mss() as sct:
                monitor = {"top": 150, "left": 150, "width": 150, "height": 150}
                frame = np.array(sct.grab(monitor))




            result = model(frame)

            rl = result.xyxy[0].tolist()

            print(rl)

            if len(rl) > 0:
                for i in range(len(rl)):
                    if rl[i][4] >= .3:
                        if rl[i][5]  == 0:
                            start_point = (int(rl[0][0]), int(rl[0][1]))  
                            end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (255, 0, 0)  
                            thickness = 2
                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                        if rl[i][5]  == 1:
                            #start_point = (int(rl[0][0]), int(rl[0][1]))  
                            #end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (0, 255, 0)  
                            thickness = 2
                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                        if rl[i][5]  == 2:
                            start_point = (int(rl[0][0]), int(rl[0][1]))  
                            end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (0, 0, 255)  
                            thickness = 2

                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                        if rl[i][5]  == 3:
                            #start_point = (int(rl[0][0]), int(rl[0][1]))  
                            #end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (255, 255, 0)  
                            thickness = 2
                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                        if rl[i][5]  == 4:
                            #start_point = (int(rl[0][0]), int(rl[0][1]))  
                            #end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (0, 255, 255)  
                            thickness = 2
                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                        if rl[i][5]  == 5:
                            #start_point = (int(rl[0][0]), int(rl[0][1]))  
                            #end_point = (int(rl[0][2]), int(rl[0][3]))  
                            color = (255, 0, 255)  
                            thickness = 2
                            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)


                        if flagPressed:
                            posicao0 = 300
                            posicao1 = 300

                            #print("FlagPressed")
                            #print(flagPressed)
                            media_x = ( start_point[0] + (end_point[0] - start_point[0])//2)
                            media_y =  ( start_point[1] + (end_point[1] - start_point[1])//2)

                            frame = cv2.line(frame, (posicao0,posicao1), (media_x,media_y), (0,0,255), 2)
                            print("Media X e Y" )
                            print(media_x, media_y)

                            print("Posicao")
                            print(posicao)



                            delta_x = posicao0 - media_x
                            delta_y = posicao1 - media_y + 3

                            print("Deltas Cheat: X, Y")
                            print(delta_x,delta_y)
                            if abs(delta_x) > 255 or abs(delta_y) > 255:
                                delta_cdx = delta_x
                                delta_y = delta_y
                                print("Deltas Cheat: X1, Y1")
                                print(delta_x,delta_y)

                            #delta_x = int(delta_x * -0.3125)
                            #delta_y = int(delta_y * -0.56)

                            writeUART((delta_x),(delta_y))
            if not flagPressed:
                global deltas

               # print("DeltasMouse: X, Y")
                #print(deltas[0],deltas[1])
                #writeUART(deltas[0],deltas[1]) 


            # Convert BGR format (used by OpenCV) to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Write the frame to the video file
            out.write(frame)
            #with mss.mss() as sct:
            #    filename = sct.shot(output="output.png")
                        
            end_time = time.time()

            # Calculate the elapsed time
            elapsed_time = end_time - start_time

            print(f"The function took {elapsed_time} seconds to run.")
        else:
            sys.exit()
            break

            

            
    time.sleep(0.001)
        # Release the VideoWriter and close the OpenCV windows
    out.release()
    cv2.destroyAllWindows()
    


def writeUART(delta_x,delta_y):
    coord = [delta_x,delta_y]

    bytes_tosend = [0x00, 0x00, 0x00, 0x00]

    if coord[0] < 0:
        #print("Delta X negativo")
        bytes_tosend[1] = abs(coord[0])
        bytes_tosend[0] = 1
    else:
        bytes_tosend[1] = coord[0]
        bytes_tosend[0] = 0
    if coord[1] < 0:
        #print("Delta Y negativo")
        bytes_tosend[3] = abs(coord[1])
        bytes_tosend[2] = 1
    else:
        bytes_tosend[3] = coord[1]
        bytes_tosend[2] = 0
    print("Bytes to send")
    print(bytes_tosend)
    #ser.write(bytes_tosend)
    coord = [0,0]


#writeUART()

#threading.Thread(target=writeUART).start()

    

# Start listening for keyboard and mouse events
with Listener( on_click=on_click) as listener:
    loop()
    listener.join()


#writeUART()


