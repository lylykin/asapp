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

        
    def CostMatrix(self) : 
        """
        return a matrix of distance : we'll have the distances of every points of the two series
        """
        
        #computes the euclidian distance
        euclidian_dist = lambda x,y : (abs(x-y))**2  
        
        #creating the cost matrix
        mat = [[euclidian_dist (x=self.compserie[i], y=self.refserie[j])
                for i in range(len(self.compserie))]
                for j in range(len(self.refserie))]

        self.cm = mat
        

    def AccCostMatrix(self, i = len(self.cm), j = len(self.cm[0]) ) :#cm est une matrice d'entiers *
        """
        returns the accumulation cost matrix.
        """
        
        if i ==0 or j==0 : 
            return math.inf
        
        if i ==1 and j == 1:
            return self.cm[i][j]
        
        else :
            pass
        
        
        
    
