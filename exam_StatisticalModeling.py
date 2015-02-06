'''
Created on Oct 23, 2014

@author: t93rockhead
'''
import pandas as pd
import numpy as np
from pandas import Series
import matplotlib.pyplot as plt

'''this method takes a df and computes the average values for each column for each classification, then checks
each value to see if it's above or below the average. If it's above the average it changes the value to 1, if 
it's below the average it changes the value to 0'''
def makeNominalValues(df):
    
    dfAreaMin = df['area'].min()
    dfAreaMax = df['area'].max()
    dfAverageArea = (dfAreaMax + dfAreaMin)/2
    
    dfPerimeterMin = df['perimeter'].min()
    dfPerimeterMax = df['perimeter'].max()
    dfAveragePerimeter = (dfPerimeterMax + dfPerimeterMin)/2
    
    dfCompactnessMin = df['compactness'].min()
    dfCompactnessMax = df['compactness'].max()
    dfAverageCompactness = (dfCompactnessMax + dfCompactnessMin)/2
    
    dfLenMin = df['length'].min()
    dfLenMax = df['length'].max()
    dfAverageLen = (dfLenMax + dfLenMin)/2
    
    dfWidthMin = df['width'].min()
    dfWidthMax = df['width'].max()
    dfAverageWidth = (dfWidthMax + dfWidthMin)/2
    
    dfCoeffMin = df['coeff'].min()
    dfCoeffMax = df['coeff'].max()
    dfAverageCoeff = (dfCoeffMax + dfCoeffMin)/2
    
    dfGrooveLengthMin = df['grooveLength'].min()
    dfGrooveLengthMax = df['grooveLength'].max()
    dfAverageGrooveLength = (dfGrooveLengthMax + dfGrooveLengthMin)/2
    
    i = 0
    for vals in df['area']:
        if vals < dfAverageArea:
            df.set_value(i, 'area', 0)
        if vals > dfAverageArea:
            df.set_value(i, 'area', 1)
        i = i+1
    
    i = 0
    for vals in df['perimeter']:
        if vals < dfAveragePerimeter:
            df.set_value(i, 'perimeter', 0)
        if vals > dfAveragePerimeter:
            df.set_value(i, 'perimeter', 1)
        i = i+1
        
    i = 0
    for vals in df['compactness']:
        if vals < dfAverageCompactness:
            df.set_value(i, 'compactness', 0)
        if vals > dfAverageCompactness:
            df.set_value(i, 'compactness', 1)
        i = i+1

    i = 0
    for vals in df['length']:
        if vals < dfAverageLen:
            df.set_value(i, 'length', 0)
        if vals > dfAverageLen:
            df.set_value(i, 'length', 1)
        i = i+1
        
    i = 0
    for vals in df['width']:
        if vals < dfAverageWidth:
            df.set_value(i, 'width', 0)
        if vals > dfAverageWidth:
            df.set_value(i, 'width', 1)
        i = i+1
        
    i = 0
    for vals in df['coeff']:
        if vals < dfAverageCoeff:
            df.set_value(i, 'coeff', 0)
        if vals > dfAverageCoeff:
            df.set_value(i, 'coeff', 1)
        i = i+1
        
    i = 0
    for vals in df['grooveLength']:
        if vals < dfAverageGrooveLength:
            df.set_value(i, 'grooveLength', 0)
        if vals > dfAverageGrooveLength:
            df.set_value(i, 'grooveLength', 1)
        i = i+1
        
    
    return df            

def findErrorForClass(df, attr, clss):
    class1DataFrame = df[ Series(df['classification'] == 1) & Series(df[attr] == clss) ]
    class2DataFrame = df[ Series(df['classification'] == 2) & Series(df[attr] == clss) ]
    class3DataFrame = df[ Series(df['classification'] == 3) & Series(df[attr] == clss) ]
    
    class1DfLen = len(class1DataFrame[class1DataFrame[attr] == clss].index)
    class2DfLen = len(class2DataFrame[class2DataFrame[attr] == clss].index)
    class3DfLen = len(class3DataFrame[class3DataFrame[attr] == clss].index)
    
    if class1DfLen <= class2DfLen:
        if class1DfLen <= class3DfLen:
            return {"ErrorCount" : class1DfLen, "Rule:" : clss}
    
    if class2DfLen <= class1DfLen:
        if class2DfLen <= class3DfLen:
            return {"ErrorCount" : class2DfLen, "Rule:" : clss}
        
    if class3DfLen <= class1DfLen:
        if class3DfLen <= class2DfLen:
            return {"ErrorCount" : class3DfLen, "Rule" : clss}

def probabilityOfValue(attr, val, classification, df):
    df = df[df['classification'] == classification]
    denom = float(len(df.index))
    numer = float(len(df[df[attr] == val].index))
    return (numer / denom)

def main():
    
    dftraining = pd.read_csv('seeds.train.csv', header = 0)
    dftesting = pd.read_csv('seeds.test.csv', header = 0)
    i = 0
    j = 0
    d = 0
    clss = 0
    for val in dftraining['classification']:
        if val == 1:
            i=i+1
        if val == 2:
            j = j+1
        if val == 3:
            d = d+1
    sumTotal = i + j + d
    print i
    print j
    print d
    print sumTotal
    print i,'/',sumTotal
    print j,'/',sumTotal
    print d,'/',sumTotal
    print '==============================='
    
    dftraining = makeNominalValues(dftraining)
    dftraining = dftraining.rename(columns={'Unnamed: 0':'bullshit'}) # rename the column
    dftraining = dftraining.drop('bullshit', 1)
    dftesting = makeNominalValues(dftesting)
    dftesting = dftesting.rename(columns={'Unnamed: 0':'bullshit'}) # rename the column
    dftesting = dftesting.drop('bullshit', 1)
    ''' print dftraining[dftraining['classification'] == 3]
    bestErrorCount = np.inf
    for attr in dftraining.columns[1:-1]:
        print attr
        error = 0
        ruleTato = []
        for clss in np.unique(dftraining[attr]):
            errorForClass = findErrorForClass(df, attr, clss)
            error += errorForClass["ErrorCount"]
            ruleTato.append(errorForClass)
        if error < bestErrorCount:
            bestErrorCount = error
            bestAttr = attr
            bestRuleTato = ruleTato
    
    print "Make rule on %s" % bestAttr
    print "Rules: %s" % bestRuleTato'''
    
    '''specifying an instance to test'''
    instance = [0, 0, 1, 0, 0, 0, 0]
    count = 0
    for index, row in dftesting.iterrows():
        instance = row.values
        pClass1 = 1
        pClass2 = 1
        pClass3 = 1
        '''computing likelihood of each value being able to compute the classification'''
        for index in range(7):
            print '%s %s' % (dftraining.columns[index], instance[index])
            pClass1 *= probabilityOfValue(dftraining.columns[index], instance[index], 1, dftraining)
            pClass2 *= probabilityOfValue(dftraining.columns[index], instance[index], 2, dftraining)
            pClass3 *= probabilityOfValue(dftraining.columns[index], instance[index], 3, dftraining)
            print pClass1
            print pClass2
            print pClass3
            print '==============================='
        
        totalLen = float(len(dftraining.index))
        '''calculating probability of each value being able to compute the classification out of the entirety of the dataframe'''
        pTotalClass1 = len(dftraining[dftraining['classification'] == 1].index) / totalLen
        pTotalClass2 = len(dftraining[dftraining['classification'] == 2].index) / totalLen
        pTotalClass3 = len(dftraining[dftraining['classification'] == 3].index) / totalLen
        print pTotalClass3
        print '---------------------------------------'
        
        print '%f %f %f' % (pTotalClass1, pTotalClass2, pTotalClass3)
        print'----------------------------------------'
        pClass1 *= pTotalClass1
        pClass2 *= pTotalClass2
        pClass3 *= pTotalClass3
        
        tClass1 = pClass1
        tClass2 = pClass2
        tClass3 = pClass3
        '''calculating probability of the instance being classified as class1, class2, or class3 in relation to the classes it isn't classified by'''
        pClass1 /= (tClass1 + tClass2 + tClass3)
        pClass2 /= (tClass1 + tClass2 + tClass3)
        pClass3 /= (tClass1 + tClass2 + tClass3)
        '''printing percentage chance that the instance declared above falls into that classification'''
        print '1: %f, 2: %f, 3: %f' % (pClass1*100 , pClass2*100, pClass3*100)
        
        if pClass1 >= pClass2 and pClass1 >= pClass3:
            if row.classification == 1:
                count+=1
                
            
        elif pClass2 >= pClass1 and pClass2 >= pClass3:
            if row.classification == 2:
                count+=1
            
            
        else:
            if row.classification == 3:
                count+=1
    
    print 'accuracy of the model on test data:', (count / float(len(dftesting)))*100,'%'

    
if __name__ == '__main__':
    main()