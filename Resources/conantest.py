import random

actualword = 'mickey mouse'
timeratio = 0.45
space = actualword.find(" ")

wordlength = len(actualword)
wordtoguessarray = ['_']
for x in range(wordlength-1):
    wordtoguessarray.insert(1,'_')
if space != -1:
    wordtoguessarray[space] = " "


if timeratio == 0.45:
    timeratio = 0.7
    y = random.randint(0,wordlength-1)
    while y == space:
        y = random.randint(0,wordlength-1)
    z = actualword[y]
    wordtoguessarray[y] = z


if timeratio == 0.7 and wordlength > 3 :
    timeratio = 0
    w = random.randint(0,wordlength-1)
    while w == y or w == space:
        w = random.randint(0,wordlength-1)
    z = actualword[w]
    wordtoguessarray[w] = z

print(wordtoguessarray)