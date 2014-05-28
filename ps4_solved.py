# Caesar Cipher Skeleton
# solves http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-2/lecture-10-hashing-and-classes/MIT6_00SCS11_ps4.pdf
# Dennis Ivy
# python3
import string
import random
#import itertools

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print ("  ", len(wordlist), "words loaded.")
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    assert -27 <= shift <= 27
    abc_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    abc_lower = abc_upper.lower()   #create a lowercase version
    upper = {}
    lower = {}
    for i in abc_upper: #for each character
        if (abc_upper.index(i) + shift) < len(abc_upper):   #if the shift doesn't run us out of bounds
            upper[i] = abc_upper[abc_upper.index(i) + shift] #set the key and the value of the dictionary upper and lower respectively
            lower[i.lower()] = abc_lower[abc_lower.index(i.lower()) + shift]
        else:   #if the shift does run us out of bounds
            diff=len(abc_upper)-(abc_upper.index(i) + shift)    #how much?
            upper[i] = abc_upper[ abs(diff) ] #restart the index at zero and set key value pairs
            lower[i.lower()] = abc_lower[ abs(diff) ]
    
    upper.update(lower)    #join the two dicts together
    return upper    #and return it

#print(build_coder(3))

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    return build_coder(shift)
    ### TODO.
#print(build_encoder(3))


def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    #coder=build_coder(shift)
    ##swap the keys and the values.
    #decoder={}
    #for i in coder: #for each value in the dictionary
    #    decoder[coder[i]] = i
    #return decoder
    return build_coder(-shift)
 
#print(build_decoder(3))

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    #print("text=",text,"coder=")
    #print(coder)
    abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    abc+=abc.lower()
    solution=''
    for i in text:
        if i in abc:
            solution+=coder[i]
        else:
            solution+=i
    return solution
    #'Hello, world!'   
#print(apply_coder("Hello, world!", build_encoder(3)))
#should output 'Khoor,czruog!'
#print(apply_coder("Khoor,czruog!", build_decoder(3)))
#should output 'Hello, world!'

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    alpha+=alpha.lower()

    coder=build_coder(shift)
    #print ("inside apply_coder, coder=",coder)
    cipher=''
    for i in text:
        if i in alpha:
            cipher += coder[i]
        else:
            cipher += i
    return cipher
#print(apply_shift("This is a test.", 8))
   



#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the shift needed to get plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    MAX_WORDS=0
    best_shift=None
    abc="ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    abc+=abc.lower()
    stripped_scrambled_text = ''
    for c in text:
        if c in abc:
            stripped_scrambled_text+=c
            
    for shift in range(0,27): #check each possible shift
        #print ("shift=",shift)
        #build the coder
        coder=build_decoder(shift)
        #shift the word
        possibly_unscrambled_text = apply_coder(stripped_scrambled_text,coder)
        #check if what we got back has words matching those in our wordist
        possible_word_list=possibly_unscrambled_text.split(" ")
        #for each resulting word...
        words_found=0
        for word in possible_word_list:
            #if so, success
            if word in wordlist:
                #print("Found the word '", word,"' at shift=",shift)
                words_found+=1
                #best_shift=shift
        if words_found > MAX_WORDS:
            MAX_WORDS=words_found
            best_shift=shift
    return shift
        


#s = apply_coder('Hello, world!', build_encoder(8))
#print("s=",s)
    #should output 'Pmttw,hdwztl!'

#shift = find_best_shift(wordlist, s) 
#returns 8
#print("shift=",shift)
#print(apply_coder(s, build_decoder(shift)))
    #outputs 'Hello, world!'
  
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    for i in shifts:
        #print("i=",i,"i[0]=",i[0],"i[1]=",i[1])
        location=i[0]
        shift=i[1]
        #build coder
        coder=build_coder(shift)
        #get the substring to which this particular shift should be applied
        sub_string=text[location:]
        #print("sub_string=",sub_string)
        #apply the shift
        shifted_substring = apply_coder(sub_string,coder)
        #print("shifted_substring=",shifted_substring)
        #set text equal to the new shifted substring prior to the next iteration.
        #print("text[:location]=",text[:location])
        text=text[:location]+shifted_substring
        #print("resulting text=",text)
    return text


#print(apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)]))
#outputs 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
 
#
# Problem 4: Multi-level decryption.
#
def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    #print("called my recursive function")
    #print("text=", text, "start=",start)
    ### TODO.
    ##theres a problem when a i look for a space and find a space as the very first character in tail...
        #print("TEXT when start=187=", text,"start=",start)
    list=[]
    #tuple=[]
    for shift in range(0,28):
        head=text[:start]
        #print("head=", head, "shift=",shift)
        tail=apply_shift(text[start:], shift)
        s=head+tail
        #s=text[:start]+apply_shift(text[start:],shift)
        space_found=tail.find(' ')
        #print("space_found=",space_found)
        if(space_found != -1):
            possible_word = tail[:space_found]
        else:
            possible_word=None
            #print("hmmm....head=",head)
        #if "second" in possible_word:
            #
            
        if possible_word != None:
            if is_word(wordlist,possible_word):
                #print("head=", head)
                #print("head=",head,"tail=",tail,"start=",start)
                #print("calling myself with s and space_found=",space_found)
                result=find_best_shifts_rec(wordlist,s,start+space_found+1)
                #print("result=",result,"head=",head)
                if result != None:
                    list=[(start,shift), result]
                    #list.append(result)
                    #print("result=",result)
                    return list
                #elif result==None:
                #    #?
                #    #break
                #    #?
                #    pass
        elif possible_word== None and is_word(wordlist,tail):
            #print("found the end bitch!!!")
            #print(text)

            return (start,shift)
        
        
        
    return None

def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    shifts=find_best_shifts_rec(wordlist,text,0)
    #print("Shifts=",shifts)
    #print("unwinding shifts...")
    result=[]
    #given a list containing a tuple, and a list of undetermined length
    while shifts:
        #print("len(shifts)=",len(shifts))
        if type(shifts) != tuple:
            temp=shifts.pop(0)
            #print("after the pop,temp=",temp)
            result.append(temp)
            if shifts != []: 
                shifts=shifts[0]
        else:
            #print("found a tuple")
            result.append(shifts)
            break
        #print("after assignment, result=",result)
        #shifts=temp
        
        #else: result.append(shifts)        
    #print ("result=",result)
    #input()
    return result
    #for e in shifts: #for each element of the shift array
    #    #print ("e=",e)
    #    if type(e) == list:
    #        #break it down into
    #        for j in e:

    #        pass
      
        
            
#s=random_scrambled(wordlist,3)
#print ("random scrambled string s=",s)

#s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
#shifts=find_best_shifts(wordlist,s)
#print("unscrambled string s=",apply_shifts(s,shifts))
#print("shifts=",shifts)
#currently works so long as what i get is a match but not necessarily the best match.

    


def decrypt_fable():
    text=get_fable_string()
    #print("text=",text)
    shifts=find_best_shifts(wordlist,text)
    #print("shifts=",shifts)
    print(apply_shifts(get_fable_string(),shifts))

decrypt_fable()


    
#What is the moral of the story?
#
#
#
#
#

