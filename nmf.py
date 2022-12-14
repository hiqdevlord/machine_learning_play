from numpy import *

def difcost(a,b):

	dif=0

	for i in range(shape(a)[0]):
		for j in range(shape(a)[1]):
			dif+=pow(a[i,j]-b[i,j],2)
	return dif

def factorize(v, pc=10, iter=50):
	ic=shape(v)[0]
	fc=shape(v)[1]

	# initialize weight and features matrices with random values
	w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
	h=matrix([[random.random() for i in range(fc)] for i in range(pc)])

	# perform operation a max of iter times
	for i in range(iter):
		wh=w*h

		#calculate current diff
		cost=difcost(v,wh)

		if i%3==0: print cost

		# terminate if fully factorized
		if cost==0: break

		# update feature matrix
		hn=(transpose(w)*v)
		hd=(transpose(w)*w*h)

		h=matrix(array(h)*array(hn)/array(hd))

		# update weights matrix
		wn=(v*transpose(h))
		wd=(w*h*transpose(h))

		w=matrix(array(w)*array(wn)/array(wd))

	return w,h
