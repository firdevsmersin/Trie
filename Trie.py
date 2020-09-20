import sys
import os
import re
import glob

class Trie(object):
    def __init__(self):
        self.root = TrieNode(None,0)

    def add_word(self, word):
        """add word to trie"""
        self.root.add_word(word)
        self.root._add()
    def all_words_in_trie(self):
        """print all keys from tree in ascending order"""
        return self.root.all_words_in_trie()
           
    def find_by_word(self,word):
        """find given *word* in tree, if not occures None is returned"""
        return self.root.find_by_word(word)

  
    def find_by_pref(self,pref):
        """find number of words with given prefix *pref*"""
        return self.root.find_by_pref(pref)

    @property
    def children(self):
        return self.root.children
    
    def __repr__(self):
        return 'Root<%s>'%(self.root.children)

class TrieNode(object):
    def __init__(self, val, cnt = 1):
        #print("node oluştu:  ")
        self.__value = val
        self.__children = []
        #print("count %d:"% (cnt)+"\n")
        self.__count = cnt
        #self.__position = []

    
    @property
    def value(self):
        return self.__value

    @property
    def count(self):
        return self.__count
    
    @property
    def children(self):
        "returns list of childrens"
        return [x for x in self.__children]
    
    def _add(self):
        self.__count += 1

    def add_child(self,value,early_child=False):
        "add child and sort list of them"
        if early_child:
            tmpt = TrieNode(value)
            tmpt.__count -= 1
            self.__children.append(tmpt)
        else:
            self.__children.append(TrieNode(value))
        self.__children.sort()
    
    def add_word(self,word):
        "add word to node"
        if len(word)>1:
            s = word[0]
            word = word[1:]
            for c in self.children:
                if c.has_value(s):
                    #print("deger eklendi :"+word)
                    c._add()
                    c.add_word(word)
                    break
            else:
                
                self.add_child(s,True)
                self.add_word(s+word)
        else:
            #print("büyük else\n")
            s = word
            for c in self.children:
                if c.has_value(s):
                    c._add()
                    break
            else:
                self.add_child(s)

    def has_value(self,letter):
        "check if value occures"
        return self.__value == letter


    def find_by_word(self,word):
        "find *word* in node"
        nbr = 0
        node = self
        while nbr!=None:
            try:
                s = word[0]
            except IndexError:
                print ('try except')
                if node.count==sum([n.count for n in node.children]):
                    nbr=None
                break
            word = word[1:]
            for c in node.children:
                nbr+=c.count
                if c.has_value(s):
                    sumleft = sum([n.count for n in c.children])
                    if c.count!=sumleft:
                        nbr+= c.count-sumleft
                    nbr -= c.count
                    node = c
                    break
            else:
                nbr=None
            if len(node.children)<=0:
                break
        if nbr!=None and len(word)>0:
            nbr=None
        print("nbr "+nbr)
        return nbr

    def all_words_in_trie(self):
        lst = []
        val = self.__value
        if val == None: val=''
        for c in self.__children:
            lst.extend(c.all_words_in_trie())        
        lst = [val+x for x in lst]
        lstp = [val]*(self.__count-sum([n.count for n in self.children]))
        return lstp+lst 

    def find_by_pref(self,pref):
        "number of keys starting with prefix *pref* in node"
        node = self
        prefidx = 0
        while len(pref)>0:
            s = pref[0]
            pref = pref[1:]
            for c in node.children:
                if c.has_value(s):
                    prefidx = c.count
                    node=c
                    break
            else:
                return 0 
            if len(node.children)<=0:
                break
        if prefidx!=0 and len(pref)>0:
            prefidx=0
        return prefidx 
   
    def __repr__(self):
        return 'Trie<%s (%i)>'%(self.__value,self.__count)

    def __gt__(self, node2):
        return self.__value > node2.value
def readfile(file__):
   words=[]
   for n in re.findall(r"[\w']+", file__.read()):
       words.append(n.lower())
   return words
def pos(f):
    words=[]
    with open(f,'r') as file_:
        for line in file_:
            for word in line.split():
                words.append(word.lower())
    kelime=words[0]
    j=1
    for j in range(len(words)):
        kelime=kelime+" "+words[j]
        j=j+1
    return kelime
def check_files_exist(files,path):
    i=1 
    for b in range(len(files)):
        if(os.path.exists(path+files[b]))==0:
            print("There is no file such as named "+files[b])
            i=0
            break
    return   i 
def find_common(word,trie_obj):
    list1=word
    list2=trie_obj.all_words_in_trie()
    return set(list1)&set(list2)
def search_on_trie(words,trieob):
    common_words=find_common(words,trieob)
    if common_words == []:
        return []
    else:
        return common_words
def findprefix():
    i=-1
    while i<0:
        path =input("File path should be like below format: \nex: /home/firdevs/Desktop/datastructure/trie/sampleTextFiles/\nEnter file path : ")
        if(os.path.exists(path)):
             files = []
             # r=root, d=directories, f = files
             for r, d, f in os.walk(path):
                 for file in f:
                     if '.txt' in file:
                         files.append(os.path.join(r, file))
             if(len(files)==0):
                 print("There is no files to add trie!!!!\n")
             else:
                 i=1 # to stop while loop all requirements are ok.
                 prefix =input("Enter the prefix : ")
                 prefix=prefix.lower()
                 for f in files:
                     t=Trie()
                     file=open(f,'r+')#open current file to read
                     words=readfile(file)# this method extracts all words from current file
                     pos_=pos(f)
                     for word in words: #add all words to trie
                         t.add_word(word)
                     pref=t.find_by_pref(prefix)
                     if(pref==0):
                         print("")
                     else:
                         in_file=f.split('/')
                         print("> "+in_file[len(in_file)-1]+" -----> %d"%(pref)+" times")
                     del t #delete created Trie object
        else:
            print("Path doesn't exist\n")
def findcommon():
    i=-1
    while i<0:
        tries=[]
        path =input("File path should be like below format: \nex :/home/firdevs/Desktop/datastructure/trie/sampleTextFiles/\nEnter file path : ")
        p=path[len(path)-1]
        if(os.path.exists(path)and p=='/'):
            files=[]
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    files.append(path+file)
            if len(files)>0:
                i=1 # to stop asking path while loop condition
                #if all requirements are ok. then we create trie as many as number of files
                for t in range(len(files)):#create  trie objects as many as number of lenght of files
                    tries.append(Trie())
                #print("ddd %d"%len(tries))
                for t in range(len(files)):# this loop for filling the tries's inside
                    #print(files[t])
                    f = open(files[t],'r+')
                    words=readfile(f)
                    count=0
                    trieobject=tries[t]
                    for word in words:
                        trieobject.add_word(word)
                        #print(word)
                print("-----------------------------")
                tries_word=[]
                tries_word=tries[0].all_words_in_trie()
                for k in range(len(tries)):
                    if k==0: #we have already checked first trie object above so skip this step
                        print("")
                    else:
                        tries_word=search_on_trie(tries_word,tries[k])
                        if tries_word=='\0':
                            print("No common words!!! \n")
                            break # if there is no common words in first two files
                            # not need to check rest of objects
                if len(tries_word)==0:
                    print("No common words!!! \n")
                else:
                    print("IN GIVEN FILES, COMMON WORDS ARE :")
                    print(tries_word)         
                        
            else:
                print("There is no file to check in given path !!!\n")
        else:
            print("Path doesn't exist\n")

if __name__ == '__main__':
    i=1
    while i>0:
        choose = input('\n------------------------------\nChoose one query:\n 1 : find prefix\n 2 : find common words\n 3 : exit\n-----------------------------\n')
        if choose == '1':
            findprefix()
        elif choose == '2':
            findcommon()
        elif choose =='3':
            print("PROGRAM IS END, BYE :)")
            break
        else:
            print("INCORRECT CHOICE !!!\n")
    
    