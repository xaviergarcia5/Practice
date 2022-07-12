
#EQ = collections.namedtuple("EQ",["mag","depth","lon","lat","date","eventID"])

def compute_mean_depth(EQList):
	'''
	param (filename) Dictionary, filename
	return value is a list
	'''
	depth_list = [x.depth for x in EQList] # x is one object in EQList
	#average of depth_list
	depth_list_mean = np. mean(depth_list)
	print(depth_list_mean)










	return mean_depth:





