# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 19:17:17 2019

@author: ANKUR


"""
import threading
import cv2
import numpy as np
import time
import random
p=0
def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

    CELL_SIZE=20
    found=0
    global img
    startx,starty=initial_point
    goalx,goaly=final_point
    a=original_binary_img
    visited=np.zeros((no_cells_height,no_cells_width))
    queue=[]
    parent=[[0 for i in range(no_cells_height)] for j in range(no_cells_width)]
    visited[startx][starty]=1
    queue.append((startx,starty))
    while(len(queue)!=0):
      y,x=queue.pop(0)#down
      temp=a[y*CELL_SIZE:y*CELL_SIZE+CELL_SIZE,(x)*CELL_SIZE:(x)*CELL_SIZE+CELL_SIZE]
      r = random.randint(0,255)
      g = random.randint(0,255)
      b = random.randint(0,255)
      rgb = (r,g,b)
      if(y+1>=0 and y+1<=goalx and x>=0 and x<=goaly and visited[y+1][x]==0 and (255 in temp[-1,:])):
            visited[y+1][x]=1
            queue.append((y+1,x))
            parent[y+1][x]=(y,x)
            cv2.rectangle(img,(x*20+3,(y+1)*20+3),(x*20-3+20,(y+1)*20-3+20),(128,128,128),-1)
      time.sleep(0.015)      
      if(y-1>=0 and y-1<=goalx and x>=0 and x<=goaly and visited[y-1][x]==0 and (255 in temp[0,:])):
            visited[y-1][x]=1
            queue.append((y-1,x))
            parent[y-1][x]=(y,x)
            cv2.rectangle(img,(x*20+3,(y-1)*20+3),(x*20-3+20,(y-1)*20-3+20),(128,128,128),-1)
      time.sleep(0.015)        
      if(x+1>=0 and x+1<=goaly and y>=0 and y<=goalx and visited[y][x+1]==0 and (255 in temp[:,-1])):
            visited[y][x+1]=1
            queue.append((y,x+1))
            parent[y][x+1]=(y,x)
            cv2.rectangle(img,((x+1)*20+3,(y)*20+3),((x+1)*20-3+20,(y)*20-3+20),(128,128,128),-1)
      time.sleep(0.015)        
      if(x-1>=0 and x-1<=goaly and y>=0 and y<=goalx and visited[y][x-1]==0 and (255 in temp[:,0])):
            visited[y][x-1]=1
            queue.append((y,x-1))
            parent[y][x-1]=(y,x)
            cv2.rectangle(img,((x-1)*20+3,(y)*20+3),((x-1)*20-3+20,(y)*20-3+20),(128,128,128),-1)
      time.sleep(0.015)         

      if(visited[goalx][goaly]==1):
          found=1
          break
    shortestPath=[]
    shortestPath.append((goalx,goaly))
    i=0
    if found==1:
        while(1):
            goalx,goaly=shortestPath[i]
            cv2.rectangle(img,((goaly)*20+2,(goalx)*20+2),((goaly)*20-2+20,(goalx)*20-2+20),(255,128,0),-1)
            time.sleep(0.005)  
            if(parent[goalx][goaly]==(startx,starty)):
                break
            shortestPath.append(parent[goalx][goaly])
            i+=1
        shortestPath.append((startx,starty))
        cv2.rectangle(img,((startx)*20+3,(starty)*20+3),((startx)*20-3+20,(starty)*20-3+20),(255,128,0),-1)
        shortestPath.reverse()
    else:
      print("Path Not found")        
    return shortestPath


def mouse_event(event, pX, pY, flags, param):

    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (pX - 2, pY - 2),
                          (pX + 2, pY + 2), (0, 0, 255), -1)
            start = pY//20, pX//20
            print("start = ", start)
            p += 1
        elif p == 1:
            cv2.rectangle(img, (pX - 2, pY - 2),
                          (pX + 2, pY + 2), (0, 200, 50), -1)
            end = (pY//20, pX//20)
            print("end = ", end)
            p += 1        
def disp():
    global img
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouse_event)
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
        
img=cv2.imread('./maze04.jpg')
a=cv2.imread('./maze04.jpg',0)
_,binary_img=cv2.threshold(img,128,255,cv2.THRESH_BINARY)
        
        
        
t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()
while p<2:
    pass
z=solveMaze(binary_img, start, end, img.shape[0]//20, img.shape[0]//20)
print(z)
cv2.waitKey(0)
