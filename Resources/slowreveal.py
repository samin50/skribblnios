from array import *
from ast import For
import random

actualword = 'skribblio'
timeratio = 0.2


wordlength = len(actualword)
wordtoguessarray = array('u', ['_'])
for x in range(wordlength-1):
    wordtoguessarray.insert(1,'_')


if timeratio == 0.45:

    y = random.randint(0,wordlength-1)
    z = actualword[y]
    wordtoguessarray[y] = z


if timeratio == 0.7 and wordlength > 3 :

    w = random.randint(0,wordlength-1)
    while w == y:
        w = random.randint(0,wordlength-1)
    z = actualword[w]
    wordtoguessarray[w] = z
