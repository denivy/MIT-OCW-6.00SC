# Dennis Ivy
# solves http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-1/lecture-7-debugging/MIT6_00SCS11_ps3.pdf
# Python 3
import random
import string
import itertools

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
WORDLIST_FILENAME = "words.txt"

def xcombinations(items, n):
    if n==0: yield []
    else:
        for i in range(0,len(items)):
            for cc in xcombinations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in range(0,len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
            
def xselections(items, n):
    if n==0: yield []
    else:
        for i in range(0,len(items)):
            for ss in xselections(items, n-1):
                yield [items[i]]+ss

def xpermutations(items):
    return xcombinations(items, len(items))

def get_perms(hand, n):
    handlist = []
    
    for key in hand:
        for i in range(hand[key]):
            handlist.append(key)

    l = [] 
    toret = []

    for c in xuniqueCombinations(handlist,n):
        l.append(c)

    for j in l:
        for p in xpermutations(j):
            toret.append("".join(p))

    return toret

def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    score=0
    word=False
    valids={}
    for j in range(0,calculate_handlen(hand)):
        # get permutations:
        toret=get_perms(hand, calculate_handlen(hand)-j)
        #print ("toret=",toret)
        for i in toret:#for each item in toret
            #print("i=",i)
            #assert false
            if is_valid_word(i,hand,word_list) == True:
                #print("found a valid word-->i=",i)
                word_score=get_word_score(i, HAND_SIZE)
                #add it to the dict
                valids[i] = word_score
                
                if word_score > score:
                    word=i
                    score=word_score

                
    #print("word=",word,"score=",score)
    
    #now that i have a dictionary of all possible valid words, search for the play that give me the highest score
    #print(itertools.permutations(valids.values()))
    #print("valids=",valids)
    #print ("valids.values=",valids.values())
    for y in range(0,len(valids)):
        #could do something that checks to see what each possible permutation is of word_n + word_n-1 ... + word_0 to see if
        #some combination could maybe be better!
        pass
    #input("waiting")
    return word

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """

    #so this function sort of works, except there may be a case where the highest score does not come from playing the lognest word first,
    #followed by any remaining possible words
    #but instead comes from playing a shorter word, followed by another remaining word that is longer than the words played following the longest word

    score=0
    print("Current Hand:",display_hand(hand))
    while calculate_handlen(hand) != 0:
        word=comp_choose_word(hand,word_list)
        #i get back a dictionary here
        if word == False:
            #found no more words to play
            break
        #consider all possible outcomes.
        print("Computer Plays:",word)
        if is_valid_word(word,hand,word_list) == True:
            word_score = get_word_score(word,HAND_SIZE)
            print_stars()
            print("Computer's word score:",word_score)
            print_stars()
            score += word_score
            hand=update_hand(hand,word)
        elif word == '.':
            break
        else:#if its not a valid word
            print("that word is not in my dictionary...try again")
            print_stars()
    print_stars()
    print("Computer's Hand Score:",score)
    print_stars()
    # TO DO ...    
    
#
# Problem #6C: Playing a game
#
#

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print ("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    list=[]
    score=0
    #move string into a list
    for i in range (0,len(word)): #for every letter in word
        score += SCRABBLE_LETTER_VALUES[ word[i] ]
        #print("score=",score," word[i]=",word[i]," scrabble_letter_value=",SCRABBLE_LETTER_VALUES[ word[i] ])
        #list.append(word[i]) #add it to a list
    score *= len(word)
    if len(word) == n:
        score+=50
    return score

def test_get_word_score():
    """
    Unit test for get_word_score
    """
    failure=False
    # dictionary of words and scores
    words = {("", 7):0, ("it", 7):4, ("was", 7):18, ("scored", 7):54, ("waybill", 7):155, ("outgnaw", 7):127, ("outgnawn", 8):146}
    for (word, n) in words.keys():
        score = get_word_score(word, n)
        if score != words[(word, n)]:
            print ("FAILURE: test_get_word_score()")
            print ("\tExpected", words[(word, n)], "points but got '" + str(score) + "' for word '" + word + "', n=" + str(n))
            failure=True
    if not failure:
        print ("SUCCESS: test_get_word_score()")

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    hand_str=""
    for letter in hand.keys():
        for j in range(hand[letter]):
            hand_str += letter 
            #print (letter)              # print all on the same line
    #print(hand_str)                               # print an empty line
    return hand_str

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = int(n / 3)
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #print("hand=",hand)
    for i in range(0,len(word)): #for ever leter in word
        hand[ word[i] ]-=1
        #print ("after update : i=",i, "word[i]=",word[i],"hand[",word[i],"]=",hand.get(word[i],hand)) #dict accessor
    return hand

def test_update_hand():
    """
    Unit test for update_hand
    """
    # test 1
    hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    word = "quail"

    hand2 = update_hand(hand.copy(), word)
    expected_hand1 = {'l':1, 'm':1}
    expected_hand2 = {'a':0, 'q':0, 'l':1, 'm':1, 'u':0, 'i':0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print ("FAILURE: test_update_hand('"+ word +"', " + str(hand) + ")")
        print ("\tReturned: ", hand2, "-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function
        
    # test 2
    hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "evil"

    hand2 = update_hand(hand.copy(), word)
    expected_hand1 = {'v':1, 'n':1, 'l':1}
    expected_hand2 = {'e':0, 'v':1, 'n':1, 'i':0, 'l':1}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print ("FAILURE: test_update_hand('"+ word +"', " + str(hand) + ")")
        print ("\tReturned: ", hand2, "-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function

    # test 3
    hand = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    word = "hello"

    hand2 = update_hand(hand.copy(), word)
    expected_hand1 = {}
    expected_hand2 = {'h': 0, 'e': 0, 'l': 0, 'o': 0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print ("FAILURE: test_update_hand('"+ word +"', " + str(hand) + ")")
        print ("\tReturned: ", hand2, "-- but expected:", expected_hand1, "or", expected_hand2)
        
        return # exit function

    print ("SUCCESS: test_update_hand()")

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    valid=False
    #copy of dict
    hand_copy = hand.copy() #needed to make sure we do not accidently mutate hand
    #hand_copy['b']=30
    #print ("hand=",hand,"hand_copy=",hand_copy)
    #handstr=""
    #print("".join(hand))
    #print(hand.values())
    #for i in range(0,len(hand.values())):#for each element in hand
    #    #check to see if 
    #    print("i=",i,"hand.values=")
    #    #handstr += i*hand[i]
    #print ("handstr",handstr)
    #is wword composed entirely of characters 
    for i in range(0,len(word)):    #for each letter in word
        #print ("i=",i, "word[i]=",word[i],"hand[",word[i],"]=",hand.get(word[i],hand)) #dict accessor
        #hand.find(word[i])
        if hand_copy.get(word[i]):
            #print("hand_copy.get(word[i]) is true")
            hand_copy[ word[i] ] -= 1
            #print("new hand_copy=",hand_copy)            
        else:
            #print("its false")
            return False
        
    if word in word_list:   #is the word in the word list
        return True
    else:
        return False

def test_is_valid_word(word_list):
    """
    Unit test for is_valid_word
    """
    failure=False
    # test 1
    word = "hello"
    hand = get_frequency_dict(word)

    if not is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected True, but got False for word: '" + word + "' and hand:", hand)

        failure = True

    # test 2
    hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}
    word = "rapture"

    if  is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True        

    # test 3
    hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if  not is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True                        

    # test 4
    hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
    word = "honey"

    if  is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        
        failure = True

    # test 5
    hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "evil"
    
    if  not is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected True, but got False for word: '" + word + "' and hand:", hand)
        
        failure = True
        
    # test 6
    word = "even"

    if  is_valid_word(word, hand, word_list):
        print ("FAILURE: test_is_valid_word()")
        print ("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        print ("\t(If this is the only failure, make sure is_valid_word() isn't mutating its inputs)")
        
        failure = True        

    if not failure:
        print ("SUCCESS: test_is_valid_word()")

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    score=0
    word=''
    while word != '.' and calculate_handlen(hand) != 0:
        print("Current Hand:",display_hand(hand))
        word=input("Enter a word ('.' exits): ")
        if is_valid_word(word,hand,word_list) == True:
            word_score = get_word_score(word,HAND_SIZE)
            print_stars()
            print("word score:",word_score)
            print_stars()
            score += word_score
            hand=update_hand(hand,word)
        elif word == '.':
            break
        else:#if its not a valid word
            print("that word is not in my dictionary...try again")
            print_stars()
    print_stars()
    print("Hand Score:",score)
    print_stars()
 
def print_stars():
    print("*" * 30)

def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hands_played=0
    game_score=0
    print("Welcome to the word game!")
    print_stars()
    userChoice = input("n for new game, or e for exit: ")
    while userChoice != 'e':
        print_stars()
        who=input("u for user, c for computer: ")
        print_stars()
        if who=='u':
            if userChoice == 'n':
                hand=deal_hand(HAND_SIZE)
                play_hand(hand.copy(), word_list)
                hands_played += 1  
            elif userChoice == 'r' and hands_played != 0: # if its a valid input            
                play_hand(hand.copy(),word_list)
            else:
                print('you had one job...try again and enter a valid choice')

        elif who=='c':
            print("computer's got this one!")
            if userChoice=='n':
                hand=deal_hand(HAND_SIZE)
                comp_play_hand(hand.copy(),word_list)
                hands_played+=1
            elif userChoice == 'r' and hands_played != 0:
                comp_play_hand(hand.copy(),word_list)
            else:
                print('you had one job...try again and enter a valid choice')

        else:
            print('you had one job...try again and choose a valid option')
        
        userChoice = input("Enter n for new, r for replay, e for exit: ")
    print_stars()        
    print("goodbye!")
    print_stars()
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """


# Build data structures used for entire session and play game

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
#hand={  'b':1,'e':1,'r':2  }
#is_valid_word("berry",hand, word_list)
#test_is_valid_word(word_list)
