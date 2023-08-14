#################################################
# term project: MyRoom
# implementation.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################

from utils.cmu_112_graphics import *
from utils.helperFn import *
from objectLibrary import *
from drawAll import *
from testMode.testAll import *


def drawMode_redrawAll(app, canvas):
    drawBG(app, canvas)
    drawPlacedObjects(app, canvas)
    drawOutlineSelection(app, canvas)
    drawDragIcon(app, canvas)

def testMode_redrawAll(app, canvas):
    testBG(app, canvas)
    
    drawAcsRate(app, canvas)
    drawRoomLog(app, canvas)
    drawPlacedObjects(app, canvas)

def startMyRoom():
    runApp(width=1280, height=720)


def main():
    startMyRoom()

if __name__ == '__main__':
    main()
