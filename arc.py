#!/usr/bin/python3
#coding=utf-8

from tkinter import *

class Highway(object):
  """
Highway have links on all roads, lights and drivers, an can
iterately loop throuph them to update or to draw.
  """

  def update(self, time): 
    """Updates coordinates of all drivers and lights, removing outdrived drivers"""
    pass

  def addDriver(self, driver,road):
    """Generates new driver on this road"""
    pass
  
  def draw(self, can):
    """Draws all the objects on provided Canvas object"""
    pass

class Drawable(object):
  """The object, that can be drawed!"""
  
  def draw(self, can):
    """Draws this"""
    pass

  def getXY(self):
    """returns x and y of object"""
    pass

class Road(Drawable):
  """
    The road has:
    X position
    Y position
    Width
    Height
    Direction of move(Up, Down) 
  """

  def getRight(self):
    """Get right to this road, or None"""
    pass

  def getLeft(self):
    """Get left to this road, or None"""
    pass

  def isFree(self,x0,x1):
    """Is it able to change current line to this line?"""
    pass
  
  def draw(self, can):
    """Draws this road"""
    pass

class OffRoad(Road):
  """Also a road, but not for all. OffRoad has another draw attributes(color, example)"""
  pass

class Light(Drawable):
  """The light. Can be yellow, red, or blue."""
  
  def update(self,time):
    """Updates the color of light"""
    pass
  
  def draw(self, can):
    """Draws the light on current location"""
    pass

  def getColor(self):
    """Current color of light"""
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
  pass


if __name__ == "__main__":
  main()
