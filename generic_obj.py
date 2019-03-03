# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:11:48 2019

@author: SB
"""


import math

import ChronoPandaInterface 

import pychrono.core as chrono


print ("Example: create a system and visualize it in realtime 3D");

# ---------------------------------------------------------------------
#
#  Create the simulation system and add items
#

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)

mysystem      = chrono.ChSystemNSC()

cpi = ChronoPandaInterface.OnscreenRender()
# Create a fixed rigid body

chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.005)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.005)
mysystem.SetMaxItersSolverSpeed(70)

brick_material = chrono.ChMaterialSurfaceNSC()
brick_material.SetFriction(0.5)
brick_material.SetDampingF(0.2)
brick_material.SetCompliance (0.0000001)
brick_material.SetComplianceT(0.0000001)

mbody1 = chrono.ChBody()
mbody1.SetBodyFixed(True)
mbody1.SetPos( chrono.ChVectorD(0,0,0))
q = chrono.ChQuaternionD()
q.Q_from_AngAxis(math.pi/8, chrono.ChVectorD(0,1,0))
mbody1.SetRot(q)
mbody1.SetMass(1)
mbody1.SetMaterialSurface(brick_material)
mbody1.GetCollisionModel().ClearModel()
mbody1.GetCollisionModel().AddBox(1,1,1) # must set half sizes
mbody1.GetCollisionModel().BuildModel()
mbody1.SetCollide(True)
ChronoPandaInterface.PandaCube(cpi, mbody1,2,WHITE)

mysystem.Add(mbody1)


# Create the falling rigid body

mbody2 = chrono.ChBodyEasyMesh("fancy_models\pallet.obj", 500, True, True, 0.001, True)
mysystem.Add(mbody2)
mbody2.SetBodyFixed(False)
mbody2.SetPos( chrono.ChVectorD(0,6.5,0))

mbody2.SetMass(1)
mbody2.SetMaterialSurface(brick_material)
q = chrono.ChQuaternionD()
q.Q_from_AngAxis(math.pi/2, chrono.ChVectorD(1,0,0))
mbody2.SetRot(q)

mbody2.SetCollide(True)

ChronoPandaInterface.PandaGenericBody(cpi, mbody2,'fancy_models\pallet.obj')


timestep=0.002
t =0;
steps=0
while(t<5):
    mysystem.DoStepDynamics(timestep)
    if (steps%5 == 0):
           cpi.Advance()
           camera_ref=mbody2.GetPos()
           camera_orig=mbody2.GetPos()+chrono.ChVectorD(2,-2,-5)
           # uncomment and comment the other one the follow the sphere with the camera
           #cpi.camera.setPosHpr(camera_ref.x, camera_ref.y+2.0, camera_ref.z+1, 180, -20, 0)
           cpi.SetCamera(camera_orig, camera_ref)

    
    t+= timestep
    steps+=1

cpi.destroy()




