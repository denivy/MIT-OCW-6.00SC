import numpy
import random
import pylab
from ps7 import *

class ResistantVirus(SimpleVirus):

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):

        #print("in isResistantTo, drug=",drug,"resistances=", self.resistances)
        if drug in self.resistances.keys():
            #print('found drug=',drug,"resistance=",self.resistances[drug])
            return self.resistances[drug]
        else:
            print("this drug=",drug,"was not found in the current list of keys",self.resistances.keys() )
            raise NotImplementedError


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        #print("Function Entered! resistances=", self.resistances)
        #input()
        #print ("activeDrugs=",activeDrugs)
        child_resistances={} #determine the resitances of the potential child...
        for i in self.resistances: #for each resitance carried by the parent (self)
            
            prob = random.random() #get a random number
            #print("i=",i,"self.resistances[i]=",self.resistances[i],"prob=",prob, "mutProb=",self.mutProb, "1-self.mutProb=",1-self.mutProb)
            if prob < 1-self.mutProb: #if this resistance is to be passed on from child to parent
                #print("should be set to true")
                child_resistances[i]=self.resistances[i] #add this resitance to the child as active
            else: #otherwise, it has no resistance 
                child_resistances[i]=not self.resistances[i]

        #print("child_resistances=",child_resistances)
        if activeDrugs == {}: #if activeDrugs is an empty list...then the virus reproduces normally.
            prob = random.random() #create a random number
                #print("popDensity=",popDensity)
            if self.maxBirthProb * (1 - popDensity) > prob: #does it reproduce this time?
                #print("had a baby")                    
                return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances , self.mutProb)
            else:
                raise NoChildException
        else: #if drugs ARE being taken...I need to do something different.
            reproduce=0
            for e in activeDrugs:   #for each active drug
                #print("e=",e)
                if self.isResistantTo(e): #determine resistance
                    #print("found a virus thats resistant to e=",e)
                    #print("self.resistances=",self.resistances)
                    #input()
                    reproduce += 1
            if reproduce == len(activeDrugs):
                reprob = random.random()
                if reprob < self.maxBirthProb * (1 - popDensity):   #if it does reproduce (i.e., resistance is too low)
                    return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)#not sure about how to define mutation probability...
                else:#if its not resistant to the drug, then it is sterilized by said drug and does not reproduce
                    raise NoChildException
            else:
                raise NoChildException

class Patient(SimplePatient):

    
    def __init__(self, viruses, maxPop):
    
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = {}

    def addPrescription(self, newDrug):

        if newDrug not in self.drugs:
            self.drugs[newDrug] = True
        else:
            raise DrugAlreadyUsedException
        # should not allow one drug being added to the list multiple times


    def getPrescriptions(self):

        return self.drugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count=0
        #print ("drugResist=",drugResist)
        #print ("self.viruses=",self.viruses)
        
        if len(drugResist) == 0:
            raise ValueError

        for v in self.viruses:#look at every virus...
            #print("v=",v)
            if type(v) != ResistantVirus or v == None: #if its not the right type, obviously it shouldn't be added to the count...
                raise TypeError
            for drug in drugResist:#look at every drug in the list
                #print("drug=",drug)
                if v.isResistantTo(drug):#if this virus is resistant to this particular drug
                    add_this_virus = True
                else:
                    add_this_virus = False #if this virus is NOT resistant to this particular drug, don't add it 
                    #print("setting add_this_virus to False")
            if add_this_virus == True: # if this virus should be added
                count += 1 #increment the counter
        return count

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        #print ( "BEFORE clear, totalPop=",self.getTotalPop(),"resistPop=",self.getResistPop(['guttagonol']) )
        for i in self.viruses: #look at each virus
            if i.doesClear():
                self.viruses.remove(i)
        #print ( "AFTER  clear, totalPop=",self.getTotalPop(),"resistPop=",self.getResistPop(['guttagonol']) )
        popDensity = self.getTotalPop() / self.maxPop #calc population density
        #print ("maxPop=",self.maxPop,"totalPop=",self.getTotalPop(),"popDensity=",popDensity)
        for r in self.viruses: #for all remaining viruses
            try: #try to append it
                #print("attempting to add a child,")
                self.viruses.append(   r.reproduce( popDensity, self.getPrescriptions() )   )
            except: #if it fails...which it should 90 percent of the time really...
                #print("no child created")
                pass #ignore the exception
        #print ( "AFTER reproduce, totalPop=",self.getTotalPop(),"resistPop=",self.getResistPop(['guttagonol']) )
        #input("Enter to Continue")
        return self.getTotalPop()



#
# PROBLEM 2
#

def simulationWithDrug():

    viruses = []
    seed_viruses = 100
    maxBirthProb = 0.1 #ten percent chance of reproducing at any given step
    clearProb = 0.05 #five percent chance of being removed at any given step
    timeStep = 150
    maxPop = 1000
    resistances = { 'guttagonol' : False }
    mutProb = 0.005 #.5 % chance of mutation.  if it does mutate, it will change its resistance
    data_points_total = []
    data_points_resistant = []

    #create the viruses
    for i in range ( 0, seed_viruses ): 
        viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )
    #create the patient
    patient = Patient(viruses,maxPop)
    #print ("patient created, perscriptions=",patient.getPrescriptions(),"totalPop=", patient.getTotalPop(),"resistPop=",patient.getResistPop(resistances))
    #run the simulation to get the data
    for tick in range (0,0):#for the appropriate number of steps...
        data_points_total.append( patient.update() )
        data_points_resistant.append( patient.getResistPop(['guttagonol']) )
    #introduce the drug
    #print( "totalPop=",patient.getTotalPop(),"resistPop=",patient.getResistPop(resistances) )
    #input("adding the drug...press enter to continue ")
    patient.addPrescription('guttagonol')
    for tick in range (0,timeStep):#for the remaining ticks
        data_points_total.append( patient.update() )
        data_points_resistant.append( patient.getResistPop(['guttagonol']) )
    #print ("scripts=",patient.getPrescriptions(),"totalPop=", patient.getTotalPop())
    #print results
    #print("viruses=",viruses)
    pylab.plot(data_points_total)
    pylab.plot(data_points_resistant)
    #pylab.plot(data_points_resistant_virus)
    pylab.title("Total Virus Population and Resistant Virus Population as a Function of Time")
    pylab.xlabel("Time in Hours")
    pylab.ylabel("Virus Population")
    pylab.show()
    
#simulationWithDrug()

#
# PROBLEM 3
#        

def simulationDelayedTreatment(preTime):
    #print("preTime=",preTime)
    viruses = []
    seed_viruses = 100
    maxBirthProb = 0.1 #ten percent chance of reproducing at any given step
    clearProb = 0.05 #five percent chance of being removed at any given step
    timeStep = 150
    maxPop = 1000
    resistances = { 'guttagonol' : False }
    mutProb = 0.005 #.5 % chance of mutation.  if it does mutate, it will change its resistance
    #create the viruses
    for i in range ( 0, seed_viruses ): 
        viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )
    #create the patient
    patient = Patient(viruses,maxPop)
    print('        +init totalPop=',patient.getTotalPop(),'resistPop=',patient.getResistPop(['guttagonol']) )
    #print ("patient created, perscriptions=",patient.getPrescriptions(),"totalPop=", patient.getTotalPop(),"resistPop=",patient.getResistPop(resistances))
    #run the simulation to get the data
    for tick in range (0,preTime):#for the appropriate number of steps...
         patient.update() 
    print('        +pre totalPop=',patient.getTotalPop(),'resistPop=',patient.getResistPop(['guttagonol']) )
    #introduce the drug
    #print( "totalPop=",patient.getTotalPop(),"resistPop=",patient.getResistPop(resistances) )
    #input("adding the drug...press enter to continue ")
    patient.addPrescription('guttagonol')
    for tick in range (0,timeStep):#for the remaining ticks
        patient.update() 
    #print ("scripts=",patient.getPrescriptions(),"totalPop=", patient.getTotalPop())
    print('        +post totalPop=',patient.getTotalPop(),'resistPop=',patient.getResistPop(['guttagonol']) )
    return ( patient.getTotalPop(), patient.getResistPop(['guttagonol']) )
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

def histograms():
    results=[]
    for i in [0,75,150]: #for each starting time....
        print("Getting Results for",i)
        sum=[]
        for x in range (1,4):
            print("   -trial",x)
            sum.append( simulationDelayedTreatment(i) )
        
        avgTotal=0
        avgResist=0

        for y in sum:
            avgTotal  += y[0]
            avgResist += y[1]
        print("appending",avgTotal/len(sum),avgResist/len(sum),"to results")
        results.append((avgTotal/len(sum), avgResist/len(sum)))
        results2=pylab.array(results)/x
        pylab.hist(results2)
        pylab.xlabel('Total Virus')
        pylab.ylabel('Resistant Virus')
        pylab.show()

#histograms()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():
    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    viruses = []
    seed_viruses = 100
    maxBirthProb = 0.1 #ten percent chance of reproducing at any given step
    clearProb = 0.05 #five percent chance of being removed at any given step
    timeStep = 300
    maxPop = 1000
    resistances = { 'guttagonol' : False , 'ivycillin' : False }
    mutProb = 0.005 #.5 % chance of mutation.  if it does mutate, it will change its resistance
    data_points_total = []
    data_points_resistant = []

    #create the viruses
    for i in range ( 0, seed_viruses ): 
        viruses.append( ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) )
    #create the patient
    patient = Patient(viruses,maxPop)
    print ( "patient created,\
    perscriptions=",patient.getPrescriptions(),\
    "totalPop=", patient.getTotalPop(),\
    "resistPop=",patient.getResistPop(['guttagonol', 'ivycillin']) )
    #run the simulation to get the data
    for tick in range (0,300):#for the appropriate number of steps...
        data_points_total.append( patient.update() )
        data_points_resistant.append( patient.getResistPop(['guttagonol', 'ivycillin']) )
    #introduce the drug
    print( "totalPop=",patient.getTotalPop(),"resistPop=",patient.getResistPop(resistances) )
    input("adding both drugs guttagonol and ivycillin...press enter to continue ")
    patient.addPrescription('guttagonol')
    patient.addPrescription('ivycillin')
    for tick in range (0,300):#for the remaining ticks
        data_points_total.append( patient.update() )
        data_points_resistant.append( patient.getResistPop(['guttagonol', 'ivycillin']) )
    print ("scripts=",patient.getPrescriptions(),"totalPop=", patient.getTotalPop())
    #print results
    #print("viruses=",viruses)
    pylab.plot(data_points_total)
    pylab.plot(data_points_resistant)
    #pylab.plot(data_points_resistant_virus)
    pylab.title("Total Virus Population and Resistant Virus Population as a Function of Time")
    pylab.xlabel("Time in Hours")
    pylab.ylabel("Virus Population")
    pylab.show()

simulationTwoDrugsVirusPopulations()
