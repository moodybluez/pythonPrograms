'''
Created on Sep 17, 2014

@author: ntiller
'''

'''worked with Andrew King'''

from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import math

def foldInfo(df):
    foldSize = len(df)/10
    remainder = len(df) % 10
    dfTest = []
    i = 0
    start = 0
    while i < 10:
        if remainder != 0:
            dfTest.append(df[start : start+foldSize+1])
            remainder -= 1
            start = start + foldSize + 1
        else:
            dfTest.append(df[start : start+foldSize])
            start = start + foldSize
        i+= 1
            
    return dfTest

def probabilityOfValue(attr, val, classification, df):
    df = df[df.classification == classification]
    denom = float(len(df.index))
    numer = float(len(df[df[attr] == val].index))
    if numer/denom == 0:
        return 0.0001
    return (numer / denom)
    
    
def constructProbabilityTable(df):
    fullArray = {}
    classifications = np.unique(df.classification)
    for attr in df.columns:
        attrArray = {}
        if attr != 'classification':
            for val in np.unique(df[attr]):
                classificationArray = {}
                for clss in classifications:
                    classificationArray[clss] = probabilityOfValue(attr, val, clss, df)
                attrArray[val] = classificationArray
        fullArray[attr] = attrArray
    return fullArray


def findProbabilities(testdf, traindf):
    resultsArray = []
    dictArray = []
    classifications = np.unique(traindf.classification)

    columns = traindf.columns

    # HERE IS THE IMPORTANT LINE. THIS FINDS ALL PROBABILITIES AND SAVES THEM
    classificationArray = constructProbabilityTable(traindf)
    i = 0            
    for index in range(len(testdf.index)):
        instance = testdf.iloc[index][:-1]
        
        
        classificationDict = {}
        totalProbability = 0.0
        for classification in classifications:
            prob = 1.0
            for col in columns[:-1]:
                # Compute the probability of a attribute/value pair existing given a classification
                # prob *= float(probabilityOfValue(col, instance[col], classification, traindf))
                prob *= classificationArray[col][instance[col]][classification]


            # Create the last probability: how often a classification occurs given all instances
            classificationCount = len(traindf[traindf.classification == classification].index) 
            prob *= classificationCount / float(len(traindf.index))

            # Save this into a dictionary keyed off of the classification
            classificationDict[classification] = prob
            totalProbability += prob

        # normalize the probabilities
        highest = 0
        bestKey= ''
        for key, value in classificationDict.items():
            classificationDict[key] /= totalProbability
            if value > highest:
                highest = value
                bestKey = key
        dictArray.append(classificationDict)
        resultsArray += bestKey
    quadLoss = quadraticLoss(dictArray, testdf)
    informLoss = infoLoss(dictArray, testdf)
    return resultsArray, quadLoss, informLoss

def quadraticLoss(df, dfTest):
    for index in df:
        for element in dfTest['classification']:
            for key, value in index.items():
                if key == element:
                    value = value - 1
    lossSum = 0
    i = 0
    for index in df:
        for key, value in index.items():
            i +=1 
            lossSum += (value * value)
    print i
    return lossSum

def infoLoss(df, dfTest):
    lossSum = 0
    for index in df:
        for element in dfTest['classification']:
            for key, value in index.items():
                if key == element:
                    value = -np.log2(value)
    i = 0
    for index in df:
        for key, value in index.items():
            i +=1 
            lossSum += value
    print i
    return lossSum
    
def main():
    df = pd.read_csv('mushroom.csv', header=0)

    
    # Here is simple code to move the first column to the last spot. 
    cols = df.columns.tolist()
    print cols
    cols = cols[1:] + cols[:1]
    cols = cols[13:]
    print cols
    df = df[cols]
    print df
    '''
    Generate testing data
    
    Last column is our classification!
    '''
    ####### THIS SHOULD NOT EXIST IN YOUR FINAL CODE #########

    dfTotal = foldInfo(df)

    ##########################################################
    
        
    # Example
    averageError = 0
    quadraticLossTotal = 0
    infoLossTotal = 0
    for i in range(10):
        dfTest = dfTotal[i]
        dfTrain = None
        for j in range(10):
            if j != i:
                if dfTrain is None:
                    dfTrain = dfTotal[j].copy()
                else:
                    dfTrain = dfTrain.combine_first(dfTotal[j])   
        guesses, quadLoss, infoLoss = findProbabilities(dfTest, dfTrain)
        quadraticLossTotal += quadLoss
        infoLossTotal += infoLoss
        i = 0
        error = 0
        for element in dfTest['classification']:
            if element != guesses[i]:
                error += 1
            i +=1
        error = float (error)/ i
        averageError += error
    averageError = averageError/10
    print "Average Error Is"
    print averageError
    print "Total Quadratic Loss"
    print quadraticLossTotal
    print "Info Loss"
    print infoLossTotal
    
    
    
    
if __name__ == '__main__':
    main()
