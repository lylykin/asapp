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
        
        self.serie_X = np.array(compserie)   
        self.serie_Y = np.array(refserie)

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
        
        mat = [[0 for j in range(len(self.serie_X))] for i in range((len(self.serie_Y)))]

        for i in range(len(self.serie_Y)):
            for j in range(len(self.serie_X)):
                mat[i][j] = self.EuclidianDist(self.serie_Y[i], self.serie_X[j])
        
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

    def FastComputeAccCostMatrix(self): 
        """
        Compute the accumulation cost matrix.
        """ 
        n = len(self.cm)
        m = len(self.cm[0])


        #creation de la fenetre de recherche
        self.window = self.window(len(self.serie_Y), len(self.serie_X))
        _ = len(self.window)
        test= len(self.window[0])
        
        #building the acm matrix

        c_mat = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                if self.window[i][j] == 1:
                    c_mat[i][j] = self.FastCoefAccCostMatrix(i, j)

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

    
    def FastCoefAccCostMatrix(self, i, j):
        """"
        principe algo : si premier elt : on est dans 
        """
        
        if i == 0 and j == 0 :
            return self.cm[i][j]
        
        elif i == 0 or j == 0:
            return math.inf
        
        elif self.window[i][j] == 0 : 
            return math.inf
    
        else : 
            return self.cm[i][j] + min(self.FastCoefAccCostMatrix(i-1, j), self.FastCoefAccCostMatrix(i, j-1), self.FastCoefAccCostMatrix(i-1, j-1))            

    def dtw(self):
        """
        returns the dtw score for two series
        """
        #pour gérer le cas ou on applique le dtw ou le cas ou on applique le fastdtw
        try :
            return self.acm[-1][-1]
        
        except :            
            self.ComputeCostMatrix()
            self.FastComputeAccCostMatrix()         
            return self.acm[-1][-1]
        
    #def update_window(self, window, update_value) : 
    #    """
    #    implémentation factice, sera à revoir. window_value correspond aux valeurs qui sont dans le radius.
    #    la fenetre a pour valeur 1 si on parcoure, 0 sinon
    #    """
    #    
    #    #cas ou la fen est upgraded de base. on a pas rétrécissement
    #    for r in range(update_value) : 
    #        for c in range(update_value[r]): 
    #            window[r][c] = 1
                

    def window(self, col, row, radius = 4):
        """
        returns a search window depending of a radius
        row : le nombre d'éléments dans une ligne
        col : le nombre de lignes (quand on regarde les colonnes)
        """
        
        window = [[0 for j in range(row)] for i in range(col)]
        
        #creation de la diagonale
        for i in range(col) : 
            
            for j in range(row):
                #on est dans la fenetre de recherche quand la case i,j est assez près de la diagonale
                if abs(i-j) <= radius :
                    window[i][j] = 1
                    
        return window

def reduce_by_half(serie : list) :  
    """
    returns half of the points of a serie
    """  
    return [serie[pt] for pt in range(0, len(serie), 2)]
    


"""      
d = Dtw([(1,0),(3,2),(4,4)],[(0,1),(2,4),(4,4)])
d.CostMatrix()
d.AccCostMatrix()
print(d)""" 