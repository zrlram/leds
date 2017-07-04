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

        current_z = self.temp_model[0][2]
        count = 0
        self.row = []
        for i, entry in enumerate(self.temp_model):
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

        self.RINGS_AROUND = []
        for rings in range(32):
            meridian = [rings * self.height + x for x in range(self.height)]
            self.RINGS_AROUND.append(meridian)

        self.VERT_RINGS = []
        self.VERT_RINGS.append(RINGS_AROUND[8])
        for ring in range(7,-1,-1):
            concat = sum([RINGS_AROUND[ring], RINGS_AROUND[16-ring]], [])
            self.VERT_RINGS.append(concat)
        for ring in range(8):
            concat = sum([RINGS_AROUND[31-ring], RINGS_AROUND[17+ring]], [])
            self.VERT_RINGS.append(concat)
        self.VERT_RINGS.append(RINGS_AROUND[24])
        
