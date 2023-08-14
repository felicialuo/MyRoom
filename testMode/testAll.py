#################################################
# term project: MyRoom
# testAll.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################

from utils.cmu_112_graphics import *
from objectLibrary import *
from drawAll import *
from agent import *
import numpy as np
import time


def testMode_mousePressed(app, event):
    if (event.x > app.x0 and event.x < app.x3 and \
        event.y > app.y15 and event.y < app.y16):
        print("start test")
        runTest(app)
        
    if (event.x > app.x3 and event.x < app.x6 and \
        event.y > app.y15 and event.y < app.y16):
        print("drawMode")
        app.mode = "drawMode"
        # reset
        app.accessibility = "N/A"
        app.roomLog = None



'''
Test Mode User Interface
'''
def testBG(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='white', width=0)
    # draw drawing space
    drawDrawingSpace(app, canvas)
    
    # draw panel
    testPanel(app, canvas)

    # draw view frame
    canvas.create_rectangle(0,0,app.width, app.margin, fill='white', width=0)
    canvas.create_rectangle(0,0,app.margin, app.height, fill='white', width=0)
    canvas.create_rectangle(app.width-app.margin, 0, app.width, app.height, 
                            fill='white', width=0)
    canvas.create_rectangle(0, app.height-app.margin, app.width, app.height,
                            fill='white', width=0)
    canvas.create_rectangle(app.margin,app.margin,
                            app.width-app.margin,app.height-app.margin, 
                            outline='black', width=5)

def testPanel(app, canvas):
    # draw panel bg
    canvas.create_rectangle(app.margin, app.margin, app.panelWidth+app.margin, 
                            app.height-app.margin, fill='white', width=0)
    # draw title
    # alt font=('HanziPen SC', 48)
    canvas.create_text(app.x3, 3*(app.y1-app.y0)/5, 
                       fill='black', text='MyRoom', 
                       font=('Nanum Pen Script', 60))
    # draw tabs
    canvas.create_rectangle(app.x0, app.y1, app.x6, app.y2, fill='black')
    canvas.create_text((app.x0+app.x6)/2, (app.y1+app.y2)/2, 
                       fill='white', text='Test Mode', font=('Roboto', 21))
    # draw instruction
    # canvas.create_text(app.x3, (app.y13+app.y14)/2--app.panelWidth, 
    #                    fill='black', text='Note', font=('Roboto', 16))
    # canvas.create_rectangle(app.x0, app.y13-app.panelWidth, app.x6, 
    #                         app.y14-app.panelWidth, fill='')
    canvas.create_text(app.x3, app.cy/2, 
                       text='Grey represents inaccessible area. \n\
Accessible rate = accessible area / open area * 100% \n\
Hint: Make sure you have 18" clearance to walk through!', 
                       justify='center', width = (app.x5-app.x1), 
                       font=('Roboto', 11))

    # draw start tab
    canvas.create_rectangle(app.x0, app.y15, app.x3, app.y16, fill='white')
    canvas.create_text((app.x0+app.x3)/2, (app.y15+app.y16)/2, 
                       fill='black', text='Start', font=('Roboto', 12))
    # draw exit tab
    canvas.create_rectangle(app.x3, app.y15, app.x6, app.y16, fill='white')
    canvas.create_text((app.x3+app.x6)/2, (app.y15+app.y16)/2, 
                       fill='black', text='Exit', font=('Roboto', 12))

    # panel frame
    canvas.create_rectangle(app.margin, app.margin, app.panelWidth+app.margin, 
                            app.height-app.margin, width=3)

def drawAcsRate(app, canvas):
    canvas.create_text(app.x3, (app.y13-app.y2)/2, fill='red', 
                       text=f"You accessible rate is {app.accessibility}", 
                       font=('Roboto', 16), justify='center', 
                       width = (app.x6-app.x0-app.margin))



'''
Run Test
'''
def runTest(app):
    room = getRoomArr(app)

    start_x = int((app.allObjects.wall.door.cx - app.allObjects.wall.leftx) 
                    / app.inchPixelRatio)
    start_y = int(room.shape[0] - 
                    ((app.allObjects.wall.boty - app.allObjects.wall.door.cy) 
                    / app.inchPixelRatio)-1)
    start_dir = app.allObjects.wall.door.direction
    start_node = Node(start_x,start_y,start_dir)

    # CITATION: following BFS implementation (until calculating open_area)
    # from https://github.com/dungba88/cleaner_robot
    total_elapsed_bfs = 0
    total_steps_bfs = 0
    total_turns_bfs = 0

    # run with bfs
    agent = Agent(room, start_node)
    sweeper = Sweeper(agent)
    agent.loggable = False
    agent.clr = 15

    start = time.time()
    sweeper.sweep()
    elapsed = time.time() - start

    total_elapsed_bfs += elapsed
    total_steps_bfs += agent.move_count
    total_turns_bfs += agent.turn_count

    print('steps taken by planned bfs: %d, turns taken: %d, time taken: %.2fms'
            % (agent.move_count, agent.turn_count, elapsed * 1000))
    agent.log()

    open_area = (room.shape[0]*room.shape[1]) - abs(np.sum(room))
    app.accessibility = np.sum(agent.roomLog - room) / open_area * 100
    app.accessibility = "{:.2f}%".format(app.accessibility)
    print(f"Accessible rate is {app.accessibility}")

    app.roomLog = agent.roomLog

def getRoomArr(app):
    dim_x = app.allObjects.wall.x // app.inchPixelRatio
    dim_y = app.allObjects.wall.y // app.inchPixelRatio
    room = np.zeros([dim_y, dim_x])
    for furnList in app.allObjects.furnDict.values():
            for furn in furnList:
                arr_leftx = int((furn.leftx - app.allObjects.wall.leftx) / app.inchPixelRatio)
                arr_rightx = int((furn.rightx - app.allObjects.wall.leftx) / app.inchPixelRatio)
                arr_topy = int(dim_y - ((app.allObjects.wall.boty - furn.topy) / app.inchPixelRatio))
                arr_boty = int(dim_y - ((app.allObjects.wall.boty - furn.boty) / app.inchPixelRatio))
                room[arr_topy : arr_boty, arr_leftx : arr_rightx] = -1

    # print initial room array
    for i in range(room.shape[0]):
        text = ""
        for j in range(room.shape[1]):
            if room[i, j] == 0:
                text += '.'
            else:
                text += '|'
        print(text)
        print('')
    return room


'''
Draw Agent Log
'''
def drawRoomLog(app, canvas):
    if app.accessibility != "N/A":
        for i in range(app.roomLog.shape[0]):
            for j in range(app.roomLog.shape[1]):
                if app.roomLog[i, j] == 0:
                    canvas.create_rectangle(app.allObjects.wall.leftx+j*app.inchPixelRatio,
                            app.allObjects.wall.topy+i*app.inchPixelRatio,
                            app.allObjects.wall.leftx+(j+1)*app.inchPixelRatio,
                            app.allObjects.wall.topy+(i+1)*app.inchPixelRatio,
                            fill='grey80', width=0)
