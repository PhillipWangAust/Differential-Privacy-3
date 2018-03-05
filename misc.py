#given two outputs of a Mechanism, compute the sensitivity 
        @staticmethod 
        def sensitivity(d1, d2):
                #print("d1:{}, d2:{}".format(d1,d2))
		total_sens = 0.
                if type(d1) is dict:
			for k,v in d1.items():
                                if k in d2:   
					total_sens += abs(d2[k]-v)
				else: total_sens += v 

                else: 
			total_sens = abs(d2-d1) 

                return total_sens
   

        @staticmethod
	def compute_sensitivity(func, d1, **kwargs):

		max_sens = 0.
                #print ("d1:{}".format(d1))
                inputs = kwargs['input']
                
                #remove one item at a time from input to see its effect on the output 
        	for i in range(len(inputs)):
                        #remove an item from input attr: values 
			inputs_cpy = inputs[:]
			inputs_cpy.pop(i)
                        #now make a copy of all input  
                        kwargs_cpy = kwargs.copy()
			kwargs_cpy['input'] = inputs_cpy

                        #compute the function now on new input   
			d2 = func(**kwargs_cpy)
                        
                        curr_sens = Diff_Privacy.sensitivity(d1,d2)
                        
			if curr_sens > max_sens: max_sens = curr_sens
		return max_sens	