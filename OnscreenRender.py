# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:10:08 2019

@author: SB
"""
from direct.showbase.ShowBase import ShowBase
#from panda3d.core import CollisionTraverser, CollisionNode

from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3, BitMask32, Quat
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
import sys
import pychrono as chrono
import math


class OnscreenRender(ShowBase):
    OnScreen=True   
    ChBodyList = []
    ModelList = []
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text="Project Chrono/Panda3D",
                                  style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                  pos=(0.8, -0.95), scale = .07)
        self.escapeEvent = OnscreenText(
            text="ESC: Quit", parent=base.a2dTopLeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.1),
            align=TextNode.ALeft, scale = .05)
        self.mouse1Event = OnscreenText(
            text="None",
            parent=base.a2dTopLeft, align=TextNode.ALeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.16), scale=.05)

        self.accept('escape', sys.exit)  # Escape quits
        self.disableMouse()  # Disble mouse camera control
        camera.setPosHpr(0, -12, 8, 0, -35, 0)  # Set the camera
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
        camera.setQuat(q)
        
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