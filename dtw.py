import math
import numpy as np
class Dtw : 
    """
    applies the Dynamic Time Warping algorithm
    refserie : reference serie we want to compare to
    compserie : serie we want to compare the reference serie with
    cm : costmatrix
    """
    
    def __init__(self, refserie : list, compserie : list):# i think it'll be better if  the series were arrays but for now i set it as a list
        
        self.refserie = np.array(refserie)   
        self.compserie = np.array(compserie)

    def __str__(self):
        return f'{self.acm}'
    
    def EuclidianDist(self, val_1 : tuple, val_2 : tuple) : 
        """
        Computes the euclidian distance between 2 points of a 2-d serie
        """
        
        return abs(val_1[0]-val_2[0]) + abs(val_1[1]-val_2[1])
    
    def ComputeCostMatrix(self) : 
        """
        Compute a matrix of distance : we'll have the distances of every point of the two series
        """
        
        #computes the euclidian distance

        
        #creating the cost matrix
        mat = np.zeros((len(self.refserie), len(self.compserie)))
        for i in range(len(self.refserie)):
            for j in range(len(self.compserie)):
                mat[i][j] = self.EuclidianDist(self.refserie[i], self.compserie[j])
        
        self.cm = mat
    
    def ComputeAccCostMatrix(self): 
        """
        Compute the accumulation cost matrix.
        """ 
        n = len(self.cm)
        m = len(self.cm[0])
        
        #building the acm matrix

        c_mat = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                c_mat[i][j] = self.CoefAccCostMatrix(i, j)

        self.acm = c_mat


    def CoefAccCostMatrix(self, i, j) : #might have a high cost, we'll see if that's an issue or not
        #we set the distance to the 1st point as infinite
        i = max(i, 0)
        j = max(j, 0)
        #the distance here is the same as the euclidian distance
        if i ==0 and j == 0:
            return self.cm[i][j]
        
        elif i == 0 or j == 0:
            return math.inf
        
        #the distance here is the euclidian distance with the smallest distance from its neighbours in the C matrix
        else :
            return self.cm[i][j] + min(self.CoefAccCostMatrix(i-1, j), self.CoefAccCostMatrix(i, j-1), self.CoefAccCostMatrix(i-1, j-1))

    def dtw(self):
        self.ComputeCostMatrix()
        self.ComputeAccCostMatrix()         
        return self.acm[-1][-1]
"""        
d = Dtw([(1,0),(3,2),(4,4)],[(0,1),(2,4),(4,4)])
d.CostMatrix()
d.AccCostMatrix()
print(d)""" 