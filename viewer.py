#!/usr/bin/python

import OpenGL.GL as gl
import yarp as y
import sys, pygame
import time
from math import sin
from numpy.linalg import inv
from numpy import array, identity, cos , sin, dot, invert, pi
from avispy.engine import Camera, Scene, Light, Display, Primitive, Object_model, rotx, roty, rotz
import avispy.objects_lib as objects_lib

xyz_inc=0.1
rot_inc=1*pi/180.0


camera=Camera()
size= 640,480
scene=Scene()
display=Display(camera,scene,res=size)

light0=Light(Light.LIGHTS[0])
light0.position=array([10.,10.,10.,1.0])
scene.add_light(light0)

light1=Light(Light.LIGHTS[1])
light1.position=array([-10.,10.,10.,1.0])
scene.add_light(light1)

light2=Light(Light.LIGHTS[2])
light2.position=array([0.,-10.,10.,1.0])
scene.add_light(light2)

light3=Light(Light.LIGHTS[3])
light3.position=array([0.,0.,-10.,1.0])
scene.add_light(light3)


bar=objects_lib.Bar()
bar.set_sides(1.6,1.5)
bar.set_pos(array([2.,1.,0.]))
bar.set_color(array([0.0,0.,1.]))
scene.add_object(bar)


sphere=objects_lib.Sphere()
sphere.set_radius(0.3)
sphere.set_pos(array([1.,1.,1.]))
sphere.set_color(array([0.,2.,0.]))
scene.add_object(sphere)


curve=objects_lib.Curve()
curve2=objects_lib.Curve()
curve3=objects_lib.Curve()
curve2.set_y_offset(-2.0)
curve3.set_y_offset(-2.0)
curve.set_color(array([1.,0.,0.]))
curve2.set_color(array([0.,1.,0.]))
curve3.set_color(array([0.,0.,1.]))
curve.set_color_reflex(array([1.,0.,0.]),shininess=0.0)
curve2.set_color_reflex(array([0.,1.,0.]),shininess=0.0)
curve3.set_color_reflex(array([0.,0.,1.]),shininess=0.0)
#curve.set_x_interval(2.0)
plot=objects_lib.Plot()
plot.add_curve(curve)
plot.add_curve(curve2)
plot.add_curve(curve3)
plot.set_pos(array([3.,3.,3.]))
plot.scale=[4.,4.,1.0]
scene.add_object(plot)


camera_center=objects_lib.Disk()
camera_center.set_color(array([0.5,0.5,0.5]))
camera_center.set_color_reflex(array([1.,1.,1.]),50.0)
camera_center.visibility=False
scene.add_object(camera_center)

#Adding objects
#world_frame=objects_lib.Frame()
#scene.add_object(world_frame)
#test_frame=identity(4)

world_bar=objects_lib.Bar()
scene.add_object(world_bar)
test_bar=identity(4)


counter=0.0
counter2=-1.0


# yarp part


portname_in =  "/gui/in"
portname_out =  "/gui/out"
y.Network.init()
port_out = y.BufferedPortBottle()
port_in = y.BufferedPortBottle()
port_out.open(portname_out)
port_in.open(portname_in)



while True:

    bottle = port_in.read()
    position = bottle.get(0).asDouble()
    speed = bottle.get(1).asDouble()
    axial_position = bottle.get(2).asDouble()
    acceleration = bottle.get(3).asDouble()



#for i in xrange(10):
    time.sleep(0.01)
    for event in pygame.event.get():
        #print event
        if event.type == pygame.QUIT or (event.type ==pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()
        #camera events:
        if event.type == pygame.MOUSEMOTION or event.type ==pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            camera.update(event)
            camera.camera_matrix.get_frame() #TODO, this is done twice innecessarly
            val=camera.camera_matrix.radius*0.01
            camera_center.set_pos(inv(camera.camera_matrix.center_rot_frame)[:,3][:3])
            camera_center.scale=[val,val,1.0]
            if event.type == pygame.MOUSEMOTION :
                if event.buttons == (1,0,0) or event.buttons == (0,0,1):
                    camera_center.visibility=True
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4 or event.button ==5:
                    camera_center.visibility=True

    #testing curve
    counter+=0.1
    counter2+=0.1
    if counter2>1.0:
        counter2=-1.0
    #test_frame[:3][:,:3]=rotx(position)
    #world_frame.trans_rot_matrix=test_frame
    curve.add_point(array([counter,cos(position),0.1]))
    curve2.add_point(array([counter,sin(position),0.0]))


    test_bar[:3][:,:3]=rotx(axial_position)
    world_bar.trans_rot_matrix=test_bar
    bar.set_length(2)
   
    world_bar.set_length(3)
    world_bar.set_sides(0.4,0.4)
    world_bar.set_pos(array([1.,1.,1.]))
    world_bar.set_color(array([1.0,1.,1.]))
    display.update()
    camera_center.visibility=False
