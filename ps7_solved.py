# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name: Dennis Ivy
# solves http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-2/lecture-16-using-randomness-to-solve-non-random-problems/MIT6_00SCS11_ps7.pdf

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        prob = random.random()
        return prob < self.clearProb
    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        prob = random.random()
        #print("prob=",prob,"popDensity",popDensity, "maxBirth=",self.maxBirthProb)
        if self.maxBirthProb * (1-popDensity) > prob:
            #print("had a baby")
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        for e in self.viruses:#for each list element
            if e.doesClear():#if it does clear (true)
                self.viruses.remove(e)#remove it from the list, else do nothing
        #calc pop density
        popDensity = self.getTotalPop() / self.maxPop
        for r in self.viruses:#for all remaining viruses
            try:#if the virus reproduces, add it to the list
                self.viruses.append(r.reproduce(popDensity))
            except:#else it raises an exception where nothing happens really
                #print(r,"didn't reproduce this round")
                pass
        return self.getTotalPop()

    
#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    #locals
    viruses=[]
    seed_viruses=100
    maxBirthProb=0.1
    clearProb=0.05
    timeStep=300
    maxPop=1000
    data_points=[]

    #create the viruses
    for i in range (0,seed_viruses): 
        viruses.append(SimpleVirus(maxBirthProb,clearProb))
    #create the patient
    patient=SimplePatient(viruses,maxPop)
    #run the simulation to get the data
    for tick in range (0,timeStep):#for the appropriate number of steps...
        data_points.append( patient.update() )

    #print results
    #print("viruses=",viruses)

    #plot the results
    pylab.plot(data_points)
    pylab.title("Total Virus Population as a Function of Time")
    pylab.xlabel("Time in Hours")
    pylab.ylabel("Virus Population")
    pylab.show()

simulationWithoutDrug()
def rollDie(num_sides):
    try:
        assert type(num_sides)==int
    except:
        raise TypeError
    return random.choice(range(1,num_sides+1))

def Yahtzee():
    #for each die
    turn=[]
    for e in range(0,5):
        turn.append(rollDie(6))#roll a six sided die
    #print ("turn=",turn)
    return turn
def dubSix(max_turns):
    #get the data
    #max_turns=10000
    #results=[]
    yahtzee=0
    for i in range(0,max_turns):
        result=Yahtzee()
        #print ("Yahtzee()=",result)
        if result == [6, 6, 6, 6, 6]:
            yahtzee+=1
    #calculate the probability...
    print("yahtzee=",yahtzee)
    return yahtzee/max_turns

#print((1/6)**5)
#print(dubSix(500000))
