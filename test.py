import string
import requests
import random
lines=[]
with open("FiveLetterWords.txt",'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines] 
    ''' 
    line.strip will remove the \n and white space from start and end of the strings
    '''
print(lines)

rdmWord = random.choice(lines)
# select a random word out of the list
used_Word = []  
''' to store the used word so that we not process them again  '''
d = dict() 
''' stores the chars that are present at the correct index in the final string '''
l = dict() 
''' stores the chars which are in the final string but not at their correct index . Also stores the indices where the particular char must not be placed '''
notinWord = list()  
'''  to store the chars that are not present in the final string   '''
while True:
    url = 'https://wordle-api.vercel.app/api/wordle'
    data = {
            "guess" : rdmWord   
            
        }
    ''' checks if the random word selected is the answer '''
    print(rdmWord)
    used_Word.append(rdmWord) 
    ''' storing so that we not use this word again  '''
    response = requests.post(url,json=data)
    response = response.json()
    print(response)

    if(response['was_correct']==False):   
        ''' => word was not correct. the api sends the json data about which char were present and which were at the correct index . We use this data to form the new rdmWord efficiently  '''
        idx=0
        for elt in response['character_info']:
            if elt['scoring']['in_word']==True:  
                ''' if the char is present in the original answer '''
                if elt['scoring']['correct_idx']==True:  
                    ''' if this char is present at the correct index as that in the original answer then this char must be present at the same index in the new random word '''
                    d.update({idx:elt['char']})
                else:                             
                    ''' => char is present but not at the correct index '''
                    if elt['char'] not in l:   
                        ''' as the same char can be used more than once in the final string so we have a dictionary mapping char to the list of indices '''
                        l[elt['char']]=[]
                    l[elt['char']].append(idx)
            else:
                notinWord.append(elt['char']) 
            idx+=1
    else:             
        ''' We found the answer string '''
        print(rdmWord)
        break
    print(d)
    print(l)
    print(notinWord)
    # break
    if(len(l)!=0 or len(d)!=0): 
        ''' if we have some chars which should be in the answer string then we use them to create the new guess string otherwise we use random function again '''

        st = ['','','','',''] 
        ''' to help in creation of new guess string   '''
        for i,ch in d.items(): 
            ''' placing the chars which are at the correct index in the final string '''
            print("i=",i)
            st[i]=ch
            
        print(st) 
        for ch , lst in l.items(): 
            ''' placing the char ch at the position apart from the ones in the list lst ''' 
            for j in range(len(st)):
                if j not in lst and st[j]=='': 
                    st[j]=ch
        rem_len = 5-len(d)-len(l)   
        ''' number of chars left to place '''
        print("rem_len=",rem_len)
        i=0  
        ''' denotes the 0th index in the list st '''
        for k in range(5):
            ''' to fill the remaining positions in the list st'''
            if i<5:
                ch =random.choice(string.ascii_lowercase) 
                ''' chooses a lowercase char  '''          
                while ch in notinWord:
                    ch =random.choice(string.ascii_lowercase) 
                if i<len(st) and st[i] == '':  
                    ''' found an empty place to put a new char not yet used '''
                    st[i]=ch
                    i+=1
                else:
                    while i<len(st) and st[i]!='':
                        i+=1
                    if(i<len(st)):
                        st[i]=ch
                        i+=1
        # rdmWord=str(st) 
        rdmWord=''.join(st)    
        ''' converting the list st to string and assigning it to rdmWord '''
        print("newRandomWord  ",rdmWord)   
    else:  
        ''' if the dictionary l and d are empty then create a new string not containing the chars in notinWord '''
        rdmWord = random.choice(lines)
        flag = True
        while True:
            for ch in rdmWord:
                if ch in notinWord:
                    flag = False
                    break
            if flag==False or rdmWord in used_Word:
                rdmWord = random.choice(lines)
            else:
                break
                               
