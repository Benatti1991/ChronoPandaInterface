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
mysystem.Set_G_acc(chrono.ChVectorD(0, 0, -9.81))
cpi = ChronoPandaInterface.OnscreenRender()
# Create a fixed rigid body

chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)
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

mbody2 = chrono.ChBody()
mbody2.SetBodyFixed(True)
mbody2.SetPos( chrono.ChVectorD(0,0,3))

mbody2.SetMass(1)
mbody2.SetMaterialSurface(brick_material)
mbody2.GetCollisionModel().ClearModel()
mbody2.GetCollisionModel().AddBox(0.5,0.5,0.5) # must set half sizes
mbody2.GetCollisionModel().BuildModel()
mbody2.SetCollide(True)
ChronoPandaInterface.PandaCube(cpi, mbody2,1, WHITE)

#mysystem.Add(mbody2)


mbody3 = chrono.ChBody()
mbody3.SetBodyFixed(False)
mbody3.SetPos( chrono.ChVectorD(0,0,3))

mbody3.SetMass(1)
mbody3.SetMaterialSurface(brick_material)
mbody3.GetCollisionModel().ClearModel()
mbody3.GetCollisionModel().AddSphere(0.5) # must set half sizes
mbody3.GetCollisionModel().BuildModel()
mbody3.SetCollide(True)
ChronoPandaInterface.PandaSphere(cpi, mbody3,1, BLACK)

mysystem.Add(mbody3)

cpi.camera.setPosHpr(0, -12, 0, 0, 0, 0)
timestep=0.005
t =0;

while(t<5):
    mysystem.DoStepDynamics(timestep)
    cpi.Advance()
    camera_ref=mbody3.GetPos()
    #cpi.SetCamera(camera_ref.x, camera_ref.y-2.0, camera_ref.z, 0, 0, 0)
    #cpi.camera.setPosHpr(camera_ref.x, camera_ref.y-2.0, camera_ref.z, 0, 0, 0)

    
    t+= timestep

cpi.destroy()




