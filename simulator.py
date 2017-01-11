#!/usr/bin/python
import time
import yarp as y

i= float(raw_input("Enter the current value\n"))                         # Input current reference


# Declaration of Initial Values
position= 0.0
speed= 0.0
acceleration= 0.0
friction = 0.001
inertia = 0.02
cycle_period = 0.06
alfa = 5.0
radio = 1
axial_position = 0.0


# Motor model with lambda function
motor1 = lambda i: alfa*i



# Function with position, velocity and acceleration calculations
def update_state (position,axial_position,speed,acceleration,delta_t,i,motor1,alfa):


            torque = motor1(i)                                                  # Ask for torque function
            next_acceleration = (torque - (speed*friction))/inertia             # General acceleration formula
            next_speed = (next_acceleration * delta_t )+ speed                  # Speed is increased
            next_position = (next_speed * delta_t) + position                   # Position is increased
	    next_axial_position = ((next_speed * delta_t) + axial_position)*radio

            acceleration = next_acceleration                                    # Update with next acceleration
            speed = next_speed                                                  # Update with next speed
            position = next_position                                            # Update with next position
            axial_position = next_axial_position

            if(position >= 360):
	       position = position - 360

            print "a: ", acceleration,
            print "v: ", speed,
            print "p: ", position,
	    print "pa: ", axial_position,
     

            return(position,axial_position,speed,acceleration)

# Main Program

def main():

# yarp inicialization

    y.Network.init()             # Defining y as the yarp network
    port_out = y.BufferedPortBottle()
    port_in = y.BufferedPortBottle()
    portname_out = "/motor/out"  # defining motor/out as and communication outport 
    portname_in = "/motor/in"    # defining motor/in as and communication inport 
    
    portguin_out = "/write"      # defining yarp communication ports
    portguin_in = "/gui/in"      # defining yarp communication ports
    style = y.ContactStyle()     # The way to handle the conection 
    style.persisten = 1          # Permanente conection style 
    port_out.open(portname_out)  # openning out ports
    port_in.open(portname_in)    # openning out ports
    y.Network.connect(portname_out, portguin_in, style) #connecting yarp ports to each other
    y.Network.connect(portguin_out, portname_in, style) #connecting yarp ports to each other

    

# Time delay program for the setting of the motor parameters
    global t,  t_last, delta_t # Defines the time variables as global
    t_last = t
    t = time.time()
    first_t=float(t)   # Time variable to print the time taken in second for each cycle.

    delta_t = t - t_last

    position1,axial_position1,speed1,acceleration1=update_state(position,axial_position,speed,acceleration,delta_t,i,motor1,alfa) # apdate all variables with new values

    while True:

        t_last = t
        t = time.time()
        delta_t = t - t_last
        print "t: ",t-first_t, " delta t: ", delta_t # excecute time
        position1,axial_position1,speed1,acceleration1=update_state(position1,axial_position1,speed1,acceleration1,delta_t,i,motor1,alfa)  # apdate all variables with new values

        bottle=port_out.prepare()            # prepering the variable to be send
        bottle.clear()                       # cleaning the state of bottle
        bottle.addDouble(position1)          # send position variable through yarp
        bottle.addDouble(speed1)             # send speed variable through yarp 
        bottle.addDouble(axial_position1)    # send axial_positionvariable through yarp
        bottle.addDouble(acceleration1)      # send acceleration variable through yarp  
        port_out.write()


        T_tempo = time.time()
        Tsleep = cycle_period - (T_tempo - t)
        time.sleep(Tsleep)

        



t_last= time.time()
t = time.time()


main()
