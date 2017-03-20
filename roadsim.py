#!/usr/bin/python3
#coding=utf-8

from tkinter import *
import time
import random

DELAY = 20
TIMEMOD = 1 #modifier of time.
FL1 = 1 #Flow 1
FL2 = 1  #Flow 2 - cars per second arived
DISTANCE = 40
MINDISTANCE = 20

def onTimer(highWay, canvas):
  highWay.update(canvas, 20*TIMEMOD)     #20 ms between updates of window is enough 50fps.
  canvas.after(DELAY, onTimer, highWay, canvas)

class Highway(object):
  """
Highway have links on all roads, lights and drivers, an can
iterately loop throuph them to update or to draw.
  """
  __objects = []
  __drivers = []
  def __init__(self, x, y, width, height, color):
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height
    self.__color = color
    self.__time = 0
    pass

  def update(self, can, time):
    """Updates coordinates of all drivers and lights, removing outdrived drivers"""
    self.__time = time

    for elem in self.__objects:
      elem.update(self.__time) #Lighter 1
    for elem in self.__drivers:
      elem.update(self.__time)
    self.draw(can)
   
    if random.randrange(1000) <= FL1*time: #Spam a driver on a first!
      n = random.randrange(2)+3 #3 or 4
      self.addDriver(Driver(0,0,30,30,self.__objects[n]),self.__objects[n]);
      
    if random.randrange(1000) <= FL2*time: #Spam a driver on a first!
      n = random.randrange(2)+5 #5 or 6
      self.addDriver(Driver(0,0,30,30,self.__objects[n]),self.__objects[n]);
    i = 0
    while i < len(self.__drivers): 
      car = self.__drivers[i]
      if car.getY()+car.getH()<0 and car.dir < 0:
        if car.prev:
          car.prev.next = None
        del self.__drivers[i]
      elif car.getY()>self.__height and car.dir > 0:
        if car.prev:
          car.prev.next = None
        del self.__drivers[i]
      else:
        i+=1

      
  def addObject(self, object):
    """Generates new driver on this road"""
    self.__objects.append(object)
    pass

  def addDriver(self, driver,road):
    """Generates new driver on this road"""
    carint = DISTANCE + 40 
    driver.setX(road.getX()+(road.getW()-driver.getW())//2)
    driver.dir = road.dir
    if road.dir > 0:
      ny = 0
      while not road.isFree(carint-100-ny,-100-ny):
        ny +=20
      driver.setY(-100-ny)
    elif road.dir < 0:
      ny = 0
      while not road.isFree(self.__height+100+ny+carint,self.__height+100+ny):
        ny +=20
      driver.setY(self.__height+100+ny)
    self.__drivers.append(driver)
    road.cars.append(driver)
    if len(road.cars)>1:
      driver.next = road.cars[len(road.cars)-2]
      road.cars[len(road.cars)-2].prev = driver
  
  def draw(self, can):
    """Draws all the objects on provided Canvas object"""
    can.create_polygon(self.__x, self.__y, self.__x+self.__width, self.__y,
                       self.__x+self.__width, self.__y+self.__height, self.__x, self.__y+self.__height,
                       fill=self.__color)
    for elem in self.__objects:
      elem.draw(can)
    crosswalk = can.create_polygon(80, 280, 240, 280, 240, 320, 80, 320, fill="#FFF")
    for i in range(10):
      can.create_polygon(80+i*20, 280, 90+i*20, 280, 90+i*20, 320, 80+i*20, 320, fill="#888")
    for elem in self.__drivers:
      elem.draw(can)
    pass

class Drawable(object):
  """The object, that can be drawed!"""

  def __init__(self,x,y,w,h):
    self.x = x
    self.y = y
    self.width = w
    self.height = h

  def draw(self, can):
    """Draws this"""
    pass

  def getX(self):
    """returns x and y of object"""
    return self.x

  def getY(self):
    """returns x and y of object"""
    return self.y

  def getW(self):
    return self.width
  
  def getH(self):
    return self.height

  def setX(self, nx):
    self.x = nx

  def setY(self, ny):
    self.y = ny

  def setW(self,nwidth):
    self.width = nwidth 
  
  def setH(self,nheight):
    self.height = nheight


#|------------------------------------ROAD------------------------>

class Road(Drawable):
  """
    The road has:
    X position
    Y position
    Width
    Height
    Direction of move(Up, Down) (1, -1)
  """
  def __init__(self, x, y, width, height, dira, color, light):
    super(Road,self).__init__(x,y,width,height)
    self.dir = dira
    self.__color = color
    self.light = light
    self.cars = []

  def update(self, time):
    i = 0
    while i < len(self.cars): 
      car = self.cars[i]
      if car.getY()+car.getH()<0 and car.dir < 0:
        del self.cars[i]
      elif car.getY()>self.height and car.dir > 0:
        del self.cars[i]
      else:
        i+=1


  def setRight(self, rightRoad):
    """Get right to this road, or None"""
    self.__rightRoad = rightRoad
    pass

  def setLeft(self, leftRoad):
    """Get left to this road, or None"""
    self.__leftRoad = leftRoad
    pass

  def getRight(self):
    """Get right to this road, or None"""
    return self.__rightRoad
    pass

  def getLeft(self):
    """Get left to this road, or None"""
    return self.__leftRoad
    pass

  def isFree(self,y0,y1):  #y0 > y1
    """Is it able to change current line to this line?"""
    for car in self.cars:
#      print ("check: %d - %d, cucar: %d, %d" % (y0,y1,car.getY(),car.getH()))
      if (car.getY()+car.getH()>y1) and (car.getY() < y0):
        return False
    return True
  
  def draw(self, can):
    can.create_polygon(self.x+1, self.y, self.x+self.width-1, self.y, self.x+self.width-1,
                       self.y+self.height, self.x+1, self.y+self.height, fill=self.__color)
    

class OffRoad(Road):
  """Also a road, but not for all. OffRoad has another draw attributes(color, example)"""
  pass

#|------------------LIGHT----------------------->

class Light(Drawable):
  """The light. Can be yellow, red, or blue."""
  __befColor = "#F00"
  def __init__(self, x, y, width, height, color=0):
    super(Light,self).__init__(x,y,width,height)
    self.__dir = dir
    self.__color = color
    self.__time = 0
    self.color_codes = ["#F00","#FF0","#0F0","#FF0"]
    self.color_ints = [3,1,5,1]

  def update(self,time):
    """Updates the color of lighti: time in ms"""
    self.__time += time
    if self.__time>=self.color_ints[self.__color]*1000:
      self.__time -= self.color_ints[self.__color]*1000
      self.__color+=1
      if self.__color>=len(self.color_codes):
        self.__color = 0;
#   Thanks, Dima.
#    if (self.__time>100):
#      self.__time-=100
#      if (self.__color == "#F00"):
#        self.__befColor = self.__color
#        self.__color = "#FF0"
#      elif (self.__color == "#0F0"):
#        self.__befColor = self.__color
#        self.__color = "#FF0"
#      else:
#        if (self.__befColor == "#F00"):
#          self.__befColor = self.__color
#          self.__color = "#0F0"
#        else:
#          self.__befColor = self.__color
#          self.__color = "#F00"
  

  def draw(self, can):
    """Draws the light on current location"""
    can.create_oval(self.x+5, self.y+5, self.x+self.width-5, self.y+self.height-5, fill=self.color_codes[self.__color])

  def getColor(self):
    """Current color of light"""
    return self.color_codes[self.__color]

class Driver(Drawable):
  """
    Usuall driver abstract class. Must have link to current highway, 
    to get information about drivers, roads, lights e.t.c
    Basic class attributes:
    X position
    Y position
    Speed
    Acceleration
    Direction(Up or Down?)
    dX - variable, detecting change of line, and which side to.
  """
  def __init__(self, x, y, width, height, nroad, speed = 0, acceleration = 0, dira = 0):
    super(Driver,self).__init__(x,y,width,height)
    self.dir = dira
    self.dy = 0
    self.__speed = speed
    self.__acc = acceleration
    self.__color = 'green' 
    self.curroad = nroad
    self.next = None
    self.prev = None
    self.stopping = False

  def update(self,time):
    """Updates logic of driver; Need to be overriden"""
    """time in ms: we must update every sicle, but change speed only on seconds tick."""
    maxspeed = 60

    self.stopping = False
    if self.next == None:
      self.__color = 'blue'
      self.stopping = False
    else:
      if self.getDistance(self.next)<30:
        self.__color = 'red'
        self.stopping = True
      else:
        self.__color = 'green'
    if (self.getDistance(self.curroad.light) <= 60) and self.getDistance(self.curroad.light) > 0 and (self.curroad.light.getColor()!="#0F0"):
      self.stopping = True
    if self.stopping == True:
      self.__acc = -10
    if self.stopping == False:
      if self.__speed < maxspeed:
        self.__acc = 10
      else:
        self.__acc = 10
        self.__speed = maxspeed
    if self.__speed < 0:
      self.__speed = 0
      self.__acc = 0
    if self.__acc != 0:
      self.__speed += self.__acc*time/10
    if self.__speed > 0:
      self.y+=self.dir * self.__speed*time/100

  def isAligned(self):
    """Is the driver at center of current road?"""
    pass

  def currentRoad(self):
    """Road, on which the driver is currently riding."""
    return self.curroad

  def nextDriver(self):
    """Returns the next to you river on this road"""
    return self.next

  def prevDriver(self):
    """Returns the previos driver on this road"""

  def getDistance(self, obj):
    """Measures distance from driver to obj."""
    #if obj == None:
    #  return 
    if obj.getY() > self.getY():
      return obj.getY() - self.getY() - self.getH()
    else:
      return self.getY() - obj.getY() - obj.getH()

  def draw(self,can):
    """Draws a driver"""
    can.create_oval(self.x+5, self.y+5, self.x+self.width-5, self.y+self.height-5, fill=self.__color)
  
  def getAcc(self):
    """Return Acceleration of this driver"""
    pass

class NormalDriver(Driver):
  def update(self,time):
    """Drive Logic of normal Driver"""
    pass

class AshotDriver(Driver):
  def update(self,time):
    """Drive Logic of Ashot"""
    pass

def main():
  """Main loop: Creating TKinter instance, running update cycle"""
  root = Tk()  # Производим инициализацию нашего графического интерфейса
  canvas = Canvas(root, width=320, height=600)  # Инициализируем Canvas размером 300х300 пикселей
  canvas.pack()  # Размещаем Canvas в окне нашего Tkinter-GUI
  highWay = Highway(0, 0, 320, 600, "#FF8")
  lighter1 = Light(0, 280, 40, 40,0)
  lighter2 = Light(280, 280, 40, 40,0)
  road1 = Road(40, 0, 40, 600, -1,"#888",lighter1)
  road2 = Road(80, 0, 40, 600, -1, "#444",lighter1)
  road3 = Road(120, 0, 40, 600, -1, "#444",lighter1)
  road4 = Road(160, 0, 40, 600, 1, "#444",lighter2)
  road5 = Road(200, 0, 40, 600, 1, "#444",lighter2)
  road6 = Road(240, 0, 40, 600, 1, "#888",lighter2)
  highWay.addObject(lighter1)
  highWay.addObject(lighter2)
  highWay.addObject(road1)
  highWay.addObject(road2)
  highWay.addObject(road3)
  highWay.addObject(road4)
  highWay.addObject(road5)
  highWay.addObject(road6)
  highWay.draw(canvas)

  canvas.after(DELAY, onTimer, highWay, canvas)
  root.mainloop()  # Создаем постоянный цикл
  pass


if __name__ == "__main__":
  main()

