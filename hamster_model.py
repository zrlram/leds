import opc
import json
import copy
import operator
from color import set_brightness_multiplier
import multiprocessing 
from ctypes import c_ubyte
from math import ceil, sin, cos

import model

class HamsterModel(model.Model):

    def __init__(self, model_file):
        model.Model.__init__(self, model_file)

        self.height = len(self.row)

        self.temp_model = sorted(self.model, key=operator.itemgetter(2), reverse=True)
        
        # HORIZONTAL RINGS TOP DOWN
        self.HOR_RINGS_TOP_DOWN = []

        current_z = self.temp_model[0][2]
        row = []
        for e in self.temp_model:
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

        RINGS_AROUND = []
        for rings in range(32):
            meridian = [rings * self.height + x for x in range(self.height)]
            RINGS_AROUND.append(meridian)

        self.VERT_RINGS = []
        self.VERT_RINGS.append(RINGS_AROUND[8])
        for ring in range(7,-1,-1):
            concat = sum([RINGS_AROUND[ring], RINGS_AROUND[16-ring]], [])
            self.VERT_RINGS.append(concat)
        for ring in range(8):
            concat = sum([RINGS_AROUND[31-ring], RINGS_AROUND[17+ring]], [])
            self.VERT_RINGS.append(concat)
        self.VERT_RINGS.append(RINGS_AROUND[24])
        
    def load_model(self, filename):

        with open(filename) as data_file:    
            data = json.load(data_file)
        print "Loading model: %s" % filename

        self.model = [x['point'] for x in data]          # making it a bit easier

