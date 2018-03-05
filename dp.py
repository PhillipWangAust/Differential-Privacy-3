from __future__ import print_function

from mechanism import Exponential as exponential  
from mechanism import Laplace as laplace  

class DP(object):
        """
        Implementation of differential privacy.Only static methods must be called
        ToDo: Checkpointing, log management in case of server failure.      
        """

        _budget = None
        
        def __init__(self, ):
	    if type(self) == DP:
                raise Exception("<DP> must not be instantiated. May lead to unexpected behaviour")


        
        @staticmethod 
        def register_budget(budget):
            """
               registers privacy budget per function call for a ga4gh server at <url> 
            """
            DP._budget = budget
	
        
        @staticmethod 
        def is_budget_registered():
             return DP._budget is not None
  

        @staticmethod
        def update_budget(epsilon):
            if DP._budget is None: 
                raise RuntimeError("Error! Server has no registered privacy settings. Call DP.register_budget first")
            
            epsilon = min(DP._budget, epsilon)  #what if budget is not sufficient
            DP._budget -= epsilon
            return epsilon


        @staticmethod
	def noise(data, epsilon, categorical= False, mechanism = "exponential", delta = 1.):
            """
            Adds noise using exponential mechanism (sensitivity = 1)
            Only count queries or queries of type choose one from a list
            categorical nature are supported 
            """  
            if DP._budget is None: 
                raise RuntimeError("Error! Server has no registered privacy settings. Call DP.register_budget first")
                

            if categorical:                                            #requires list be sorted by scores of elements
                return exponential.categorical_sample(epsilon)    
                

            if type(data) is int or type(data) is float:
                if mechanism == "laplace": 
                     data += laplace.sample(epsilon)
                else: 
                     data += exponential.sample(epsilon)
                      
                
            if type(data) is dict:
                for ky in data:
                     data[ky] = noise(data[ky], epsilon, categorical=categorical, mechanism=mechanism, delta=delta)
                 
            if type(data) is list: 
            	for indx, value in enumerate(data): 
                     data[indx] = noise(data[indx], epsilon, categorical=categorical, mechanism=mechanism, delta=delta) 
                                        
            return data



       
		               
def privatize(eps, is_categorical= False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            epsilon = DP.update_budget(eps)
            if epsilon == 0.: epsilon = 1e-200
            return DP.noise(function(*args, **kwargs), epsilon, categorical=is_categorical)
        return wrapper

    return decorator
                




@privatize(0.1)
def average(lst):
	return sum(lst)/float(len(lst))



if __name__ == "__main__":
     #privacy settings. 
     #Diff_Privacy.epsilon = 0.55

     #input attribute values that need to be protected
     lst = [1,2,3,4,5]    
     DP.register_budget(1.3)
     #find the average in diff: private way  		
     myres = average(lst)
     print("Diff: Private Result:{}".format(myres))
     


