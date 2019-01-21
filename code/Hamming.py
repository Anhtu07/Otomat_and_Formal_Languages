def noOfParityBits(noOfBits):
	i=0
	while 2.**i <= noOfBits+i: 
		i+=1
	return i
def noOfParityBitsInCode(noOfBits):
	i=0
	while 2.**i <= noOfBits:
		i+=1

	return i

def appendParityBits(data):
	n=noOfParityBits(len(data)) #no of parity bits required for given length of data
	i=0 #loop counter
	j=0 #no of parity bits
	k=0 #no of data bits
	list1=list()
	while i <n+len(data):
		if i== (2.**j -1):
			list1.insert(i,0)
			j+=1
		else:
			list1.insert(i,data[k])
			k+=1
		i+=1
	return list1

def hammingCodes(data):
	n=noOfParityBits(len(data))
	list1=appendParityBits(data) # list with parity bits at appropriate position
	i=0 #loop counter
	k=1 #2 to the power kth parity bit
	while i<n:
		k=2.**i
		j=1
		total=0
		while j*k -1 <len(list1):
			if j*k -1 == len(list1)-1: #if lower index is last one to be considered in sub list then
				lower_index=j*k -1
				temp=list1[int(lower_index):len(list1)]
			elif (j+1)*k -1>=len(list1):
				lower_index=j*k -1
				temp=list1[int(lower_index):len(list1)] #if list's size is smaller than boundary point
			elif (j+1)*k -1<len(list1)-1:
				lower_index=(j*k)-1
				upper_index=(j+1)*k -1
				temp=list1[int(lower_index):int(upper_index)]
			
			total=total+sum(int(e) for e in temp) #do the sum of sub list for corresponding parity bits
			j+=2 #increment by 2 beacause we want alternative pairs of numberss from list
		if total%2 >0:
			list1[int(k)-1]=1 # to check even parity summing up all the elements in sublist and if summ is even than even parity else odd parity
		i+=1
	return list1
def hammingCorrection(data):
	n=noOfParityBitsInCode(len(data))
	i=0
	list1=list(data)
	errorthBit=0
	while i<n:
		k=2.**i
		j=1
		total=0
		while j*k -1 <len(list1):
			if j*k -1 == len(list1)-1:
				lower_index=j*k -1
				temp=list1[int(lower_index):len(list1)]
			elif (j+1)*k -1>=len(list1):
				lower_index=j*k -1
				temp=list1[int(lower_index):len(list1)] #if list's size is smaller than boundary point
			elif (j+1)*k -1<len(list1)-1:
				lower_index=(j*k)-1
				upper_index=(j+1)*k -1
				temp=list1[int(lower_index):int(upper_index)]
			
			total=total+sum(int(e) for e in temp)
			j+=2 #increment by 2 beacause we want alternative pairs of numberss from list
		if total%2 >0:
			errorthBit+=k # to check even parity summing up all the elements in sublist and if summ is even than even parity else odd parity
		i+=1
	if errorthBit>=1:
		#toggle the corrupted bit
		if list1[int(errorthBit-1)]=='0' or list1[int(errorthBit-1)]==0:
			list1[int(errorthBit-1)]=1
		else:
			list1[int(errorthBit-1)]=0
	list2=list()
	i=0
	j=0
	k=0
	while i<len(list1): 
		if i!= ((2**k)-1):
			temp=list1[int(i)]
			list2.append(temp)
			j+=1
		else:
			k+=1
		i+=1
	return errorthBit, list2