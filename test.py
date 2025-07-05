import string
import requests
import random
lines=[]
with open("FiveLetterWords.txt",'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]


rdmWord = random.choice(lines)
used_Word = []
d = dict()
l = dict()
notinWord = list()
while True:
    url = 'https://wordle-api.vercel.app/api/wordle'
    data = {
            "guess" : rdmWord
        }
    print(rdmWord)
    used_Word.append(rdmWord)
    response = requests.post(url,json=data)
    response = response.json()
    print(response)

    if(response['was_correct']==False):
        idx=0
        for elt in response['character_info']:
            if elt['scoring']['in_word']==True:
                if elt['scoring']['correct_idx']==True:
                    d.update({idx:elt['char']})
                else:
                    
                    if elt['char'] not in l:
                        l[elt['char']]=[]
                    l[elt['char']].append(idx)
            else:
                notinWord.append(elt['char'])
            idx+=1
    else:
        print(rdmWord)
        break
    print(d)
    print(l)
    print(notinWord)
    # break
    if(len(l)!=0 or len(d)!=0):

        st = ['','','','','']
        for i,ch in d.items():
            print("i=",i)
            st[i]=ch
            
        print(st)
        for ch , lst in l.items():
            for j in range(len(st)):
                if j not in lst and st[j]=='':
                    st[j]=ch
        rem_len = 5-len(d)-len(l)
        print("rem_len=",rem_len)
        i=0
        for k in range(5):
            if i<5:
                ch =random.choice(string.ascii_lowercase)           
                while ch in notinWord:
                    ch =random.choice(string.ascii_lowercase) 
                if i<len(st) and st[i] == '':
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
        print("newRandomWord  ",rdmWord)   
    else:

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
                               
