from keras.models import Sequential
from keras.layers import Dense, Activation
from sim import Sim
import numpy
class Controller(object):
    def __init__(self, model):
        self.model = model
        self.last_state = [0,0,0]
        self.itr = 0

    def update_mode(self, new):
        self.model = new

    def process(self, current_pos, target_pos, current_vel, current_accel, time):
        self.itr +=1
        error_norm = (target_pos - current_pos) / target_pos 
      
        current_vel = current_vel / 5
        current_accel = current_accel / 5

        

        self.last_state = numpy.array([error_norm, current_vel, current_accel, time])

        self.last_state = self.last_state.reshape(-1,4)

        #print(self.last_state.shape)

        out = self.model.predict(self.last_state)
       # print(out)
        out = out[0][0]
        out = max(min(out, 1), -1)
      
       # print(str(self.last_state) + " -> " + str(out))
        return out
    def result(self, state, time):
        state =  numpy.array(state)
        state = state.reshape(-1,4)
        print(str(numpy.abs(state)))
        self.model.fit(state, [0], epochs=1) 
        self.itr = 0
     