# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:01:12 2019

@author: SB
"""
import pychrono as chrono
from panda3d.core import LPoint3, LVector3, BitMask32, Quat


class ChPandaBody(object):
    #def __init__(self, CPInterf, chbody , color)
    def __init__(self, CPInterf, chbody, color=None):
        self.chbody = chbody
        self.obj = loader.loadModel(self.model)
        if CPInterf.OnScreen:
               self.obj.reparentTo(render)
        else: 
               self.obj.reparentTo(CPInterf.myscene)
        if color:
               self.obj.setColor(color) 
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
              ChPandaBody.__init__(self, CPInterf, chbody, color)
       
              self.obj.setScale(s)


class PandaSphere(ChPandaBody):
       model = "models/sphere.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody, color)
       
              self.obj.setScale(s)


class PandaBox(ChPandaBody):
       model = "models/cube.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody, color)
       
              self.obj.setSx(s[0])
              self.obj.setSy(s[1])
              self.obj.setSz(s[2])
              

  #TODO: not a proper ellipsoid, just a stretched sphere                   
class PandaEllipsoid(ChPandaBody):
       model = "models/sphere.blend"
       def __init__(self, CPInterf, chbody, s, color=None):
              ChPandaBody.__init__(self, CPInterf, chbody, color)
       
              self.obj.setSx(s[0])
              self.obj.setSy(s[1])
              self.obj.setSz(s[2])

         
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