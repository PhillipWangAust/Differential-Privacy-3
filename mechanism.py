import random 
import numpy as np


class Mechanism(object):
    """
    An abstract implementation for differentially private 
    mechanisms e.g. Laplace, Exponential etc.    
    """    
    def sample(self, epsilon):
    	pass


class Laplace(Mechanism):
    """
    Implements a exponential mechanism of differential 
    privacy. Only count queries with sensitivity = 1 are 
    supported        
    """
    @staticmethod
    def sample(self, epsilon):  
        return int(abs(np.random.laplace(0, scale=1./epsilon)))

 
class Exponential(Mechanism):
   """
   Implements a exponential mechanism of differential 
   privacy. Only queries with sensitivity = 1 (Counts) 
   and, select one from list based on scores are supported        
   """

   @staticmethod        
   def sample(epsilon):
        """
        Samples numerical noise from exponential distribution
        """
        #sample from uniform distribution
   	u = random.uniform(0., 1.0)

        #convert to exponential distribution sample
        lamda = epsilon/2. 
        return int(-(np.log(-u+1.))/lamda)
        
       
   @staticmethod
   def categorical_sample(data, epsilon):
       """
       Samples a categorical item from exponential distribution
       Assumption: item are ranked by their position in Lst. 
       e.g. Lst[0] is highest rank and len(Lst)-1 lowest.
       """
  
       #compute scores using scoring function.
       
      
       if not type(data) == list:
       		raise TypeError("Return Type of scoring function must be a list")
   
       #draw a sample with indx-score and return the associated attribute.
       indx = Exponential.sample(epsilon)
               
       if indx > len(data)-1:
           indx = len(data)-1
 
       return data[indx] 



