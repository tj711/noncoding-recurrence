#!python

import rpy2.robjects as robjects
import pandas.rpy.common as com
#from rpy2.objects import pandas2ri
#pandas2ri.activate()

import pandas as pd
import numpy as np
import cPickle
import random

## load .RData and converts to pd.DataFrame
#robj = robjects.r.load('train_test.rda')
# iterate over datasets the file
'''
for sets in robj:
    myRData = com.load_data(sets)
    # convert to DataFrame
    if not isinstance(myRData, pd.DataFrame):
        myRData = pd.DataFrame(myRData)
        print(myRData.shape)

## save pd.DataFrame to R dataframe
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C':[7,8,9]},
                index=["one", "two", "three"])
r_dataframe = com.convert_to_r_dataframe(df)
'''

#-------------------------------------------------------------
# Split data into training set and testing/validation set or
# just sampling part of the data
#-------------------------------------------------------------
def sample_split_data(mydata,split_rate):
	(nrows,ncols) = mydata.shape
	#mcords = np.core.defchararray.split(mydata[:,-1],'-')
	mcords = [str.split(cord,'-') for cord in mydata[:,-1]]
	chr_cords_list = [cord[0]+str(int(cord[1])/10**6) for cord in mcords]

	#Debugging
	print "debugging:",split_rate,chr_cords_list[0:10]

	uniq_list_val = list(set(chr_cords_list))
	uniq_train_val = random.sample(uniq_list_val,int(split_rate*len(uniq_list_val)))
	uniq_test_val = list(set(uniq_list_val)-set(uniq_train_val))

	train_indices = [i for i,item in enumerate(chr_cords_list) if item in uniq_train_val]
	test_indices = list(set(range(len(chr_cords_list))) - set(train_indices))

	print "debugging:",len(chr_cords_list),len(train_indices),len(test_indices),train_indices[0:10]

	train_data = mydata[train_indices,]
	test_data = mydata[test_indices,]

	return train_data,test_data
#//end sample_split_data


def transform_data(r_datfile, full_dump_name, train_sampl_size,test_sampl_size,sample_only=True):
	#train_sampl_size = 100000
	#test_sampl_size = 20000

	#full_dump_name = 'noncoding.data.py.save'
	#sampl_dump_name = 'noncoding.data.py.'+str(train_sampl_size/10**3)+"k."+str(test_sampl_size/10**3)+"k.save"
	#print sampl_dump_name

	if sample_only:
		full_data = cPickle.load(open('noncoding.data.py.save','rb'))
		train_data = full_data['train_data']
		test_data = full_data['test_data']

		## Sample the data set (~3.6M -> sampl_size)
		#train_data_subset = train_data[random.sample(range(train_data.shape[0]),train_sampl_size),]
		#test_data_subset = test_data[random.sample(range(test_data.shape[0]),test_sampl_size),]
		train_subset,train_left = sample_split_data(train_data, float(train_sampl_size)/train_data.shape[0])
		test_subset,test_left = sample_split_data(test_data,float(test_sampl_size)/test_data.shape[0])

		print('train_subset:{},test_subset:{}'.format(train_subset.shape,test_subset.shape))

		dump_data_subset = {'train_data': train__subset,
												'test_data': test_subset}
		cPickle.dump(dump_data_subset,open(sampl_dump_name,'wb'),protocol=cPickle.HIGHEST_PROTOCOL)
	else:
		## Load the R-store data
		robj = robjects.r.load(r_datfile)
		myRData = com.load_data(robj[0])
		#from rpy2.robjects import r
		#r.data('train_test.rda')
		#myRData = pandas2ri.ripy(r[0])

		train_data = np.array(pd.DataFrame(myRData['train']))
		test_data = np.array(pd.DataFrame(myRData['test']))
		dump_data = {'train_data': train_data,
  		           'test_data': test_data}

		print('train:{}, test:{}'.format(train_data.shape, test_data.shape))
		cPickle.dump(dump_data,open(full_dump_name,'wb'),protocol=cPickle.HIGHEST_PROTOCOL)

		'''
		## Sample the data set (~3.6M -> sampl_size)
		#train_data_subset = train_data[random.sample(range(train_data.shape[0]),train_sampl_size),]
		#test_data_subset = test_data[random.sample(range(test_data.shape[0]),test_sampl_size),]
		train_subset,train_left = sample_split_data(train_data, float(train_sampl_size)/train_data.shape[0])
		test_subset,test_left = sample_split_data(test_data,float(test_sampl_size)/test_data.shape[0])

		print('train_subset:{},test_subset:{}'.format(train_subset.shape,test_subset.shape))

		dump_data_subset = {'train_data': train_subset,
												'test_data': test_subset}
		cPickle.dump(dump_data_subset,open(sampl_dump_name,'wb'),protocol=cPickle.HIGHEST_PROTOCOL)
		'''
	#//end if
#//end function transform_data

def main():
	#train_sampl_size = 100000
	#test_sampl_size = 20000
	##call transformation of data
	transform_data('../data/train_test.sampled.mixed.331.0.3.rda',
								 '../data/noncoding.data.sampled.mixed.331.0.3.save',
								 100000,
								 20000,
								 False)
#//end main

if __name__ == "__main__":
	main()
