# Problem Set 6: Simulating robots
# solves http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-2/lecture-14-sampling-and-monte-carlo-simulation/MIT6_00SCS11_ps6.pdf
# Name: Dennis Ivy

import math
import random
import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        #set class vars
        self.width=width
        self.height=height
        #initialze the array
        self.room = {}
        # a value of false means the tile is dirty
        for x in range(0,width):
            for y in range(0,height):
                self.room[(x,y)]=False
        
        #print("room=",self.Room)
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        #can only clean full tiles, not partial tiles...
        self.room[(int(pos.x),int(pos.y))]=True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        try:
            #print ("type(m,n)=",type(m,n))
            assert type(m)==int
            assert type(n)==int
        except:
            raise TypeError("isTileCleaned accepts only integers")
        return self.room[(m,n)]
        
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.room)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count=0
        for i in self.room:
            #print("i=",i)
            if self.room[i]==True:
                count+=1
        return count

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        #get a random x and a random y
        
        return Position( random.choice( range(0,self.width) ), random.choice( range(0,self.height) ) )


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if self.width > pos.x > 0 and self.height > pos.y > 0:
            return True
        else:
            return False

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed=speed
        self.room=room#?necessary?
        self.location=self.room.getRandomPosition()
        self.direction=random.choice(range(0,360))
        #self.room.cleanTileAtPosition(self.location)


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.location
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.location=position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction=direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        if self.room.isPositionInRoom(self.location.getNewPosition(self.direction,self.speed)) == True: #if the new position would be in the room
            self.setRobotPosition( self.location.getNewPosition(self.direction,self.speed) )# then do it.
        else:#if its out of the room,
            self.setRobotDirection( random.choice( range(0,360) ) ) #get a new random direction
            self.updatePositionAndClean()#and try again
            #now that we are back, with our updated new position...
        #clean that tile
        self.room.cleanTileAtPosition(self.location)

def Tests():
    #print("creating a room...")
    #room = RectangularRoom(10,10)
    #print("numTiles=",room.getNumTiles())
    #print("cleanTiles=",room.getNumCleanedTiles())
    #print("creating a position...")
    #pos1=Position(5,5)
    #print("is tile clean...should get false", room.isTileCleaned(pos1.getX(), pos1.getY()))
    #print("cleaning the tile at the position")
    #room.cleanTileAtPosition(pos1)
    #print("is tile clean, should get true...",room.isTileCleaned(pos1.getX(), pos1.getY()))
    #print("cleanTiles=",room.getNumCleanedTiles())
    #print("room contains a valid position...should get true...",room.isPositionInRoom(pos1))
    #pos2=Position(5000,5000)
    #print("room contains an invalid position...should get false...",room.isPositionInRoom(pos2))
    #print("random location inside the room....")
    #pos3=room.getRandomPosition()
    #print("pos3=",pos3)#got some kind of object...
    #print("check if its a valid position...should get true...",room.isPositionInRoom(pos3))
    #print
    #print("Creating a robot!....")
    #sbot1= StandardRobot(room,1)
    #print("sbot1=",sbot1)
    #initial_pos=sbot1.getRobotPosition()
    #print("direction=",sbot1.getRobotDirection(),"position=(",sbot1.getRobotPosition().getX(),",",sbot1.getRobotPosition().getY(),")")
    #print("it should have cleaned a square in the room...")
    #print("should get 2...cleanTiles=",room.getNumCleanedTiles())
    #print("make sure it cleaned the right square...should get true...",room.isTileCleaned(sbot1.location.getX(), sbot1.location.getY()))
    #print("move the robot")
    #sbot1.updatePositionAndClean()
    #print("direction=",sbot1.getRobotDirection(),"position=(",sbot1.getRobotPosition().getX(),",",sbot1.getRobotPosition().getY(),")")
    #print("did it move to a new square?")
    #if initial_pos.getX() == int( sbot1.getRobotPosition().getX() ) and initial_pos.getY() == int( sbot1.getRobotPosition().getY() ):
    #    print("Nope")
    #else:print("Yep...well maybe... at least not no...")
    #print("it should have cleaned a square in the room...")
    #print("should get 3...cleanTiles=",room.getNumCleanedTiles())
    #print("make sure it cleaned the right square...should get true...",room.isTileCleaned(int(sbot1.location.getX()), int(sbot1.location.getY())))
    #print("make sure we still have the correct number of tiles")
    #print("numTiles=",room.getNumTiles())
    #works, but with unexpected consequences of returning float positions...lets see how this develops i guess
    #seems to be working, but lets try it for 10 times.
    #prior to test, lets zero everything out again...
    print("creating a room...")
    room = RectangularRoom(20,20)
    print("Creating a robot!....")
    sbot1= StandardRobot(room,1)
    #print("sbot1=",sbot1)
    initial_pos=sbot1.getRobotPosition()
    #print("direction=",sbot1.getRobotDirection(),"position=(",sbot1.getRobotPosition().getX(),",",sbot1.getRobotPosition().getY(),")")
    print("it should have cleaned a square in the room...")
    print("numTiles=",room.getNumTiles(), "cleanTiles=",room.getNumCleanedTiles())
    print("move the robot 10 times")
    for i in range(0,10):
        print("sbot1.location=(",sbot1.getRobotPosition().getX(),",",sbot1.getRobotPosition().getY(),")")
        sbot1.updatePositionAndClean()
        print("did it move to a new square?")
        if initial_pos.getX() == int( sbot1.getRobotPosition().getX() ) and initial_pos.getY() == int( sbot1.getRobotPosition().getY() ):
            print("Nope")
        else:print("Yep")
    print("make sure we still have the correct number of tiles")
    print("numTiles=",room.getNumTiles())
    print("cleanTiles=",room.getNumCleanedTiles())

    

    #print("room=",room.room)


#Tests()

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    sum=0 #init counter
    
    for e in range(0,num_trials):#for each trial
        ticks=0
        #print(e)
        room=RectangularRoom(width,height)  #create a room
        target = room.getNumTiles() * min_coverage  #set the target
        #print ("target=",target)
        bots=[] #create a container for the number of robots
        #trial_average=0
        #create some robots
        for r in range(0,num_robots):#create the correct number and type of robots.
            if robot_type == StandardRobot:
                bots.append(StandardRobot(room,speed))
            elif robot_type == RandomWalkRobot:
                bots.append(RandomWalkRobot(room,speed))
        #print("bots created=",len(bots))
        #print("bots[]=",bots)    
        #print("running trial number",e)
        ##################################################################
        anim=ps6_visualize.RobotVisualization(num_robots,width,height,0)#
        ##################################################################
        while room.getNumCleanedTiles() < target:#until the room is clean enough
            ticks+=1    #count the number of ticks
            for m in range(0,len(bots)):#move each bot
                bots[r].updatePositionAndClean()
            ########################
            anim.update(room,bots)#
            ########################
        sum+=ticks
        #############
        anim.done()#
        #############
    return sum/num_trials

    #raise NotImplementedError
#print("average time for 1 robot on  1x1  to 100%=",runSimulation(1,1,1,1,1,100,StandardRobot))
#print("average time for 1 robot with speed 1 on  5x5  to 100%=",runSimulation(1,1,5,5,1,20,StandardRobot))
#print("average time for 1 robot with speed 1 on 10x10 to  75%=",runSimulation(1,1,10,10,0.75,20,StandardRobot))
#print("average time for 1 robot with speed 1 on 10x10 to  90%=",runSimulation(1,1,10,10,0.90,20,StandardRobot))
print("average time for 1 robot with speed 1 on 20x20 to 100%=",runSimulation(1,1,20,20,1,20,StandardRobot))

#print("average time for 1 robot with speed 2 on  5x5  to 100%=",runSimulation(1,2,5,5,1,20,StandardRobot))
#print("average time for 1 robot with speed 2 on 10x10 to  75%=",runSimulation(1,2,10,10,0.75,20,StandardRobot))
#print("average time for 1 robot with speed 2 on 10x10 to  90%=",runSimulation(1,2,10,10,0.90,20,StandardRobot))
#print("average time for 1 robot with speed 2 on 20x20 to 100%=",runSimulation(1,2,20,20,1,20,StandardRobot))

#print("average time for 1 robot with speed .5 on  5x5  to 100%=",runSimulation(1,0.5,5,5,1,20,StandardRobot))
#print("average time for 1 robot with speed .5 on 10x10 to  75%=",runSimulation(1,0.5,10,10,0.75,20,StandardRobot))
#print("average time for 1 robot with speed .5 on 10x10 to  90%=",runSimulation(1,0.5,10,10,0.90,20,StandardRobot))
#print("average time for 1 robot with speed .5 on 20x20 to 100%=",runSimulation(1,0.5,20,20,1,20,StandardRobot))

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    data_points=[] 
    for i in range(1,11):   #for anywhere from 1 to 10 robots
        print("calling simulation for num_robots=",i)
        data_points.append((runSimulation(i,1,10,10,1,5,StandardRobot),i))

    print("plotting")

    pylab.title("cleaning time to number of robots with speed 1 for a 10x10")
    pylab.ylabel("Time")
    pylab.xlabel("Number of Robots")
    pylab.plot(data_points)
    pylab.show()


#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    data_points=[] 
    for dimensions in [(20,20),(25,16),(40,10),(50,8),(100,4)]:   #for any of these dimensions
        print("calling simulation for dimensions=",dimensions, "width=",dimensions[0],"height=",dimensions[1])
        data_points.append((runSimulation(2,1,dimensions[0],dimensions[1],0.8,5,StandardRobot),dimensions[1]))

    print("plotting")

    pylab.title("80% cleaning 2 robots with speed 1 for various dimensions")
    pylab.ylabel("Time")
    pylab.xlabel("Height")
    pylab.plot(data_points)
    pylab.show()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        #get a random direction
        self.direction = random.choice(range(0,360))
        if self.room.isPositionInRoom(self.location.getNewPosition(self.direction,self.speed)) == True: #if the new position would be in the room
            self.setRobotPosition( self.location.getNewPosition(self.direction,self.speed) )# then do it.
        else:#if its out of the room,
            self.setRobotDirection( random.choice( range(0,360) ) ) #get a new random direction
            self.updatePositionAndClean()#and try again
            #now that we are back, with our updated new position...
        #clean that tile
        self.room.cleanTileAtPosition(self.location)



# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    
    for robot_type in [StandardRobot,RandomWalkRobot]:
        data_points=[] 
        print("Simulating for",robot_type)
        for i in range(1,11):   #for anywhere from 1 to 10 robots
            print("num_robots=",i)
            data_points.append((runSimulation(i,1,20,20,0.8,5,robot_type),i))
            pylab.plot(data_points)

    print("plotting")

    pylab.title("Comparing Robot Types")
    pylab.ylabel("Time")
    pylab.xlabel("Number of Robots")
    
    pylab.show()
    
#showPlot3()
