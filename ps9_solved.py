
# 6.00 Problem Set 9
#
# Intelligent Course Advisor
# solves http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-3/lecture-20-more-clustering/MIT6_00SCS11_ps9.pdf
# Name: Dennis Ivy
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1
from operator import itemgetter
import itertools

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects={}
    inputFile = open(filename)
    for line in inputFile:
        #print ("line=",line)
        name,value,work = line.split(',')
        #print("name=",name,"value=",value,"work=",work)
        subjects[name]=(int(value),int(work))
    #print("subjects=",subjects)
    return subjects

#print(loadSubjects("subjects.txt"))

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print (res)

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    #print("subInfo1[0]=",subInfo1[0],"subInfo2[0]=",subInfo2[0])
    if subInfo1[0] > subInfo2[0] : return True
    else : return False
    #return lambda x:x[1]

#print ( cmpValue( (5,6),(7,8) ) )
def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    #print("subInfo1=",subInfo1,"subInfo2=",subInfo2)
    if subInfo1[1] < subInfo2[1] : return True
    else : return False

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    if subInfo1[0]/subInfo1[1] > subInfo2[0]/subInfo2[1] : return True
    else : return False
def cmpSum(subInfo1, subInfo2):

    assert type(subInfo1) == tuple, "Arguments to comparator should be tuples"
    assert type(subInfo2) == tuple, "Arguments to comparator should be tuples"
    return sum(subInfo1) > sum(subInfo2)

def greedyAdvisor(subjects, maxWork, comparator):
    
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    #print("maxWork=",maxWork,"comparator=",comparator, "subjects=", subjects)#debug
    #input()
    ###########################################################
    try: 
        assert type(subjects) == dict and maxWork >=0
    except (Exception,e):
        raise Exception
    ###########################################################
    
    subjects_copy = subjects.copy()
    if comparator == cmpValue:
        subjects_copy=sorted(subjects.items(), key=lambda x: x[1][0], reverse=True)
        #for x in sorted(subjects.items(), key=lambda x : x[1][0] , reverse=True):
            #print ("x=",x, "name=",x[0],"value=",x[1][0],"work=",x[1][1] )#debug
    elif comparator == cmpWork:
        subjects_copy = sorted(subjects.items(), key=lambda x: x[1][1])
        #for x in sorted(subjects.items(), key=lambda x : x[1][1], reverse=True) :
            #print ("x=",x, "name=",x[0],"value=",x[1][0],"work=",x[1][1] )#debug
    elif comparator == cmpRatio:
        subjects_copy = sorted(subjects.items(), key=lambda x: x[1][0] / x[1][1], reverse=True)
        #for x in sorted(subjects.items(), key=lambda x: (x[1][0] / x[1][1]), reverse=True ):
            #print ("x=",x, "name=",x[0],"value=",x[1][0],"work=",x[1][1], "ratio=",x[1][0]/x[1][1] )#debug
    elif comparator == cmpSum:
        subjects_copy = sorted(subjects.items(), key=lambda x: (x[1][0] + x[1][1]), reverse=True )
        #for x in sorted(subjects.items(), key=lambda x: (x[1][0] + x[1][1]), reverse=True ):
            #print ("x=",x, "name=",x[0],"value=",x[1][0],"work=",x[1][1], "sum=",x[1][0]+x[1][1] )#debug
    else:
        raise NotImplementedError
    #input()
    total_work=0
    results={}
    i=0
    while(total_work <= maxWork and i < len(subjects_copy)):
        course=subjects_copy[i]
        name=course[0]
        value=int(course[1][0])
        work=int(course[1][1])
        #print("total_work=",total_work,"course=",course,"work=",work,"value=",value,"name=",name)
        #print("total_work=",total_work,"course=",course,"course[0]=", course[0], "course[1]=",course[1], "course[1][0]=",course[1][0],"course[1][1]=", course[1][1])
        if total_work + work > maxWork:
            i+=1
            continue
        results[name]=(value,work)
        total_work += work
        #print("total_work=",total_work)
        i+=1
    #print("results=",results)
    return results

#print(greedyAdvisor(loadSubjects("shortened_subjects.txt"),50,cmpRatio))
#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    
    #print("subjects=",len(subjects),"maxWork=",maxWork)
    #input()
    bestSet = None
    bestValue=0
    pset=powerset(subjects) #now a have a powerset of all possible key combinations.
        
    #print("got power set...now step thru and find the best")
    for i in pset:#for each element in the power set...i.e. for each possible combination of keys.
        #check to see if this set maximizes our objective function.
        #print ("i=",i)#debug
        currentWork=0
        for e in i:#for each element in this particular subset
            #print ("e=",e,"subjects[e]=",subjects[e])
            name=e
            value=subjects[e][0]
            work=subjects[e][1]
            #print("name=",e,"value=",value,"work=",work)
            currentWork += work     #calculate the currentWork
        if currentWork == maxWork:   #if the current work is AN optimal solution, return the current set...
            #print("FOUND optimal match at i=",i)
            #input()
            bestSet=i
            break
        elif currentWork < maxWork: #else, if its potentially the best option.
            #set the bestValue to current Work and the best Set to i
            if currentWork > bestValue:    #check to see if it beats the previous best
                bestValue=currentWork
                bestSet = i
            #else: continue #if its too big...then it won't do..so continue
    #if we made it thru the entire powerset and didn't find an exact match, then send the best match
    #print("Made it thru pset...should now have the best set in i")#build a dictionary to return
    #print("bestValue=",bestValue,"bestSet=",bestSet)
    #input()
    result={}
    for x in bestSet:
        result[x] = subjects[x]
    #print("returning result=",result)
    #input()
    return result
    

def powerset(subjects):
    s=list(subjects)
    try:
        return itertools.chain.from_iterable( itertools.combinations(s,r) for r in range(len(s) +1) )
    except:
        pass
    
