#!/usr/bin/python3
#coding=utf-8

from tkinter import *

DELAY = 500

def onTimer(highWay, canvas):
  highWay.update(canvas, 1)
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
    pass

  def update(self, can, time):
    """Updates coordinates of all drivers and lights, removing outdrived drivers"""
    self.__objects[0].update(can)
    self.__objects[1].update(can)
    for elem in self.__drivers:
      elem.update(can)
    self.draw(can)
    pass

  def addObject(self, object):
    """Generates new driver on this road"""
    self.__objects.append(object)
    pass

  def addDriver(self, driver,road):
    """Generates new driver on this road"""
    self.__drivers.append(driver)
    pass
  
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
  def draw(self, can):
    """Draws this"""
    pass

  def getX(self):
    """returns x and y of object"""
    pass

  def getY(self):
    """returns x and y of object"""
    pass

class Road(Drawable):
  """
    The road has:
    X position
    Y position
    Width
    Height
    Direction of move(Up, Down) (1, -1)
  """
  def __init__(self, x, y, width, height, dir, color):
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height
    self.__dir = dir
    self.__color = color
    pass

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

  def isFree(self,x0,x1):
    """Is it able to change current line to this line?"""
    pass
  
  def draw(self, can):
    can.create_polygon(self.__x+1, self.__y, self.__x+self.__width-1, self.__y, self.__x+self.__width-1,
                       self.__y+self.__height, self.__x+1, self.__y+self.__height, fill=self.__color)
    pass

  def getX(self):
    """returns x and y of object"""
    return self.__x
    pass

  def getY(self):
    """returns x and y of object"""
    return self.__y
    pass

class OffRoad(Road):
  """Also a road, but not for all. OffRoad has another draw attributes(color, example)"""
  pass

class Light(Drawable):
  """The light. Can be yellow, red, or blue."""
  __befColor = "#F00"
  def __init__(self, x, y, width, height, color):
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height
    self.__dir = dir
    self.__color = color
    pass

  def update(self,time):
    """Updates the color of light"""
    if (self.__color == "#F00"):
      self.__befColor = self.__color
      self.__color = "#FF0"
    elif (self.__color == "#0F0"):
      self.__befColor = self.__color
      self.__color = "#FF0"
    else:
      if (self.__befColor == "#F00"):
        self.__befColor = self.__color
        self.__color = "#0F0"
      else:
        self.__befColor = self.__color
        self.__color = "#F00"
    pass
  
  def draw(self, can):
    """Draws the light on current location"""
    can.create_oval(self.__x+5, self.__y+5, self.__x+self.__width-5, self.__y+self.__height-5, fill=self.__color)
    pass

  def getColor(self):
    """Current color of light"""
    return self.__color
    pass

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
  def __init__(self, x, y, width, height, speed, acceleration, dir):
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height
    self.__dir = dir
    self.__color = speed
    self.__color = acceleration
    pass

  def update(self,time):
    """Updates logic of driver; Need to be overriden"""
    pass

  def isAligned(self):
    """Is the driver at center of current road?"""
    pass

  def currentRoad(self):
    """Road, on which the driver is currently riding."""
    pass

  def nextDriver(self):
    """Returns the next to you river on this road"""
    pass

  def prevDriver(self):
    """Returns the previos driver on this road"""

  def distance(self, obj):
    """Measures distance from driver to obj."""

  def draw(self,can):
    """Draws a driver"""
    pass
  
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
  lighter1 = Light(0, 280, 40, 40,"#0F0")
  lighter2 = Light(280, 280, 40, 40, "#0F0")
  road1 = Road(40, 0, 40, 600, -1,"#888")
  road2 = Road(80, 0, 40, 600, -1, "#444")
  road3 = Road(120, 0, 40, 600, -1, "#444")
  road4 = Road(160, 0, 40, 600, 1, "#444")
  road5 = Road(200, 0, 40, 600, 1, "#444")
  road6 = Road(240, 0, 40, 600, 1, "#888")
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
