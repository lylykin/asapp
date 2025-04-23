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
        euclidian_dist = lambda x,y : (abs(x-y))**2  
        
        #creating the cost matrix
        mat = [[euclidian_dist (x=self.compserie[i], y=self.refserie[j])
                for i in range(len(self.compserie))]
                for j in range(len(self.refserie))]

        self.cm = mat
    
    def AccCostMatrix(self,): 
        """
        returns the accumulation cost matrix.
        """ 
        i = len(self.cm)
        j = len(self.cm[0])
        
        #matrice initialization to make my life easier
        init_mat = [[_ for _ in range(j)]
                    for k in range(i)]
               
        #i'm still not sure if those matrix should be attributes or not, but we can stock them in one objet if done this way ig
        self.acm = self._AccCostMatrix(i-1, j-1, init_mat)  

    def _AccCostMatrix(self, i, j, c_mat) : #might have a high cost, we'll see if that's an issue or not
        """
        private function to remove an issue with the recursive function below
        """
        #we set the distance to the 1st point as infinite
        if i ==0 or j==0 : 
            return math.inf 
        
        #the distance here iis tshe same as the euclidian distance
        if i ==1 and j == 1:
            return self.cm[i][j]
        
        #the disnace here is the euclidian distance with the smallest distance from its neighbours in the C matrix
        else :
            c_mat[i][j] = self.cm[i][j] + min(self._AccCostMatrix(i-1, j, c_mat), self._AccCostMatrix(i, j-1, c_mat), self._AccCostMatrix(i-1, j-1, c_mat))
        
        
        
d = Dtw([1,3,4],[1,2,4])
d.CostMatrix()
d.AccCostMatrix()
print(d)