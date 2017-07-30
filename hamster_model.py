import operator
import model

class HamsterModel(model.Model):

    # defines HOR_RINGS_* and VERT_RINGS_*
    # defines height
    # defines row 
    def __init__(self, model_file):
        model.Model.__init__(self, model_file)

        # sort by z-coord
        temp_model = sorted(self.model, key=operator.itemgetter(2), reverse=True)

        current_z = temp_model[0][2]
        count = 0
        self.row = []
        for i, entry in enumerate(temp_model):
            if entry == [0.0,0.0,0.0]: continue
            z = entry[2]
            if z != current_z:
                self.row.append(count)
                current_z = z
                count = 0
            count = count + 1
        self.row.append(count)
        print "rows: ", self.row

        self.height = len(self.row)
        self.bottom_missing = 3     # how many rows are missing on the bottom of the globe
        
        # HORIZONTAL RINGS TOP DOWN
        self.HOR_RINGS_TOP_DOWN = []

        current_z = temp_model[0][2]
        row = []
        for e in temp_model:
            if e == [0.0,0.0,0.0]: continue
            z = e[2]
            if z != current_z:
                current_z = z
                self.HOR_RINGS_TOP_DOWN.append(row)
                row = []
            row.append(self.position[str(e)])
        self.HOR_RINGS_TOP_DOWN.append(row)
        #print self.HOR_RINGS_TOP_DOWN
        
        # HORIZONTAL RINGS MIDDLE OUT
        self.HOR_RINGS_MIDDLE_OUT = []
        self.HOR_RINGS_MIDDLE_OUT.append(self.HOR_RINGS_TOP_DOWN[8])
        for offset in [1, 2, 3, 4, 5]:
            concat = sum([self.HOR_RINGS_TOP_DOWN[8+offset], self.HOR_RINGS_TOP_DOWN[8-offset]], [])
            self.HOR_RINGS_MIDDLE_OUT.append(concat)
        for ring in range(3,-1,-1):
            self.HOR_RINGS_MIDDLE_OUT.append(self.HOR_RINGS_TOP_DOWN[ring])

        lengths_top = [ 9, 6, 7, 6, 8, 6, 7, 6 ] 
        fillers = [0, 0, 0, 0, 3, 0, 0, 30]
        self.RINGS_AROUND = []
        count = 0
        direction = 0
        for rings in range(32):
            if rings not in [5, 8, 13, 16, 21, 24, 29, 32]: 
                #print "change"
                direction ^= 1

            meridian = []
            for i in range(lengths_top[rings%8]+5):
                meridian.append(count) 
                count += 1
            if not direction: meridian.reverse()      # making it bottom to top
            self.RINGS_AROUND.append(meridian)
            count += fillers[rings%8]
        #print self.RINGS_AROUND

        self.VERT_RINGS = []
        self.VERT_RINGS.append(self.RINGS_AROUND[8])
        for ring in range(7,-1,-1):
            concat = sum([self.RINGS_AROUND[ring], self.RINGS_AROUND[16-ring]], [])
            self.VERT_RINGS.append(concat)
        for ring in range(8):
            concat = sum([self.RINGS_AROUND[31-ring], self.RINGS_AROUND[17+ring]], [])
            self.VERT_RINGS.append(concat)
        self.VERT_RINGS.append(self.RINGS_AROUND[24])
        
