import operator
import model
import copy

class OrbModel(model.Model):

    # defines HOR_RINGS_* and VERT_RINGS_*
    # defines height
    def __init__(self, model_file):
        model.Model.__init__(self, model_file)

        self.row = [44, 44, 40, 36, 32, 28, 20, 12]
        self.height = len(self.row)

        HALF_POINT = sum(self.row) - 1

	self.HOR_RINGS_TOP_DOWN = []
	# top
	count = 0
	for h in range(len(self.row)-1, -1, -1):
	    r = []
	    for element in range(HALF_POINT-count,HALF_POINT-count-self.row[h],-1):
		r.append(element)
	    self.HOR_RINGS_TOP_DOWN.append(r)
	    count += self.row[h]
	# bottom
	for h in range(0, len(self.row)-1):
	    r = []
	    for element in range(count,count+self.row[h]):
		r.append(element)
	    self.HOR_RINGS_TOP_DOWN.append(r)
	    count += self.row[h]

	self.HOR_RINGS_MIDDLE_OUT = []
	count = 0
	for h in range(0, len(self.row)):
	    r = []
	    for element in range(count,count+self.row[h]):
		r.append(element)
	    # bottom
	    if h < 7:
		for element in range(HALF_POINT+count+1,HALF_POINT+count+1+self.row[h]):
		    r.append(element)
	    self.HOR_RINGS_MIDDLE_OUT.append(r)
	    count += self.row[h]

        offsets = []
	offsets.append([1,1,1,1,1,1,0,0]) # 1
	offsets.append([1,1,1,1,0,0,1,1]) # 2
	offsets.append([1,1,1,0,1,1,0,0]) # 3
	offsets.append([1,1,1,1,1,1,1,0]) # 4
	offsets.append([1,1,1,1,1,0,0,0]) # 5
	offsets.append([1,1,0,1,0,1,1,1]) # 6
	offsets.append([1,1,1,1,1,0,0,0]) # 7
	offsets.append([1,1,1,1,1,1,1,0]) # 8
	offsets.append([1,1,1,0,1,1,0,0]) # 9
	offsets.append([1,1,1,1,0,0,1,1]) # 10
	offsets.append([1,1,1,1,1,1,0,0]) # 1
	#offsets.append([0,0,0,0,0,0,0,0]) # 0

        self.VERT_RINGS = []
        # row = [0, 44, 44, 40, 36, 32, 28, 20] 
        temp = []
        temp.append(0)
        for i,el in enumerate(self.row[:-1]):        # row is correct!
            temp.append(temp[i]+self.row[i])
        t = copy.copy(temp)
        temp.reverse()
        for y in t:   # bottom
            addition = min(y+HALF_POINT, self.numLEDs-1)
            temp.append(addition)
        self.VERT_RINGS.append(temp)   # first vert_line
        #print self.VERT_RINGS

	for round in range(0,4):        # 0 to 4
	    for x,el in enumerate(offsets):
		# sorry, please forgive me!
		el2 = copy.copy(el)
		el3 = copy.copy(el)
		el3.reverse()        # need to invert top part
		el3.extend(el2)    # add index to itself for top and bottom

		new_vert = list(map(operator.add, el3, self.VERT_RINGS[x+round*len(offsets)]))

		self.VERT_RINGS.append(new_vert)
