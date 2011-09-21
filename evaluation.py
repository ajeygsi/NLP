#!/usr/bin/python
import spell_checker
file = 'commonmisspelled.txt'

f = open(file)
error = []
correct = []
for line in f:
    error.append(line.split()[0])
    correct.append(line.split()[1])

meanReciprocalRank = 0
avgTime = 0.0
for i in range(len(error)):
    suggestions = spell_checker.correct(error[i])
    #avgTime += time
    reciprocalRank = 0.0
    for j in range(5):
        if suggestions[j][0] == correct[i]:
            reciprocalRank = 1.0/(j+1)
            break
    meanReciprocalRank += reciprocalRank
    print i

#print float(avgTime)/len(error)
print float(meanReciprocalRank)/len(error)
