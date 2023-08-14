#################################################
# term project: MyRoom
# objectLibrary.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################


from utils.cmu_112_graphics import *
from utils.helperFn import *

# for all directions: 0 - 0 degree(right), 1 - 90 degree (top), 
#                     2 - 180 degree (left), 3 - 270 degree (bottom)

class AllObjects():
    def __init__(self, inchPixelRatio=3):
        self.inchPixelRatio = inchPixelRatio
        self.wall = None
        self.furnDict = {'beds':[], 'nightstands':[], 'tables':[], \
                         'chairs':[], 'dressers':[]}
        self.wallDict = {'wall0':[], 'wall1':[], 'wall2':[], 'wall3':[]}

    def addWall(self, wall):
        self.wall = wall
        print("Wall added")

    def addDoor(self, door):
        self.wallDict[door.host].append(door)
        print("Door added")

    def addWindow(self, window):
        self.wallDict[window.host].append(window)
        print("Window added")

    def addBed(self, bed):
        self.furnDict['beds'].append(bed)
        print("Bed added")

    def addNist(self, nist):
        self.furnDict['nightstands'].append(nist)
        print("Nightstand added")

    def addTable(self, table):
        self.furnDict['tables'].append(table)
        print("Table added")

    def addChair(self, chair):
        self.furnDict['chairs'].append(chair)
        print("Chair added")

    def addDresser(self, dresser):
        self.furnDict['dressers'].append(dresser)
        print("Dresser added")
    
    def checkSelection(self, cx, cy):
        # check wall
        if self.wall != None:
            if almostEqual(cx, self.wall.leftx) and cy > self.wall.topy and cy < self.wall.boty:
                for obj in self.wallDict['wall2']:
                    if almostEqual(cy, obj.cy): return obj
                return "wall2"
            if almostEqual(cx, self.wall.rightx) and cy > self.wall.topy and cy < self.wall.boty:
                for obj in self.wallDict['wall0']:
                    if almostEqual(cy, obj.cy): return obj
                return "wall0"
            if almostEqual(cy, self.wall.topy) and cx > self.wall.leftx and cx < self.wall.rightx:
                for obj in self.wallDict['wall1']:
                    if almostEqual(cx, obj.cx): return obj
                return "wall1"
            if almostEqual(cy, self.wall.boty) and cx > self.wall.leftx and cx < self.wall.rightx:
                for obj in self.wallDict['wall3']:
                    if almostEqual(cx, obj.cx): return obj
                return "wall3"

        # check furniture
        for furnList in self.furnDict.values():
            for furn in furnList:
                if (cx > furn.leftx and cx < furn.rightx \
                    and cy > furn.topy and cy < furn.boty): return furn
        
        return None
    
    def outlineSelection(self, obj, canvas):
        # for wall
        if obj == "wall2":
            canvas.create_line(self.wall.leftx, self.wall.topy, 
                               self.wall.leftx, self.wall.boty,
                               fill='red', width=self.wall.th)
        elif obj == "wall0":
            canvas.create_line(self.wall.rightx, self.wall.topy, 
                               self.wall.rightx, self.wall.boty,
                               fill='red', width=self.wall.th)
        elif obj == "wall1":
            canvas.create_line(self.wall.leftx, self.wall.topy, 
                               self.wall.rightx, self.wall.topy,
                               fill='red', width=self.wall.th)
        elif obj == "wall3":
            canvas.create_line(self.wall.leftx, self.wall.boty, 
                               self.wall.rightx, self.wall.boty,
                               fill='red', width=self.wall.th)

        # for door and windows:
        elif isinstance(obj, Door) or isinstance(obj, Window):
            canvas.create_line(obj.cx - sin(obj.direction)*obj.w/2, 
                           obj.cy - cos(obj.direction)*obj.w/2,
                           obj.cx + sin(obj.direction)*obj.w/2, 
                           obj.cy + cos(obj.direction)*obj.w/2,
                           fill='red', width=obj.th)
        
        # for furniture
        else:
            canvas.create_rectangle(obj.leftx, obj.topy, obj.rightx, obj.boty,
                                outline='red', width=3)

    def ifCollideExisting(self, obj):
        # check collision btw door and windows
        if isinstance(obj, Door) or isinstance(obj, Window):
            hostWall = obj.host
            for other in self.wallDict[hostWall]:
                if other != obj:
                    if hostWall == "wall1" or hostWall == "wall3":
                        if (abs(obj.cx-other.cx) < obj.w/2+ other.w/2): 
                            return True
                    else: 
                        if (abs(obj.cy-other.cy) < obj.w/2+ other.w/2): 
                            return True
        
        # check collision btw furn
        if isinstance(obj, Furniture):
            for furnList in self.furnDict.values():
                for furn in furnList:
                    if furn != obj:
                        if (obj.rightx>=furn.leftx and obj.rightx<=furn.rightx 
                            and obj.boty>=furn.topy and obj.boty<=furn.boty):
                            return True
                        if (obj.leftx>=furn.leftx and obj.leftx<=furn.rightx 
                            and obj.boty>=furn.topy and obj.boty<=furn.boty):
                            return True
                        if (obj.rightx>=furn.leftx and obj.rightx<=furn.rightx 
                            and obj.topy>=furn.topy and obj.topy<=furn.boty):
                            return True
                        if (obj.leftx>=furn.leftx and obj.leftx<=furn.rightx 
                            and obj.topy>=furn.topy and obj.topy<=furn.boty):
                            return True
                        # two-way checking
                        if (furn.rightx>=obj.leftx and furn.rightx<=obj.rightx 
                            and furn.boty>=obj.topy and furn.boty<=obj.boty):
                            return True
                        if (furn.leftx>=obj.leftx and furn.leftx<=obj.rightx 
                            and furn.boty>=obj.topy and furn.boty<=obj.boty):
                            return True
                        if (furn.rightx>=obj.leftx and furn.rightx<=obj.rightx 
                            and furn.topy>=obj.topy and furn.topy<=obj.boty):
                            return True
                        if (furn.leftx>=obj.leftx and furn.leftx<=obj.rightx 
                            and furn.topy>=obj.topy and furn.topy<=obj.boty):
                            return True
            
        return False
    
    def ifFurnInRoom(self, furn):
        if self.wall == None: return False
        if (furn.leftx > (self.wall.leftx+self.wall.th/2) and 
            furn.rightx < (self.wall.rightx-self.wall.th/2) and
            furn.topy > (self.wall.topy+self.wall.th/2) and 
            furn.boty < (self.wall.boty-self.wall.th/2)):
            return True
        return False

    def isWallLegal(self):
        if self.wall.leftx >= self.wall.rightx-self.wall.th : return False
        if self.wall.topy >= self.wall.boty-self.wall.th: return False

        for furnList in self.furnDict.values():
            for furn in furnList:
                if not self.ifFurnInRoom(furn):
                    return False
        
        for objList in self.wallDict.values():
            for obj in objList:
                if obj.host == "wall1" or obj.host == "wall3":
                    if (obj.cx-obj.w/2 < self.wall.leftx+self.wall.th or 
                        obj.cx+obj.w/2 > self.wall.rightx-self.wall.th):
                        return False
                else:
                    if (obj.cy-obj.w/2 < self.wall.topy+self.wall.th or
                        obj.cy+obj.w/2 > self.wall.boty-self.wall.th):
                        return False
        
        return True

    def moveSelection(self, command, selection):
        dx, dy = 0, 0
        if command == 'Up': dy = -self.inchPixelRatio
        if command == 'Down': dy = self.inchPixelRatio
        if command == 'Left': dx = -self.inchPixelRatio
        if command == 'Right': dx = self.inchPixelRatio
        
        # for furniture
        if isinstance(selection, Furniture): 
            selection.cx += dx
            selection.leftx += dx
            selection.rightx += dx
            selection.cy += dy
            selection.topy += dy
            selection.boty += dy
            # undo if collide
            if (self.ifCollideExisting(selection)
                or not self.ifFurnInRoom(selection)):
                selection.cx -= dx
                selection.leftx -= dx
                selection.rightx -= dx
                selection.cy -= dy
                selection.topy -= dy
                selection.boty -= dy

        # for door and windows
        if isinstance(selection, Door) or isinstance(selection, Window):
            if selection.host == "wall1" or selection.host == "wall3":
                selection.cx += dx
                # undo if collide
                if not self.isWallLegal() or self.ifCollideExisting(selection):
                    selection.cx -= dx
            else:
                selection.cy += dy
                # undo if collide
                if not self.isWallLegal() or self.ifCollideExisting(selection):
                    selection.cy -= dy

        # for wall
        if selection == "wall2":
            self.wall.leftx += dx
            self.wall.x -= dx
            self.wall.cx += dx/2
            for obj in self.wallDict["wall2"]:
                obj.cx += dx
            # undo if collide
            if not self.isWallLegal():
                self.wall.leftx -= dx
                self.wall.x += dx
                self.wall.cx -= dx/2
                for obj in self.wallDict["wall2"]:
                    obj.cx -= dx

        if selection == "wall0":
            self.wall.rightx += dx
            self.wall.x += dx
            self.wall.cx += dx/2
            for obj in self.wallDict["wall0"]:
                obj.cx += dx
            # undo if collide
            if not self.isWallLegal():
                self.wall.rightx -= dx
                self.wall.x -= dx
                self.wall.cx -= dx/2
                for obj in self.wallDict["wall0"]:
                    obj.cx -= dx

        if selection == "wall1":
            self.wall.topy += dy
            self.wall.y -= dy
            self.wall.cy += dy/2
            for obj in self.wallDict["wall1"]:
                obj.cy += dy
            # undo if collide
            if not self.isWallLegal():
                self.wall.topy -= dy
                self.wall.y += dy
                self.wall.cy -= dy/2
                for obj in self.wallDict["wall1"]:
                    obj.cy -= dy

        if selection == "wall3":
            self.wall.boty += dy
            self.wall.y += dy
            self.wall.cy += dy/2
            for obj in self.wallDict["wall3"]:
                obj.cy += dy
            # undo if collide
            if not self.isWallLegal():
                self.wall.boty -= dy
                self.wall.y -= dy
                self.wall.cy -= dy/2
                for obj in self.wallDict["wall3"]:
                    obj.cy -= dy

    def deleteSelection(self, selection):
        if isinstance(selection, Bed) and selection in self.furnDict['beds']:
            self.furnDict['beds'].remove(selection)
            print("Bed deleted")
        if isinstance(selection, Nist) and selection in self.furnDict['nightstands']:
            self.furnDict['nightstands'].remove(selection)
            print("Nightstand deleted")
        if isinstance(selection, Table) and selection in self.furnDict['tables']:
            self.furnDict['tables'].remove(selection)
            print("Table deleted")
        if isinstance(selection, Chair) and selection in self.furnDict['chairs']:
            self.furnDict['chairs'].remove(selection)
            print("Chair deleted")
        if isinstance(selection, Dresser) and selection in self.furnDict['dressers']:
            self.furnDict['dressers'].remove(selection)
            print("Dresser deleted")
        if isinstance(selection, Window):
            for objList in self.wallDict.values():
                if selection in objList: 
                    objList.remove(selection)
                    print("Window deleted")
                    break

    def rotateSelection(self, selection):
        if isinstance(selection, Furniture): 
            # direction val: 0-Right, 1-Up, 2-Left, 3-Down
            old_x = selection.x
            old_y = selection.y
            old_direction = selection.direction
            selection.x = old_y
            selection.y = old_x
            selection.direction = (old_direction + 1) % 4
            selection.leftx = selection.cx - selection.x/2
            selection.rightx = selection.cx + selection.x/2
            selection.topy = selection.cy - selection.y/2
            selection.boty = selection.cy + selection.y/2
            # undo if collide
            if (self.ifCollideExisting(selection)
                or not self.ifFurnInRoom(selection)):
                selection.x = old_x
                selection.y = old_y
                selection.direction = old_direction
                selection.leftx = selection.cx - selection.x/2
                selection.rightx = selection.cx + selection.x/2
                selection.topy = selection.cy - selection.y/2
                selection.boty = selection.cy + selection.y/2
        if isinstance(selection, Door): 
            selection.swing = -selection.swing



class Furniture():
    def __init__(self, cx, cy, inchPixelRatio=3):
        self.cx = cx
        self.cy = cy
        self.direction = 1
        self.inchPixelRatio = inchPixelRatio

    def __eq__(self, other):
        return (type(self)==type(other) and
                (self.cx == other.cx) and (self.cy == other.cy) and 
                (self.x == other.x) and (self.y == other.y))

class Bed(Furniture):
    def __init__(self, cx, cy, x=54, y=75, inchPixelRatio=3):
        super().__init__(cx, cy, inchPixelRatio)
        self.direction = 1
        self.x = x * self.inchPixelRatio
        self.y = y * self.inchPixelRatio
        self.leftx = self.cx - self.x/2
        self.rightx = self.cx + self.x/2
        self.topy = self.cy - self.y/2
        self.boty = self.cy + self .y/2
    
    def draw(self, canvas):
        # outline
        round_rectangle(canvas, self.leftx, self.topy, self.rightx, self.boty,
                        r=3*self.inchPixelRatio, width=2)
        # pillows
        r = self.inchPixelRatio
        if self.direction == 0:
            p0_x0 = self.rightx-self.y/4
            p0_y0 = self.topy+self.y/12
            p0_x1 = self.rightx-self.y/12
            p0_y1 = self.topy+5*self.y/12

            p1_x0 = self.rightx-self.y/4
            p1_y0 = self.topy+7*self.y/12
            p1_x1 = self.rightx-self.y/12
            p1_y1 = self.topy+11*self.y/12
        if self.direction == 1:
            p0_x0 = self.leftx+self.x/12
            p0_y0 = self.topy+self.x/12
            p0_x1 = self.leftx+5*self.x/12
            p0_y1 = self.topy+self.x/4

            p1_x0 = self.leftx+7*self.x/12
            p1_y0 = self.topy+self.x/12
            p1_x1 = self.leftx+11*self.x/12
            p1_y1 = self.topy+self.x/4
        if self.direction == 2:
            p0_x0 = self.leftx+self.y/12
            p0_y0 = self.topy+self.y/12
            p0_x1 = self.leftx+self.y/4
            p0_y1 = self.topy+5*self.y/12

            p1_x0 = self.leftx+self.y/12
            p1_y0 = self.topy+7*self.y/12
            p1_x1 = self.leftx+self.y/4
            p1_y1 = self.topy+11*self.y/12
        if self.direction == 3:
            p0_x0 = self.leftx+self.x/12
            p0_y0 = self.boty-self.x/4
            p0_x1 = self.leftx+5*self.x/12
            p0_y1 = self.boty-self.x/12

            p1_x0 = self.leftx+7*self.x/12
            p1_y0 = self.boty-self.x/4
            p1_x1 = self.leftx+11*self.x/12
            p1_y1 = self.boty-self.x/12

        round_rectangle(canvas, p0_x0, p0_y0, p0_x1, p0_y1, r, width=1)
        round_rectangle(canvas, p1_x0, p1_y0, p1_x1, p1_y1, r, width=1)
        
        # bedding
        if self.direction == 0:
            l0_x0 = self.rightx-self.y/3
            l0_y0 = self.topy
            l0_x1 = self.rightx-self.y/3
            l0_y1 = self.boty

            l1_x0 = self.rightx-self.y/2
            l1_y0 = self.topy
            l1_x1 = self.rightx-self.y/3
            l1_y1 = self.boty
        if self.direction == 1:
            l0_x0 = self.leftx
            l0_y0 = self.topy+self.x/3
            l0_x1 = self.rightx
            l0_y1 = self.topy+self.x/3

            l1_x0 = self.leftx
            l1_y0 = self.topy+self.x/2
            l1_x1 = self.rightx
            l1_y1 = self.topy+self.x/3
        if self.direction == 2:
            l0_x0 = self.leftx+self.y/3
            l0_y0 = self.topy
            l0_x1 = self.leftx+self.y/3
            l0_y1 = self.boty

            l1_x0 = self.leftx+self.y/3
            l1_y0 = self.topy
            l1_x1 = self.leftx+self.y/2
            l1_y1 = self.boty
        if self.direction == 3:
            l0_x0 = self.leftx
            l0_y0 = self.boty-self.x/3
            l0_x1 = self.rightx
            l0_y1 = self.boty-self.x/3

            l1_x0 = self.leftx
            l1_y0 = self.boty-self.x/3
            l1_x1 = self.rightx
            l1_y1 = self.boty-self.x/2

        canvas.create_line(l0_x0, l0_y0, l0_x1, l0_y1)
        canvas.create_line(l1_x0, l1_y0, l1_x1, l1_y1)

class Nist(Furniture):
    def __init__(self, cx, cy, x=18, y=16, inchPixelRatio=3):
        super().__init__(cx, cy, inchPixelRatio)
        self.direction = 1
        self.x = x * inchPixelRatio
        self.y = y * inchPixelRatio
        self.leftx = cx - self.x/2
        self.rightx = cx + self.x/2
        self.topy = cy - self.y/2
        self.boty = cy + self.y/2

    def draw(self, canvas):
        # outline
        round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        # lamp
        canvas.create_oval(self.cx-self.y/3, self.cy-self.y/3, 
                           self.cx+self.y/3, self.cy+self.y/3)
        canvas.create_oval(self.cx-self.y/6, self.cy-self.y/6, 
                           self.cx+self.y/6, self.cy+self.y/6)

class Table(Furniture):
    def __init__(self, cx, cy, x=48, y=24, inchPixelRatio=3):
        super().__init__(cx, cy, inchPixelRatio)
        self.direction = 1
        self.x = x * inchPixelRatio
        self.y = y * inchPixelRatio
        self.leftx = cx - self.x/2
        self.rightx = cx + self.x/2
        self.topy = cy - self.y/2
        self.boty = cy + self.y/2

    def draw(self, canvas):
        round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)

class Chair(Furniture):
    def __init__(self, cx, cy, x=20, y=18, inchPixelRatio=3):
        super().__init__(cx, cy, inchPixelRatio)
        self.direction = 1
        self.x = x * inchPixelRatio
        self.y = y * inchPixelRatio
        self.leftx = cx - self.x/2
        self.rightx = cx + self.x/2
        self.topy = cy - self.y/2
        self.boty = cy + self.y/2

    def draw(self, canvas):
        # outline
        round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        # arms
        if self.direction == 1 or self.direction == 3:
            round_rectangle(canvas,self.leftx, self.topy, self.leftx+1.5*self.inchPixelRatio, self.boty,
                                r=self.inchPixelRatio, width=2)
            round_rectangle(canvas,self.rightx-1.5*self.inchPixelRatio, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        if self.direction == 0 or self.direction == 2:
            round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.topy+1.5*self.inchPixelRatio,
                                r=self.inchPixelRatio, width=2)
            round_rectangle(canvas,self.leftx, self.boty-1.5*self.inchPixelRatio, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        # back
        if self.direction == 0:
            round_rectangle(canvas,self.leftx, self.topy, self.leftx+3*self.inchPixelRatio, self.boty,
                                r=self.inchPixelRatio, width=2)
        if self.direction == 1:
            round_rectangle(canvas,self.leftx, self.boty-3*self.inchPixelRatio, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        if self.direction == 2:
            round_rectangle(canvas,self.rightx-3*self.inchPixelRatio, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)
        if self.direction == 3:
            round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.topy+3*self.inchPixelRatio,
                                r=self.inchPixelRatio, width=2)

class Dresser(Furniture):
    def __init__(self, cx, cy, x=30, y=20, inchPixelRatio=3):
        super().__init__(cx, cy, inchPixelRatio)
        self.direction = 1
        self.x = x * inchPixelRatio
        self.y = y * inchPixelRatio
        self.leftx = cx - self.x/2
        self.rightx = cx + self.x/2
        self.topy = cy - self.y/2
        self.boty = cy + self.y/2

    def draw(self, canvas):
        round_rectangle(canvas,self.leftx, self.topy, self.rightx, self.boty,
                                r=self.inchPixelRatio, width=2)



class Wall():
    def __init__(self, cx, cy, x=144, y=144, th=4.5, inchPixelRatio=3):
        self.cx = cx
        self.cy = cy
        self.inchPixelRatio = inchPixelRatio

        self.th = th * self.inchPixelRatio
        self.x = x * self.inchPixelRatio
        self.y = y * self.inchPixelRatio
        self.leftx = self.cx - self.x/2
        self.rightx = self.cx + self.x/2
        self.topy = self.cy - self.y/2
        self.boty = self.cy + self .y/2

        self.door = None

    def __eq__(self, other):    
        return (type(self)==type(other) and
                (self.cx == other.cx) and (self.cy == other.cy))

    def draw(self, canvas):
        canvas.create_rectangle(self.leftx, self.topy, self.rightx, self.boty,
                                fill='', width=self.th)
        x = int((self.rightx - self.leftx)/self.inchPixelRatio)
        xFt = x // 12
        xIn = x % 12
        y = int((self.boty - self.topy)/self.inchPixelRatio)
        yFt = y // 12
        yIn = y % 12
        canvas.create_text(self.cx, self.topy-12*self.inchPixelRatio, 
                           text=f'{xFt}ft {xIn}in', font=('Roboto', 16))
        canvas.create_text(self.leftx-16*self.inchPixelRatio, self.cy, 
                           text=f'{yFt}ft {yIn}in', font=('Roboto', 16))


class Door(Wall):
    # cxcy is door frame center, w is width of the door
    def __init__(self, cx, cy, w=36, th=4.5, host="wall3", inchPixelRatio=3):
        self.cx = cx
        self.cy = cy
        self.host = host
        self.direction = 1
        self.swing = 1 # swing 1 is left, -1 is right
        self.inchPixelRatio = inchPixelRatio
        
        self.th = th * self.inchPixelRatio
        self.w = w * self.inchPixelRatio 
    
    def draw(self, canvas):
        sw = self.swing
        start = abs((sw-1)//2)*90
        canvas.create_arc(self.cx - sw*3*self.w/2, self.cy+self.w, 
                            self.cx + sw*self.w/2, self.cy-self.w, extent=90, 
                            start=start, fill='')
        canvas.create_line(self.cx - sw*self.w/2, self.cy, 
                            self.cx + sw*self.w/2, self.cy, 
                            fill='white', width=self.th)
        canvas.create_line(self.cx - sw*self.w/2, self.cy-self.w, 
                            self.cx - sw*self.w/2, self.cy, 
                            width=self.inchPixelRatio)
        
class Window(Wall):
    # cxcy is window frame center, w is width of the door
    def __init__(self, cx, cy, host="wall3", w=36, th=4.5, inchPixelRatio=3):
        self.cx = cx
        self.cy = cy
        self.host = host # wall 0, 1, 2, 3
        self.direction = int(host[-1]) % 2 # vert dir 0, hori dir 1
        self.inchPixelRatio = inchPixelRatio
        
        self.th = th * self.inchPixelRatio
        self.w = w * self.inchPixelRatio 

    def draw(self, canvas):
        canvas.create_rectangle(self.cx - sin(self.direction)*self.w/2 - cos(self.direction)*self.th/2,
                        self.cy - cos(self.direction)*self.w/2 - sin(self.direction)*self.th/2,
                        self.cx + sin(self.direction)*self.w/2 + cos(self.direction)*self.th/2,
                        self.cy + cos(self.direction)*self.w/2 + sin(self.direction)*self.th/2,
                        fill = 'white')
        canvas.create_line(self.cx - sin(self.direction)*self.w/2, 
                           self.cy - cos(self.direction)*self.w/2,
                           self.cx + sin(self.direction)*self.w/2, 
                           self.cy + cos(self.direction)*self.w/2,)