#################################################
# term project: MyRoom
# drawAll.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################

from utils.cmu_112_graphics import *
from utils.helperFn import *
from objectLibrary import *

'''
Initial Controller Setup
'''
def appStarted(app):
    app.image = None
    app.mode = 'drawMode'

    app.margin = 10
    app.panelWidth = 280
    app.inchPixelRatio = 3

    app.cx = -app.width
    app.cy = -app.width
    app.dragx = -app.width
    app.dragy = -app.width
    app.relx = -app.width
    app.rely = -app.width

    app.allObjects = AllObjects()
    app.accessibility = "N/A"
    app.roomLog = None

    # set panel datum
    app.x0 = app.margin
    app.x1 = app.margin*2+app.panelWidth/8
    app.x2 = 3*app.panelWidth/8
    app.x3 = app.panelWidth/2+app.margin
    app.x4 = app.margin*2+5*app.panelWidth/8
    app.x5 = 7*app.panelWidth/8
    app.x6 = app.margin+app.panelWidth

    app.y0 = app.margin
    app.y1 = 3*app.panelWidth/8+app.margin
    app.y2 = app.panelWidth/2+app.margin
    app.y3 = 5*app.panelWidth/8+app.margin
    app.y4 = 7*app.panelWidth/8-app.margin
    app.y5 = app.panelWidth-2*app.margin
    app.y6 = 10*app.panelWidth/8-4*app.margin
    app.y7 = 11*app.panelWidth/8-5*app.margin
    app.y8 = 13*app.panelWidth/8-7*app.margin
    app.y9 = 14*app.panelWidth/8-8*app.margin
    app.y10 = 16*app.panelWidth/8-10*app.margin
    app.y11 = 17*app.panelWidth/8-11*app.margin
    app.y12 = 19*app.panelWidth/8-13*app.margin

    app.y13 = 2*app.panelWidth+app.margin
    app.y14 = 33*app.panelWidth/16+app.margin
    app.y15 = app.height-app.panelWidth/16-app.margin
    app.y16 = app.height-app.margin

    # keep track of tab selection
    app.selectBldg = False
    app.selectBldgCount = 0
    app.selectFurn = False
    app.selectFurnCount = 0

    app.test = False

    # keep track of icon selection
    app.wallIconPressed = False
    app.wallIconReleased = False

    app.windowIconPressed = False
    app.windowIconReleased = False

    app.bedIconPressed = False
    app.bedIconReleased = False

    app.nistIconPressed = False
    app.nistIconReleased = False

    app.tableIconPressed = False
    app.tableIconReleased = False

    app.chairIconPressed = False
    app.chairIconReleased = False

    app.dresserIconPressed = False
    app.dresserIconReleased = False

    # keep track of object selection
    app.objSelection = None

    # load icon img
    # all img are my original work specifically for this term project
    app.drawWallIcon = app.loadImage('icons/drawWallIcon.png')
    app.drawWallIcon = app.scaleImage(app.drawWallIcon, (app.x2-app.x1)/50)
    app.windowIcon = app.loadImage('icons/windowIcon.png')
    app.windowIcon = app.scaleImage(app.windowIcon,  (app.x2-app.x1)/50)
    app.bedIcon = app.loadImage('icons/bedIcon.png')
    app.bedIcon = app.scaleImage(app.bedIcon, (app.x2-app.x1)/50)
    app.nistIcon = app.loadImage('icons/nistIcon.png')
    app.nistIcon = app.scaleImage(app.nistIcon, (app.x2-app.x1)/50)
    app.tableIcon = app.loadImage('icons/tableIcon.png')
    app.tableIcon = app.scaleImage(app.tableIcon, (app.x2-app.x1)/50)
    app.chairIcon = app.loadImage('icons/chairIcon.png')
    app.chairIcon = app.scaleImage(app.chairIcon, (app.x2-app.x1)/50)
    app.dresIcon = app.loadImage('icons/dresIcon.png')
    app.dresIcon = app.scaleImage(app.dresIcon, (app.x2-app.x1)/50)

def drawMode_mousePressed(app, event):
    # reset drag x&y
    app.dragx = -app.width
    app.dragy = -app.width
    # initiate
    app.cx = event.x
    app.cy = event.y

    # check tabs
    ifBldgTabPressed(app)
    ifFurnTabPressed(app)
    ifTestTabPressed(app)

    # check icons
    whichIconPressed(app)

    # check placed objects
    app.objSelection = app.allObjects.checkSelection(app.cx, app.cy)

def drawMode_mouseDragged(app, event):
    app.dragx = event.x
    app.dragy = event.y

def drawMode_mouseReleased(app, event):
    app.relx = event.x
    app.rely = event.y

    if app.wallIconPressed: 
        app.wallIconPressed = False
        app.wallIconReleased = True
    placeWall(app)

    if app.windowIconPressed: 
        app.windowIconPressed = False
        app.windowIconReleased = True
    placeWindow(app)

    if app.bedIconPressed: 
        app.bedIconPressed = False
        app.bedIconReleased = True
    placeBed(app)

    if app.nistIconPressed: 
        app.nistIconPressed = False
        app.nistIconReleased = True
    placeNist(app)

    if app.tableIconPressed: 
        app.tableIconPressed = False
        app.tableIconReleased = True
    placeTable(app)

    if app.chairIconPressed: 
        app.chairIconPressed = False
        app.chairIconReleased = True
    placeChair(app)

    if app.dresserIconPressed: 
        app.dresserIconPressed = False
        app.dresserIconReleased = True
    placeDresser(app)

def drawMode_keyPressed(app, event):
    if event.key == "r": appStarted(app)
    if event.key == "p": 
        print(app.allObjects.wallDict)
        print(app.allObjects.furnDict)
    
    # move selected object
    if event.key == "Up" and app.objSelection != None: 
        app.allObjects.moveSelection("Up", app.objSelection)
    if event.key == "Down" and app.objSelection != None: 
        app.allObjects.moveSelection("Down", app.objSelection)
    if event.key == "Left" and app.objSelection != None: 
        app.allObjects.moveSelection("Left", app.objSelection)
    if event.key == "Right" and app.objSelection != None: 
        app.allObjects.moveSelection("Right", app.objSelection)

    # delete selected object
    if event.key == "BackSpace" and app.objSelection != None: 
        app.allObjects.deleteSelection(app.objSelection)

    # rotate selected object
    if event.key == "Space" and app.objSelection != None: 
        app.allObjects.rotateSelection(app.objSelection)

def whichIconPressed(app):
    # only allow one room in the drawing space:
    if app.allObjects.wall == None and app.selectBldg:
        if (app.cx > app.x1 and app.cx < app.x2 \
            and app.cy > app.y3 and app.cy < app.y4):
            app.wallIconPressed = True
    
    # only enable other icons when there's a room
    # window
    if app.allObjects.wall != None and app.selectBldg:
        if (app.cx > app.x1 and app.cx < app.x2 \
            and app.cy > app.y5 and app.cy < app.y6):
            app.windowIconPressed = True

    # furniture
    if app.allObjects.wall != None and app.selectFurn:
        if (app.cx > app.x4 and app.cx < app.x5 \
            and app.cy > app.y3 and app.cy < app.y4):
            app.bedIconPressed = True

        if (app.cx > app.x4 and app.cx < app.x5 \
            and app.cy > app.y5 and app.cy < app.y6):
            app.nistIconPressed = True

        if (app.cx > app.x4 and app.cx < app.x5 \
            and app.cy > app.y7 and app.cy < app.y8):
            app.tableIconPressed = True

        if (app.cx > app.x4 and app.cx < app.x5 \
            and app.cy > app.y9 and app.cy < app.y10):
            app.chairIconPressed = True

        if (app.cx > app.x4 and app.cx < app.x5 \
            and app.cy > app.y11 and app.cy < app.y12):
            app.dresserIconPressed = True

def ifBldgTabPressed(app):
    if (app.cx > app.x0 and app.cx < app.x3 \
        and app.cy > app.y1 and app.cy < app.y2):
        app.selectBldg = True
        app.selectBldgCount += 1
        # reset the furn tab
        app.selectFurn = False
        app.selectFurnCount = 0
        # click again to reset selection
        if app.selectBldgCount > 1 or app.selectFurn == True: 
            app.selectBldgCount = 0
            app.selectBldg = False

def ifFurnTabPressed(app):
    if (app.cx > app.x3 and app.cx < app.x6 \
        and app.cy > app.y1 and app.cy < app.y2):
        app.selectFurn = True
        app.selectFurnCount += 1
        # reset the bldg tab
        app.selectBldg = False
        app.selectBldgCount = 0
        # click again to reset selection
        if app.selectFurnCount > 1 or app.selectBldg == True: 
            app.selectFurnCount = 0
            app.selectFurn = False

def ifTestTabPressed(app):
    # only allow test when there is a room
    if app.allObjects.wall != None and (app.cx > app.x0 and app.cx < app.x6 \
                                    and app.cy > app.y15 and app.cy < app.y16):
        print("testMode")
        app.mode = "testMode"  

            

'''
Draw Mode User Interface
'''
def drawBG(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='floral white', width=0)

    # draw drawing space
    drawDrawingSpace(app, canvas)
    
    # draw panel
    drawPanel(app, canvas)

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
    
def drawPanel(app, canvas):
    # draw panel bg
    canvas.create_rectangle(app.margin, app.margin, app.panelWidth+app.margin, 
                            app.height-app.margin, fill='white', width=0)
    # draw title
    # alt font=('HanziPen SC', 48)
    canvas.create_text(app.x3, 3*(app.y1-app.y0)/5, 
                       fill='black', text='MyRoom', 
                       font=('Nanum Pen Script', 60))
    # draw tabs
    drawBldgTab(app, canvas)
    drawFurnTab(app, canvas)
    drawTestTab(app, canvas)
    drawInstructionTab(app, canvas)

    canvas.create_rectangle(app.margin, app.margin, app.panelWidth+app.margin, 
                            app.height-app.margin, width=3)

def drawBldgTab(app, canvas):
    if app.selectBldg: 
        bgFill, textFill = 'black', 'white'
        
        canvas.create_text((app.x1+app.x2)/2, (app.y2+app.y3)/2, 
                            fill='black',text='Drag & Drop',font=('Roboto', 16))
        # walls
        canvas.create_image((app.x1+app.x2)/2, (app.y3+app.y4)/2,
                            image=ImageTk.PhotoImage(app.drawWallIcon))
        canvas.create_rectangle(app.x1, app.y3, app.x2, app.y4,
                                outline='grey80')
        canvas.create_text((app.x1+app.x2)/2, app.y4+2*(app.y5-app.y4)/5, 
                            fill='grey50', text='Walls', font=('Roboto', 12))
        # windows
        canvas.create_image((app.x1+app.x2)/2, (app.y5+app.y6)/2,
                             image=ImageTk.PhotoImage(app.windowIcon))
        canvas.create_rectangle(app.x1, app.y5, app.x2, app.y6,
                                outline='grey80')
        canvas.create_text((app.x1+app.x2)/2, app.y6+2*(app.y7-app.y6)/5,
                            fill='grey50', text='Window', font=('Roboto', 12))
    
    else: bgFill, textFill = 'white', 'black'
    canvas.create_rectangle(app.x0, app.y1, app.x3, app.y2, fill=bgFill)
    canvas.create_text((app.x1+app.x2)/2, (app.y1+app.y2)/2, 
                       fill=textFill, text='Building', font=('Roboto', 21))
    
def drawFurnTab(app, canvas):
    if app.selectFurn: 
        bgFill, textFill = 'black', 'white'
  
        canvas.create_text((app.x4+app.x5)/2, (app.y2+app.y3)/2, 
                           fill='black', text='Drag & Drop', 
                           font=('Roboto', 16))
        # bed icon
        canvas.create_image((app.x4+app.x5)/2, (app.y3+app.y4)/2,
                             image=ImageTk.PhotoImage(app.bedIcon))
        canvas.create_rectangle(app.x4, app.y3, app.x5, app.y4,
                                outline='grey80')
        canvas.create_text((app.x4+app.x5)/2, app.y4+2*(app.y5-app.y4)/5,
                            fill='grey50', text='Bed', font=('Roboto', 12))
        # night stand icon
        canvas.create_image((app.x4+app.x5)/2, (app.y5+app.y6)/2,
                            image=ImageTk.PhotoImage(app.nistIcon))
        canvas.create_rectangle(app.x4, app.y5, app.x5, app.y6,
                                outline='grey80')
        canvas.create_text((app.x4+app.x5)/2, app.y6+2*(app.y7-app.y6)/5,
                            fill='grey50',text='Nightstand',font=('Roboto', 12))
        # table icon
        canvas.create_image((app.x4+app.x5)/2, (app.y7+app.y8)/2,
                            image=ImageTk.PhotoImage(app.tableIcon))
        canvas.create_rectangle(app.x4, app.y7, app.x5, app.y8,
                                outline='grey80')
        canvas.create_text((app.x4+app.x5)/2, app.y8+2*(app.y9-app.y8)/5,
                            fill='grey50', text='Table', font=('Roboto', 12))
        # chair icon
        canvas.create_image((app.x4+app.x5)/2, (app.y9+app.y10)/2,
                            image=ImageTk.PhotoImage(app.chairIcon))
        canvas.create_rectangle(app.x4, app.y9, app.x5, app.y10,
                                outline='grey80')
        canvas.create_text((app.x4+app.x5)/2, app.y10+2*(app.y11-app.y10)/5,
                            fill='grey50', text='Chair', font=('Roboto', 12))
        # dresser icon
        canvas.create_image((app.x4+app.x5)/2, (app.y11+app.y12)/2,
                            image=ImageTk.PhotoImage(app.dresIcon))
        canvas.create_rectangle(app.x4, app.y11, app.x5, app.y12,
                                outline='grey80')
        canvas.create_text((app.x4+app.x5)/2, app.y12+2*(app.y11-app.y10)/5,
                            fill='grey50', text='Dresser', font=('Roboto', 12))
        
    else: bgFill, textFill = 'white', 'black'
    canvas.create_rectangle(app.x3, app.y1, app.x6, app.y2, fill=bgFill)
    canvas.create_text((app.x4+app.x5)/2, (app.y1+app.y2)/2, 
                       fill=textFill, text='Furniture', font=('Roboto', 21))

def drawInstructionTab(app, canvas):
    canvas.create_rectangle(app.x0, app.y13, app.x6, app.y14, fill='white')
    canvas.create_text(app.x3, (app.y13+app.y14)/2, 
                       fill='black', text='Instruction', font=('Roboto', 16))

    canvas.create_text(app.x3, (app.y14+app.y15)/2, 
                       text='1. To start, choose Building tab, drag and drop walls into the drawing space\n\
2. Click on the object you want to modify, use the arrow keys to move, space to rotate, backspace to delete, Press "R" to restart\n\
Note: You cannot manipulate objects to collide with existing or go outside the room', 
                       justify='center', width = (app.x6-app.x0-app.margin), 
                       font=('Roboto', 11))

def drawTestTab(app, canvas):
    canvas.create_rectangle(app.x0, app.y15, app.x6, app.y16, fill='white')
    canvas.create_text(app.x3, (app.y15+app.y16)/2, fill='black', text='Test', 
                       font=('Roboto', 12))
   
def drawDrawingSpace(app, canvas):
    
    gridGap = 12*app.inchPixelRatio
    vertGridX = 0
    horiGridY = 0
    while vertGridX < app.width - app.margin:
        canvas.create_line(vertGridX, 0,
                           vertGridX, app.height,
                           fill='grey90', width=1)
        vertGridX += gridGap
    while horiGridY < app.height - app.margin:
        canvas.create_line(0, horiGridY,
                           app.width, horiGridY,
                           fill='grey80', width=1)
        horiGridY += gridGap


'''
Draw Drag Motion
'''
def drawDragIcon(app, canvas):
    drawDragWall(app, canvas)
    drawDragWindow(app, canvas)
    drawDragBed(app, canvas)
    drawDragNist(app, canvas)
    drawDragTable(app, canvas)
    drawDragChair(app, canvas)
    drawDragDresser(app, canvas)

def drawDragWall(app, canvas):
    if app.wallIconPressed:
        tempWall = Wall(app.dragx, app.dragy)
        tempWall.draw(canvas)

def drawDragWindow(app, canvas):
    if app.windowIconPressed:
        tempWindow = Window(app.dragx, app.dragy)
        tempWindow.draw(canvas)

def drawDragBed(app, canvas):
    if app.bedIconPressed:
        tempBed = Bed(app.dragx, app.dragy)
        tempBed.draw(canvas)

def drawDragNist(app, canvas):
    if app.nistIconPressed:
        tempNist = Nist(app.dragx, app.dragy)
        tempNist.draw(canvas)

def drawDragTable(app, canvas):
    if app.tableIconPressed:
        tempTable = Table(app.dragx, app.dragy)
        tempTable.draw(canvas)

def drawDragChair(app, canvas):
    if app.chairIconPressed:
        tempChair = Chair(app.dragx, app.dragy)
        tempChair.draw(canvas)

def drawDragDresser(app, canvas):
    if app.dresserIconPressed:
        tempDresser = Dresser(app.dragx, app.dragy)
        tempDresser.draw(canvas)


'''
Place Objects
'''
def ifWallInDrawingSpace(app, wall):
    if (wall.leftx > app.margin+app.panelWidth+24*app.inchPixelRatio and wall.rightx < app.width-app.margin
        and wall.topy > app.margin+12*app.inchPixelRatio and wall.boty < app.height-app.margin):
        return True
    return False

def drawPlacedObjects(app, canvas):
    if app.allObjects.wall != None:
        app.allObjects.wall.draw(canvas)
        for ls in app.allObjects.wallDict.values():
                for obj in ls:
                    obj.draw(canvas)
    for furnList in app.allObjects.furnDict.values():
        for furn in furnList:
            furn.draw(canvas)

def placeWall(app):
    if app.wallIconReleased:
        newWall = Wall(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        newDoor = Door(newWall.leftx+newWall.x/4, newWall.boty, 
                         inchPixelRatio=newWall.inchPixelRatio)
        if (ifWallInDrawingSpace(app, newWall)):
            app.allObjects.addWall(newWall)
            app.allObjects.addDoor(newDoor)
            app.allObjects.wall.door = newDoor
        app.wallIconReleased = False

def placeWindow(app):
    if app.windowIconReleased:
        lx = app.allObjects.wall.leftx
        rx = app.allObjects.wall.rightx
        ty = app.allObjects.wall.topy
        by = app.allObjects.wall.boty
        cx = roundNearestInch(app.relx, app.inchPixelRatio)
        cy = roundNearestInch(app.rely, app.inchPixelRatio)

        newWindow = None
        if almostEqual(cx, lx) and cy > ty+21*app.inchPixelRatio and cy < by-21*app.inchPixelRatio:
            host = "wall2"
            newWindow = Window(lx, cy, host=host)
        if almostEqual(cx, rx) and cy > ty+21*app.inchPixelRatio and cy < by-21*app.inchPixelRatio:
            host = "wall0"
            newWindow = Window(rx, cy, host=host)
        if almostEqual(cy, ty) and cx > lx+21*app.inchPixelRatio and cx < rx-21*app.inchPixelRatio:
            host = "wall1"
            newWindow = Window(cx, ty, host=host)
        if almostEqual(cy, by) and cx > lx+21*app.inchPixelRatio and cx < rx-21*app.inchPixelRatio:
            host = "wall3"
            newWindow = Window(cx, by, host=host)

        if newWindow!= None and not app.allObjects.ifCollideExisting(newWindow):
            app.allObjects.addWindow(newWindow)

        app.windowIconReleased = False

def placeBed(app):
    if app.bedIconReleased:
        newBed = Bed(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        if (app.allObjects.ifFurnInRoom(newBed) 
            and not app.allObjects.ifCollideExisting(newBed)):
            app.allObjects.addBed(newBed)
        app.bedIconReleased = False

def placeNist(app):
    if app.nistIconReleased:
        newNist = Nist(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        if (app.allObjects.ifFurnInRoom(newNist)
            and not app.allObjects.ifCollideExisting(newNist)):
            app.allObjects.addNist(newNist)
        app.nistIconReleased = False

def placeTable(app):
    if app.tableIconReleased:
        newTable = Table(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        if (app.allObjects.ifFurnInRoom(newTable)
            and not app.allObjects.ifCollideExisting(newTable)):
            app.allObjects.addTable(newTable)
        app.tableIconReleased = False

def placeChair(app):
    if app.chairIconReleased:
        newChair = Chair(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        if (app.allObjects.ifFurnInRoom(newChair)
            and not app.allObjects.ifCollideExisting(newChair)):
            app.allObjects.addChair(newChair)
        app.chairIconReleased = False

def placeDresser(app):
    if app.dresserIconReleased:
        newDresser = Dresser(roundNearestInch(app.relx, app.inchPixelRatio), 
                       roundNearestInch(app.rely, app.inchPixelRatio), 
                       inchPixelRatio=app.inchPixelRatio)
        if (app.allObjects.ifFurnInRoom(newDresser)
            and not app.allObjects.ifCollideExisting(newDresser)):
            app.allObjects.addDresser(newDresser)
        app.dresserIconReleased = False


'''
Outline Selected Objects
'''
def drawOutlineSelection(app, canvas):
    if app.objSelection != None:
        app.allObjects.outlineSelection(app.objSelection, canvas)
        