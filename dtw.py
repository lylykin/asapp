import math

class Dtw : 
    """
    applies the Dynamic Time Warping algorithm
    refserie : eference serie we want to compare to
    compserie : serie we want to compare the refercence serie with
    cm : costmatrix
    """
    
    def __init__(self, refserie : list, compserie : list):# i think it'll be better if  the series were arrays but for now i set it as a list
        
        self.refserie = refserie   
        self.compserie = compserie

    def __str__(self):
        return f'{self.acm}'
    
    def CostMatrix(self) : 
        """
        return a matrix of distance : we'll have the distances of every points of the two series
        """
        
        #computes the euclidian distance
        euclidian_dist = lambda x,y : (abs(x-y))
        
        #creating the cost matrix
        mat = [[euclidian_dist (x=self.compserie[i], y=self.refserie[j])
                for i in range(len(self.compserie))]
                for j in range(len(self.refserie))]

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
        
        #the distance here iis tshe same as the euclidian distance
        if i ==0 and j == 0:
            return self.cm[i][j]
        
        elif i == 0 or j == 0:
            return math.inf
        
        #the disnace here is the euclidian distance with the smallest distance from its neighbours in the C matrix
        else :
            return self.cm[i][j] + min(self.CoefAccCostMatrix(i-1, j), self.CoefAccCostMatrix(i, j-1), self.CoefAccCostMatrix(i-1, j-1))

    def dtw(self): 
        return self.acm[-1][-1]
        
d = Dtw([1,3,4],[1,2,4])
d.CostMatrix()
d.AccCostMatrix()
print(d)