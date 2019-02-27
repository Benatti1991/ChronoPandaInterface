#-------------------------------------------------------------------------------
# Name:        demo_masonry
#
# This file shows how to
#   - create a small stack of bricks,
#   - create a support that shakes like an earthquake, with imposed motion law
#   - simulate the bricks that fall
#   - output the postprocessing data for rendering the animation with POVray
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()


# Load the Chrono::Engine unit and the postprocessing unit!!!
import pychrono.core as chrono
#import pychrono.postprocess
import ChronoPandaInterface 
import math

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
GRAY = (0.5, 0.5, 0.5, 1)
BRICK_ORANGE = (204/255, 102/255, 0, 1)

# ---------------------------------------------------------------------
#
#  Create the simulation system and add items
#

my_system = chrono.ChSystemNSC()
cpi = ChronoPandaInterface.ChronoPandaInterface()

# Set the default outward/inward shape margins for collision detection,
# this is epecially important for very large or very small objects.
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# Maybe you want to change some settings for the solver. For example you
# might want to use SetMaxItersSolverSpeed to set the number of iterations
# per timestep, etc.

#my_system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
my_system.SetMaxItersSolverSpeed(70)



# Create a contact material (surface property)to share between all objects.
# The rolling and spinning parameters are optional - if enabled they double
# the computational time.
brick_material = chrono.ChMaterialSurfaceNSC()
brick_material.SetFriction(0.5)
brick_material.SetDampingF(0.2)
brick_material.SetCompliance (0.0000001)
brick_material.SetComplianceT(0.0000001)
# brick_material.SetRollingFriction(rollfrict_param)
# brick_material.SetSpinningFriction(0)
# brick_material.SetComplianceRolling(0.0000001)
# brick_material.SetComplianceSpinning(0.0000001)



# Create the set of bricks in a vertical stack, along Y axis

nbricks_on_x = 4
nbricks_on_y = 6

size_brick_x = 0.15
size_brick_y = 0.12
size_brick_z = 0.12
density_brick = 1000;    # kg/m^3
mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z;
inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick; # to do: compute separate xx,yy,zz inertias

for ix in range(0,nbricks_on_x):
    for iy in range(0,nbricks_on_y):
        # create it
        body_brick = chrono.ChBody()
        # set initial position
        body_brick.SetPos(chrono.ChVectorD(ix*size_brick_x, (iy+0.5)*size_brick_y, 0 ))
        # set mass properties
        body_brick.SetMass(mass_brick)
        body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))
        # set collision surface properties
        body_brick.SetMaterialSurface(brick_material)

        # Collision shape
        body_brick.GetCollisionModel().ClearModel()
        body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
        body_brick.GetCollisionModel().BuildModel()
        body_brick.SetCollide(True)

        # Visualization shape, for rendering animation
        ChronoPandaInterface.PandaCube(cpi, body_brick,(size_brick_x, size_brick_y, size_brick_z),BRICK_ORANGE)


        my_system.Add(body_brick)


# Create the room floor: a simple fixed rigid body with a collision shape
# and a visualization shape

body_floor = chrono.ChBody()
body_floor.SetBodyFixed(True)
body_floor.SetPos(chrono.ChVectorD(0, -2, 0 ))
body_floor.SetMaterialSurface(brick_material)

# Collision shape
body_floor.GetCollisionModel().ClearModel()
body_floor.GetCollisionModel().AddBox(3, 1, 3) # hemi sizes
body_floor.GetCollisionModel().BuildModel()
body_floor.SetCollide(True)

# Visualization shape
ChronoPandaInterface.PandaCube(cpi, body_floor,(6, 2, 6),WHITE)

my_system.Add(body_floor)



# Create the shaking table, as a box

size_table_x = 1;
size_table_y = 0.2;
size_table_z = 1;

body_table = chrono.ChBody()
body_table.SetPos(chrono.ChVectorD(0, -size_table_y/2, 0 ))
body_table.SetMaterialSurface(brick_material)

# Collision shape
body_table.GetCollisionModel().ClearModel()
body_table.GetCollisionModel().AddBox(size_table_x/2, size_table_y/2, size_table_z/2) # hemi sizes
body_table.GetCollisionModel().BuildModel()
body_table.SetCollide(True)

# Visualization shape
ChronoPandaInterface.PandaCube(cpi, body_table,(size_table_x, size_table_y, size_table_z),GRAY)


my_system.Add(body_table)


# Create a constraint that blocks free 3 x y z translations and 3 rx ry rz rotations
# of the table respect to the floor, and impose that the relative imposed position
# depends on a specified motion law.

link_shaker = chrono.ChLinkLockLock()
link_shaker.Initialize(body_table, body_floor, chrono.CSYSNORM)
my_system.Add(link_shaker)

# ..create the function for imposed x horizontal motion, etc.
mfunY = chrono.ChFunction_Sine(0,1.5,0.001)  # phase, frequency, amplitude
link_shaker.SetMotion_Y(mfunY)

# ..create the function for imposed y vertical motion, etc.
mfunZ = chrono.ChFunction_Sine(0,1.5,0.12)  # phase, frequency, amplitude
link_shaker.SetMotion_Z(mfunZ)

# Note that you could use other types of ChFunction_ objects, or create
# your custom function by class inheritance (see demo_python.py), or also
# set a function for table rotation , etc.




# ---------------------------------------------------------------------
#
#  Create an Irrlicht application to visualize the system
#
camera_point = chrono.ChVectorD(0,0,0)
camera_pos = chrono.ChVectorD(3,3,3)
camera_dis =  camera_point - camera_pos 



cpi.camera.setPosHpr(camera_pos.x, camera_pos.y, camera_pos.z, 0, 0, 0)
cpi.SetCamera(camera_pos, camera_point)
#cpi.camera.setPosHpr(camera_pos.x, camera_pos.y, camera_pos.z, camera_angle.z, camera_angle.y, camera_angle.x) 

#cpi.camera.setPosHpr(0, 0, 4, camera_angle.z, camera_angle.y, camera_angle.x)

timestep = 0.005
t = 0
steps = 0


while(t<10):
    my_system.DoStepDynamics(timestep)
    if (steps%5 == 0):
           cpi.Advance()
    
    t+= timestep
    steps+=1

cpi.destroy()