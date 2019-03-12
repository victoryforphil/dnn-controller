import matplotlib.pyplot as plt
import numpy as np
from sim import Sim
from controller import Controller
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense, Activation
from keras.utils import plot_model
from ann_visualizer.visualize import ann_viz;
import keras.backend as K


model = Sequential()
model.add(Dense(8, input_dim=4))
model.add(Dense(4))
model.add(Dense(1))
model.summary()
#plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
ann_viz(model, title="My first neural network")
model.compile(optimizer=Adam(lr=0.05),loss='mse', metrics=['mae'])

cntrl = Controller(model)

sim_inst = Sim(cntrl)

error = sim_inst.run_multiple(100)
   


print("done")