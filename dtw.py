import math

class Dtw : 
    """
    applies the Dynamic Time Warping algorithm
    refserie : reference serie we want to compare to
    compserie : serie we want to compare the reference serie with
    cm : costmatrix
    """
    
    def __init__(self, refserie : list, compserie : list):# i think it'll be better if  the series were arrays but for now i set it as a list
        
        self.refserie = refserie   
        self.compserie = compserie

    def __str__(self):
        return f'{self.acm}'
    
    def EuclidianDist(self, val_1 : tuple, val_2 : tuple) : 
        """
        Computes the euclidian distance between 2 points of a 2-d serie
        """
        
        euclidian_dist = lambda x,y : (abs(x-y))
        return euclidian_dist(x=val_1[0]-val_2[0], y = val_1[1]-val_2[1])
        
    
    def CostMatrix(self) : 
        """
        return a matrix of distance : we'll have the distances of every point of the two series
        """
        
        #computes the euclidian distance

        
        #creating the cost matrix
        mat = [[self.EuclidianDist(v1, v2)
                for v1 in self.compserie]
                for v2 in self.refserie]

        self.cm = mat
    
    def AccCostMatrix(self): 
        """
        returns the accumulation cost matrix.
        """ 
        n = len(self.cm)
        m = len(self.cm[0])
        
        #building the acm matrix
        c_mat = [[self.CoefAccCostMatrix(i, j) for j in range(m)]
                for i in range(n)]
                
                
        self.acm = c_mat


    def CoefAccCostMatrix(self, i, j) : #might have a high cost, we'll see if that's an issue or not
        #we set the distance to the 1st point as infinite
        
        #the distance here is the same as the euclidian distance
        if i ==0 and j == 0:
            return self.cm[i][j]
        
        elif i == 0 or j == 0:
            return math.inf
        
        #the distance here is the euclidian distance with the smallest distance from its neighbours in the C matrix
        else :
            return self.cm[i][j] + min(self.CoefAccCostMatrix(i-1, j), self.CoefAccCostMatrix(i, j-1), self.CoefAccCostMatrix(i-1, j-1))

    def dtw(self):
        self.CostMatrix()
        self.AccCostMatrix()         
        return self.acm[-1][-1]
"""        
d = Dtw([(1,0),(3,2),(4,4)],[(0,1),(2,4),(4,4)])
d.CostMatrix()
d.AccCostMatrix()
print(d)""" 