from math import modf
from copy import copy

chunk = lambda ulist:  map(lambda i: ulist[i-1:i+1],  xrange(0, len(ulist), 1))

class Enumeration(object):
    def __init__(self, names):
        for number, name in enumerate(names.split("|")):
            setattr(self, name, number)

def toStrList(l):
    return ', '.join(map(str, l))

def get_row(l,row):
    nl = []
    for i in xrange(len(l)):
        nl += [l[i][row]]
    return nl

def sortx(a,b):
    if a.x<b.x:return -1
    elif a.x>b.x:return 1
    else:return 0

def sorty(a,b):
    if a.y<b.y:return -1
    elif a.y>b.y:return 1
    else:return 0

def sortz(a,b):
    if a.z<b.z:return -1
    elif a.z>b.z:return 1
    else:return 0

def to_maya_sel(prefix,l):
    l.sort()
    nl=[[l[0]]]
    for i in xrange(1,len(l)):
        if nl[-1][-1]+1==l[i]:nl[-1]+=[l[i]]
        else:nl+=[[l[i]]]
    for i in xrange(len(nl)):
        if len(nl[i])>2: nl[i]=[nl[i][0],nl[i][-1]]
    st = []
    for i in xrange(len(nl)):
        #pPlane1.vtx[3:8]
        if len(nl[i])==1:
            st += [prefix+"["+str(nl[i][0])+"]"]
        else:
            st += [prefix+"["+str(nl[i][0])+":"+str(nl[i][1])+"]"]
    #l=[0,1,4,5,6,7,8,18,12,11,15]
    #print listToMayaSel("Pplane01.vtx",l)
    #select -r pPlane1.vtx[3:8] pPlane1.vtx[11:16] pPlane1.vtx[20:24] pPlane1.vtx[30:32] pPlane1.vtx[40:41] ;
    return st

def enumerate_list(c,offset=0):
    e=[]
    for i in xrange(len(c)):
        e+=[i+offset]
    return e

def enumerate_number(n,offset=0):
    e=[]
    for i in xrange(n):
        e+=[i+offset]
    return e

def offset(c,offset=0):
    e=[]
    for i in xrange(len(c)):
        e+=[c[i]+offset]
    return e

def remove_valuez(l,value):
    find = 0
    n=copy(l)
    while find>-1:
        find = find(n,value)
        if find>-1: n.pop(find)
    if not n:n=[]
    return n

def cycle(l,cycles):
    for i in xrange(0,cycles):
        first_to_last = l[0]
        l.pop(0)
        l.append(first_to_last)
    return l 

def find(l,x):
    i=0
    while i<len(l):
        if l[i]==x:
            return i
        i+=1
    return -1

def group_by_1st(l):
    def sort_my(a,b):
        if a[0]>b[0]: return 1
        elif a[0]==b[0]: return 0
        else: return -1
    l1=copy(l)
    l1.sort(sort_my)
    r=[]
    e=l1[0][0]
    r.append(l1[0])
    for i in xrange(1,len(l1)):
        if e==l1[i][0]:
            r[len(r)-1].extend(l1[i][1:])
        else:
            e=l1[i][0]
            r.append(l1[i])
    return r

def remove_duplicates(l1,l2):
    lt = copy(l1)
    for i in xrange(0,len(l2)):
        try:
            ind = lt.index(l2[i])
            lt.pop(ind)
        except:
            pass
    return lt

def leave_duplicates(l1,l2):
    l=[]
    lt = copy(l1)
    for i in xrange(0,len(l2)):
        try:
            ind = lt.index(l2[i])
            l.append(lt[ind])
            lt.pop(ind)

        except:
            pass
    return l

def group_duplicates(l):
    l_new = []
    for i in xrange(len(l)):
        id = find(l_new,l[i])
        if id==-1:
            l_new.append(l[i])
    return l_new

def to_pairs(l):
    #[0,1,2,3]=>[[0,1][2,3]]
    nl=[]
    for i in xrange(1,len(l)/2+1):
        nl.append([l[i*2-2],l[i*2-1]])
    return nl

def to_edges(l):
    #[0,1,2,3]=>[[0,1][1,2][2,3][3,0]]
    edges = []
    for i in xrange(len(l)):
        if i ==len(l)-1:
            edges+=[[l[i],l[0]]]
        else:
            edges+=[[l[i],l[i+1]]]
    return edges

def duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

class CycleList():
    def __init__(self,li):
        self.list=copy(li)
    def __str__(self):
        return str(self.list)
    def __len__(self):
        return len(self.list)
    def fixkey(self,key):
        len1=float(len(self.list))
        nkey = key-modf(key/len1)[1]*len1
        if nkey<0:nkey=len1+nkey
        return int(nkey)
    def __getitem__(self, key):
        key=self.fixkey(key)
        return self.list[key]
    def __setitem__(self, key, value):
        key=self.fixkey(key)
        self.list[key]=value
    def __add__(self,other):
        self.list+=other
    def __sub__(self,other):
        return remove_duplicates(self.list,other)
    def __getslice__(self, i, j):
        i=self.fixkey(i)
        if j<10e10:
            j=self.fixkey(j)
        if i>j:i,j=j,i
        return CycleList(self.list[i:j])
    def find(self,key):
        return find(self.list,key)
    def group(self):
        return CycleList(group_duplicates(self.list))
    def pop(self,key):
        self.list.pop(key)
    def append(self,value):
        self.list.append(key)
    def extract(self,id,value):
        #self.list[id].extract(key)
        pass
    def cycle(self,cycles):
        cycle(self.list,cycles)
    def reverse(self):
        return CycleList(self.list[::-1])