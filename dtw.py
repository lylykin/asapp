import math
import numpy as np
import fast_math

from path_extended import PointExtended
class Dtw : 
    """
    applies the Dynamic Time Warping algorithm
    refserie : reference serie we want to compare to
    compserie : serie we want to compare the reference serie with
    cm : costmatrix
    """
    
    def __init__(self, refserie : list, compserie : list):
        
        self.serie_X = compserie  
        self.serie_Y = refserie

        #if self.euclidian_dist(self.serie_X[0], self.serie_Y[0]) != 0 :
        #    self.points_align()


    def __str__(self):
        return f'{self.acm}'
    
    def euclidian_dist(self, val_1 : PointExtended , val_2 : PointExtended) : 
        """
        Computes the euclidian distance between 2 points of a 2-d serie
        """
        
        # knowing that:
        # delta theta is between 0 and 2pi, 
        # delta x is between 0 and 109 but, it will be generally between 0 and 50 
        # so to have an impact, I think delta theta should be multiplied by 15 or 20
        return (math.sqrt((val_1.x-val_2.x)**2 + 
                          (val_1.y-val_2.y)**2 + 
                          (8*fast_math.smallest_delta_angle(val_1.theta,val_2.theta))**2) +
                        (5 * (val_1.curvature - val_2.curvature))**2 )
    
    
    def compute_cost_matrix(self) : 
        """
        Compute a matrix of distance : we'll have the distances of every point of the two series
        """
                
        #creating the cost matrix
        
        mat = [[0 for j in range(len(self.serie_X))] for i in range((len(self.serie_Y)))]

        for i in range(len(self.serie_Y)):
            for j in range(len(self.serie_X)):
                if(self.window is not None and self.window[i][j] == 0):
                    mat[i][j] = math.inf
                else:
                    mat[i][j] = self.euclidian_dist(self.serie_Y[i], self.serie_X[j])
        
        self.cm = mat

    def fast_compute_acc_cost_matrix(self, ceiling): 
        """
        Compute the accumulation cost matrix.
        """ 
        n = len(self.cm)
        m = len(self.cm[0])

        #building the acm matrix. We only need its last element : the min cost
        c_mat = np.zeros((n, m))
        c_mat[-1][-1] = self.fast_coef_acc_cost_matrix(n-1, m-1, ceiling)

        self.acm = c_mat
    
    def fast_coef_acc_cost_matrix(self, i, j, ceiling):
        """"
        returns the coefs of the accumulation cost matrix
        """
        
        #cas initial : le premier point ets à une distance de 0
        if i == 0 and j == 0 :
            return self.cm[i][j]
        
        #cas initial : le score est à l'infini sur les bords
        elif i == 0 or j == 0:
            return math.inf
        
        #cas initial : le point recherché n'est pas dans la fenêtre de recherche
        elif self.window[i][j] == 0 : 
            return math.inf
    
        else : 
            #si on dépasse un certain score, on considère que le dtw ne passera pas par ce point
            if self.cm[i][j] > ceiling:
               return math.inf
            
            new_ceiling = ceiling - self.cm[i][j]
            return self.cm[i][j] + min(self.fast_coef_acc_cost_matrix(i-1, j, new_ceiling ), self.fast_coef_acc_cost_matrix(i, j-1, new_ceiling), self.fast_coef_acc_cost_matrix(i-1, j-1, new_ceiling))            

    def dtw(self, ceiling):
        """
        Retourne le score dtw enntre 2 séries
        """
        # try except pour gérer le cas ou on applique le dtw ou le cas ou on applique le fastdtw.
        #finalement un peu inutile car on a pas eu besoin d'implémenter le fast
        try :
            return self.acm[-1][-1]
        except :            
            self.window = self.create_window(len(self.serie_Y), len(self.serie_X))
            self.compute_cost_matrix()
            self.fast_compute_acc_cost_matrix(ceiling)         
            return self.acm[-1][-1]
                

    def create_window(self, col : int, row : int, radius = 5):
        """
        retourne une fenêtre de recherche, soit une diagonale de 1.
        Si le coefficient est 1 : la valeur associée dans la matrice de cout est dans la fenêtre
        Si le coefficient est 0 : on est hors de la fenêtre de recherche et le score ne sera pas calculé
        radius : largeur de la diagonale
        row : le nombre d'éléments dans une ligne
        col : le nombre de lignes (quand on regarde les colonnes)
        """
        
        window = [[0 for j in range(row)] for i in range(col)]
        
        if col <= 1 or row <= 1 :
            return [[1 for j in range(row)] for i in range(col)]  
          
        #creation de la diagonale
        for i in range(col) : 
            
            for j in range(row):
    
                #on est dans la fenetre de recherche quand la case i,j est assez près de la diagonale 
                #(avec un facteur pour résoudre le pb de ratio/sizing de la fen)
                if abs(i*(row/col)-j) <= radius :
                    window[i][j] = 1
    
        return window

    def points_align(self) :
        """
        creates if needed an offset, so that the first two points of the series are aligned
        Edits the serie_Y attribute when called
        """
        
        #récupération des premiers points pour la lisibilité
        X_first = self.serie_X[0]
        Y_first = self.serie_Y[0]
        
        #calcul de la distance entre 2 points
        off_x = X_first[0]-Y_first[0]
        off_y = Y_first[1]-Y_first[1]
        
        #application de l'offset pour aligner les 2 séries
        res = []
        for elt in range(len(self.serie_X)) :                 
            res.append((self.serie_X[elt][0]-off_x, self.serie_X[elt][1]-off_y))
        self.serie_X = res
                
"""      
d = Dtw([(1,0),(3,2),(4,4)],[(0,1),(2,4),(4,4)])
d.CostMatrix()
d.AccCostMatrix()
print(d)""" 