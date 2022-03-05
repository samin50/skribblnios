import random 

f = open("dictionary.txt", "r")
content = f.read()
Dictionary = content.split(",")
f.close()

word1 = random.choice(Dictionary)

word2 = random.choice(Dictionary)
while word2 == word1:
    word2 = random.choice(Dictionary)

word3 = random.choice(Dictionary)
while word3 == (word1 or word2):
    word3 = random.choice(Dictionary)
