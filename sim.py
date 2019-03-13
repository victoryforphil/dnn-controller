import matplotlib.pyplot as plt
import random
import numpy as np

class Simulator (object):
    def __init__(self):
        
        self.time_step = 0.1 #0.1s per step

        self.current_state = None
        self.current_accel = 0 # Set on reset
        self.current_vel   = 0
        self.current_pos   = 0
        self.current_tgt   = 0 # Set on reset
        self.current_dif   = 0
        self.current_step  = 0
        self.current_input = 0 
        self.current_fric  = 0 # Set on reset
        self.current_done  = False;

        self.max_accel = 4.0
        self.min_accel = 3.0
        self.max_vel   = 3.9
        self.max_tgt   = 20.0
        self.min_tgt   = 10.0
        self.max_fric  = 0.9
        self.min_fric  = 0.4
        self.max_step  = 100

        self.reset()

    def get_input_dims(self):
        return len(self.get_current_state())

    def dqn_step(self, input):
        new_state = self.simulate(input)
        reward = self.calculate_reward(new_state)
        done = self.current_done
        return (new_state, reward, done)

    def simulate(self, input):

        if self.current_done:
            self.reset()
            return

        self.current_input = input

        self.current_accel  = self.current_accel * self.current_input
        self.current_accel -= (self.current_fric * self.current_vel)
        self.current_vel   += self.time_step * self.current_accel
        self.current_vel    = self.clamp(self.current_vel, -1.0, 1.0)

        self.current_pos  += current_vel * self.time_step
        self.current_step += 1

        self.current_dif = (self.current_tgt - self.current_pos)

        self.current_state = self.get_current_state()

        if self.current_step > self.max_step:
            self.current_done = True
            
        if abs(self.current_dif) < 0.1 and abs(self.current_vel) < 0.1 :
            self.current_done = True
        
        return self.current_state
    
    def get_current_state(self):
        return [self.current_dif, self.current_accel, self.current_vel]

    def clamp(self, val, minX, maxX):
        return max(min(val, maxX), minX)

    def calculate_error(self, state):
        error = state[0]
        error = error / self.current_tgt
        return abs(error)

    def calculate_reward(self, state):
        error = self.calculate_error(state)
        error = self.clamp(error, 0, 1.0)
        error_rwd = 1.0 - error

        velocity = self.state[2]
        velocity_rwd = 1.0 =abs(velocity)

        time = self.current_step / self.max_step

        reward = (velocity_rwd + time + error_rwd ) / 3
        return reward

    def reset(self):
        self.current_state = None
        self.current_accel = random.uniform(self.min_accel, self.max_accel)
        self.current_vel   = 0
        self.current_pos   = 0
        self.current_tgt   = random.uniform(self.min_tgt,   self.max_tgt)
        self.current_dif   = 0
        self.current_step  = 0
        self.current_input = 0
        self.current_fric  = random.uniform(self.min_fric,  self.max_fric)
        self.current_done  = False;
