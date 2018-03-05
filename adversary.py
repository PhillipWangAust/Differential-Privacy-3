#Compute posterior beliefs. 
def Beta(org_answers,noisy_answers, curr_pop, lamda):

 #simulating the other possible databases in the world by subtracting 1 and then computing prob.

	posteriors = {}  
        if curr_pop not in org_answers:
		  org_answers[curr_pop] =  0. 
                  noisy_answers[curr_pop] =  0.
 
	for pop in org_answers.keys():
		org_answers_m = org_answers.copy()
                org_answers_m[pop] -= 1
                org_answers_m[curr_pop] += 1
                
                posteriors[pop] = mp.mpf(1., dps=50)   
		for key in noisy_answers.keys():
                        posteriors[pop] *= mp.mpf(1./(2.*lamda)*np.exp(-1*(abs(noisy_answers[key]-org_answers_m[key])/lamda)), dps=50)



        norm_pos = {}         
        #normalizing posteriors
        #print("curr_pop:{}\t posteriors:{}".format(curr_pop, posteriors))
	for k,v in posteriors.items():
                #Only return posterior beliefs of wk using which we produced the noisy answers. 
                if k  == curr_pop:
			norm_pos[k] = v/sum(posteriors.values())
              
        _max_pos_key = max(norm_pos, key=lambda key: norm_pos[key])

        
        return _max_pos_key, norm_pos[_max_pos_key]


def Adversary_model(func, inputs,  sensitivity = 1 ):

	#modeling prior beliefs: assume all neighbours have equal prior prob: 
        alpha  =  1./len(inputs)
        print ("possible worlds:{}\nprior belief:{}".format(len(inputs), alpha))
          
        beta = 0.
        
        labels = set(inputs)
        
        computed = []
        
        if len(labels) > 1.:
                global_max_beta = global_max_Conf =  0.0

                #print("labels:{}".format(labels))
 
		for label in labels:
			first_occur  = inputs.index(label)
                        wk =  inputs[:]   
			wk.pop(first_occur)
                        kwargs = {}
                        kwargs['input'] =  wk
                        output =  func(**kwargs)

			org_answers = output['original_answer']
                	noisy_answers = output['noisy_answer']  
          
                         
                	lamda = sensitivity/Diff_Privacy.epsilon 
                  
                	if type(noisy_answers) is dict:
                                #print("original answers:{}, noisy answers:{}".format(org_answers,noisy_answers ))
				attr_ky, _max_beta  = Beta(org_answers, noisy_answers, label, lamda) 
                                _max_Conf = abs( _max_beta - alpha)    
                                print("Max_Beta:{}, Conf:{}".format( _max_beta, _max_Conf))
                                if _max_beta > global_max_beta:
			        	global_max_beta = _max_beta
					global_max_Conf = _max_Conf
					
                print ("Max. Beta:{}, Max.Conf:{}".format(global_max_beta, global_max_Conf))