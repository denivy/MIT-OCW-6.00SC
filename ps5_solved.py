# Dennis Ivy 
# 6.00 Problem Set 5
#http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-2/lecture-12-introduction-to-simulation-and-random-walks/MIT6_00SCS11_ps5.pdf
# RSS Feed Filter
#import lib2to3
import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word=word
    def is_word_in(self, text):
        lword = self.word.lower()
        #print("pre-text=",text)
        text=text.lower()
        #make sure we get a string
        try:
            assert type(text) == str
        except:
            raise TypeError("word trigger is_word_in method requires a string")
        #strip slashes/whateva
        for c in text:
            if c in string.punctuation:
                text=text.replace(c,' ')
        #print("post-text=",text)
        word_list=text.split(' ')
        #print ("word_list=",word_list)
        #print ("lword=",lword)
        for i in word_list:
            #print("i=",i)
            if lword == i:
                return True
        return False
        #raise ValueError

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self,news_story):
        return self.is_word_in(news_story.title)

class SubjectTrigger(WordTrigger):
    def evaluate(self, news_story):
        return self.is_word_in(news_story.subject)
           
class SummaryTrigger(WordTrigger):
    def evaluate(self, news_story):
        return self.is_word_in(news_story.summary)

# Composite Triggers
# Problems 6-8
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.other=other_trigger
    def evaluate(self, story):
        return not self.other.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, other1,other2):
        self.other1=other1
        self.other2=other2
    def evaluate(self,story):
        return self.other1.evaluate(story) and self.other2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, other1, other2):
        self.other1=other1
        self.other2=other2
    def evaluate(self, story):
        return self.other1.evaluate(story) or self.other2.evaluate(story)
        
# Phrase Trigger
# Question 9
class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase=phrase
        #print("setting self.phrase=",self.phrase)
    def evaluate(self, story):
        for x in [story.get_subject(),story.get_title(), story.get_summary()]:
            if self.phrase in x:
                #print("found it!")
                return True
        return False

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    filtered_list=[] #array of stories to return
    # TODO: Problem 10
    for s in stories:#for each element in stories
        for t in triggerlist:
            if t.evaluate(s) == True:
                filtered_list.append(s)

    # Feel free to change this line!
    return filtered_list

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    args= [e.split(' ') for e in lines]
    trigger_type=[]
    triggers=[]
    d={}
    #print("args=",args)
    #get an array of trigger types whose indices correspond to the indices in args
    for i in args:
        for j in i:
            if j.isupper():
                trigger_type.append(j)
            #get the first occurance of a name in format 'tX' where x is a number
    for x in trigger_type:
        if x in ['TITLE','SUBJECT','PHRASE']:
            #get the index and use it to access args
            index=args[trigger_type.index(x)]
            name = index[0]
            words = " ".join(index[2:])            
            #print("d=",d)
            if x=='TITLE':                
                d[name] = TitleTrigger(words)
                triggers.append(d[name])
                #print("t1=",t1)
                #print("triggers=",triggers)                
            elif x=='SUBJECT':
                d[name] = SubjectTrigger(words)
                triggers.append(d[name])
            elif x=='PHRASE':
                d[name] = PhraseTrigger(words)
                triggers.append(d[name])
            else:
                raise UnboundLocalError('ralph fail english? thats unpossible!')
            #print('index=',index,'name=',name,'words=',words)
            #create title trigger and add it to the trigger list
        if x=='AND':
            index=args[trigger_type.index(x)]
            name=index[0]
            other1=index[2]
            other2=index[3]
            d[name] = AndTrigger(d[other1],d[other2])
            pass
    #print("triggers=",triggers)
    return triggers
    
import _thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    #t1 = SubjectTrigger("Obama")
    #t2 = SummaryTrigger("MIT")
    #t3 = PhraseTrigger("Supreme Court")
    #t4 = OrTrigger(t2, t3)
    triggerlist = readTriggerConfig("triggers.txt")
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    #triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print ("Polling...")

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print ("Sleeping...")
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    _thread.start_new_thread(main_thread, (p,))
    p.start()

