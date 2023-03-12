#Importing Dependencies
import numpy as np
import cv2
import matplotlib.pyplot as plt
#Creating Workspace
workspace = np.zeros((250,600),dtype=np.float64)
workspace[workspace==0] = 1e+50
rect_1=np.array([[95,0],
                 [95,105],
                 [155,105],
                 [155,0]]) 
cv2.fillPoly(workspace,[rect_1],color =-1)              #rectangle

rect_2=np.array([[95,250],
                 [95,145],
                 [155,145],
                 [155,250]])
cv2.fillPoly(workspace,[rect_2],color =-1)              #rectangle

hexapt= np.array([[300,50],
                 [354,88],
                 [354,162],
                 [300,200],
                 [247,162],
                 [247,88]])
hexapt=hexapt.reshape(-1,1,2)
cv2.fillPoly(workspace,[hexapt],color =-1)              #polygon

triapt=np.array([[460,25],
                 [460,225],
                 [510,125]])
cv2.fillPoly(workspace,[triapt],color = -1)             #triangle
#Validating node
def valid(node, list, array):                            
    pad = 5 # Pad of 5mm on boundary
    if  node not in list and 0 +pad <= node[0] < 250-pad and 0 +pad <= node[1] < 600-pad and array[node] > 0:
        return True
    else:
        return False

def Reverse(list):
    return [ele for ele in reversed(list)]
#Movement in 8 directions
def move(node, direction):
    x,y= node
    if direction==0:
        x=x+1
        y=y
    elif direction==1:
        x=x+1
        y=y+1
    elif direction==2:
        x=x-1
        y=y
    elif direction==3:
        x=x-1
        y=y-1
    elif direction==4:
        x=x
        y=y+1
    elif direction==5:
        x=x-1
        y=y+1
    elif direction==6:
        x=x
        y=y-1
    elif direction==7:
        x=x+1
        y=y-1
    return (x,y)

# Creating a Problem Array #
display = np.zeros((workspace.shape[0],workspace.shape[1],3))
display[:,:,2] = workspace.copy()
display[:,:,2][workspace == -1] = 255   #Displaying Obstacles
display = display.astype(np.uint8)
flag = False


Openlist = {}
Closedlist = []
parent = {}

# User Input #
while flag == False:
    xs = int(input("Enter X value of Starting node "))
    ys = int(input("Enter Y value of Starting node "))
    xg = int(input("Enter X value of Goal node "))
    yg = int(input("Enter Y value of Goal node "))
    start = (ys,xs)
    goal = (yg,xg)
    if valid(start, Closedlist, workspace) and valid(goal, Closedlist, workspace) and start != goal:
        flag = True
    else:
        print("Invalid value, please try again\n")


Openlist[start] = 0
workspace[start] = 0
Closedlist.append(start)
node = start

#Initializing video
out = cv2.VideoWriter('Project2.avi',cv2.VideoWriter_fourcc(*'DIVX'),400,(display.shape[1], display.shape[0]))
#Djikstra Algorithm
while node != goal:
    Openlist = dict(sorted(Openlist.items(), key=lambda item: item[1]))
    node = list(Openlist.keys())[0]
    Openlist.pop(node)
    Closedlist.append(node)
    cost = 0
    for directory in range(8):
        if directory % 2 == 0:
            cost= 1
        else:
            cost= 1.4
        temp = move(node, directory)
        if valid(temp, Closedlist, workspace):
            if temp not in Openlist or workspace[temp] > np.exp(10):
                parent[temp] = node
                workspace[temp] = workspace[node]+cost
                Openlist[temp] = workspace[temp]
            elif workspace[temp] > workspace[node]+cost:
                parent[temp] = node
                workspace[temp] = workspace[node]+cost
        else:
            continue
        
    display[:,:,0][node] = 255
    cv2.imshow("Djikstra Visualization", np.flipud(display))
    cv2.waitKey(1)
    out.write(np.flipud(display))
#Backtracking
node = goal
path = []
while start not in path:    
    node = parent.pop(node)
    path.append(node)
print("Total nodes : ", len(path))
path = Reverse(path)
for n in path:
    display[:,:,1][n] = 255
    out.write(np.flipud(display))
cv2.imshow("Djikstra Visualization", np.flipud(display))
cv2.waitKey(0)
out.release()