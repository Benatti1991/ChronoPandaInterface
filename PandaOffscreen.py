# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:06:55 2019

@author: SB
"""

#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Models: Eddie Canaan
# Last Updated: 2015-03-13
#


from direct.showbase.ShowBase import ShowBase


from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TextNode, NodePath, Texture, CardMaker, Shader
from panda3d.core import LPoint3, LVector3, BitMask32, Quat
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
import sys
import pychrono as chrono
import math


class ChronoPandaInterface(ShowBase):
    ChBodyList = []
    ModelList = []
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        
        mybuffer =  base.win.makeTextureBuffer("Buffer", 512, 512, to_ram=True)
        mytexture = mybuffer.getTexture()
        mybuffer.setSort(-100)
        self.mycamera = base.makeCamera(mybuffer)
        self.myscene = NodePath("My Scene")
        self.mycamera.reparentTo(self.myscene)

        self.texture = mytexture
        

        self.accept('escape', sys.exit)  # Escape quits
        self.disableMouse()  # Disble mouse camera control
        self.mycamera.setPosHpr(0, -12, 8, 0, -35, 0)  # Set the camera
        self.setupLights()  # Setup default lighting
    

    def setupLights(self):  # This function sets up some default lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.8, .8, .8, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 45, -45))
        directionalLight.setColor((0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))
        
        
    def SetCamera(self, pos, targ):
        
        delta = targ - pos
        q0 = chrono.ChQuaternionD()
        q0.Q_from_AngAxis(-math.pi/2, chrono.VECT_X)
        
        alpha = 0   
        if (delta.z <= 0 and delta.x != 0):
               alpha = -math.asin(delta.x/math.hypot(delta.x, delta.z))
        if (delta.z > 0):
               alpha = math.asin(delta.x/math.hypot(delta.x, delta.z)) + math.pi
        q1 = chrono.ChQuaternionD()
        q1.Q_from_AngAxis(alpha, q0.GetZaxis())
        q2 = chrono.ChQuaternionD()
        q2 = q1*q0
        beta = math.asin(delta.y/delta.Length())
        q3 = chrono.ChQuaternionD()
        q3.Q_from_AngAxis(beta, q2.GetXaxis())
        qc = chrono.ChQuaternionD()
        qc = q3*q2
        q = Quat(qc.e0, qc.e1, qc.e2, qc.e3)
        self.mycamera.setPos(pos.x, pos.y, pos.z)
        self.mycamera.setQuat(q)
        
    """Function called at each step to update rendered bodies positions 
       according to the position af their respective modelled bodies"""    
    def Update_Pos(self):
           for model, body in zip(self.ModelList, self.ChBodyList) :
                  new_pos = body.GetPos()
                  model.setPos(new_pos.x, new_pos.y, new_pos.z)
                  new_ori = body.GetRot()
                  q = Quat(new_ori.e0, new_ori.e1, new_ori.e2, new_ori.e3)
                  model.setQuat(q)

    """Function used to update the visualization
    It shouldn't be called at each simulation step"""                    
    def Advance(self):
           
           self.Update_Pos()
           self.taskMgr.step()
           return self.texture 
           

        
        
class ChPandaBody(object):
    #def __init__(self, CPInterf, chbody , color)
    def __init__(self, CPInterf, chbody):
        self.chbody = chbody
        self.obj = loader.loadModel(self.model)
        self.obj.reparentTo(CPInterf.myscene)
        #self.obj.setColor(color)
        PosVec = chbody.GetPos()
        self.obj.setPos(PosVec.x,PosVec.y, PosVec.z)
        RotQuat = chbody.GetRot()
        q = Quat(RotQuat.e0,RotQuat.e1, RotQuat.e2, RotQuat.e3)
        self.obj.setQuat(q)
        CPInterf.ChBodyList.append(self.chbody)
        CPInterf.ModelList.append(self.obj)

    
class PandaCube(ChPandaBody):
       model = "models/cube.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody)
       
              self.obj.setScale(s)
              if color:
                     self.obj.setColor(color)

class PandaSphere(ChPandaBody):
       model = "models/sphere.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody)
       
              self.obj.setScale(s)
              if color:
                     self.obj.setColor(color)

class PandaBox(ChPandaBody):
       model = "models/cube.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody)
       
              self.obj.setSx(s[0])
              self.obj.setSy(s[1])
              self.obj.setSz(s[2])
              
              if color:
                     self.obj.setColor(color)
  #TODO: not a proper ellipsoid, just a stretched sphere                   
class PandaEllipsoid(ChPandaBody):
       model = "models/sphere.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody)
       
              self.obj.setSx(s[0])
              self.obj.setSy(s[1])
              self.obj.setSz(s[2])
              
              if color:
                     self.obj.setColor(color)   
         
"""Cylinder visualization. Set s=(r,h)
TODO: not properly set. 
"""              
class PandaCyilinder(ChPandaBody):
       model = "models/cylinder.obj"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody)
       
              self.obj.setSx(s[0])
              self.obj.setSy(s[2])
              self.obj.setSz(s[1])
              
              if color:
                     self.obj.setColor(color)   