import matplotlib.pyplot as plt
import random

class Sim(object):
    def __init__(self, cntrlr):
        print("Simulating")
        self.controller = cntrlr

    def run_multiple(self, instances):
        count = 0

        average_time = 0
        total_time = 0
        last_run = None
        last_error = 0

       
        plt.ion()
        plt.show()
       

        while count < instances:
            count += 1
            last_run, time, error= self.run()
            last_error = error
            total_time += time
            #self.graph_run(last_run)
            plt.cla()
            plt.plot(last_run)
            plt.legend( ('Throttle','Acc', 'Vel', 'Pos', "Target"), loc='upper left', shadow=True)
            plt.xlabel('steps (s)')
            plt.ylabel('distance (mV)')
            plt.title('About as simple as it gets, folks')
            plt.grid(True)
            plt.savefig("graph.png")
            plt.draw()
            plt.pause(0.001)
            

        average_time = total_time / instances
        print("Runs on avg took: " + str(average_time))    
        
        return (average_time, last_error)

    def run(self):
        is_done = False
        step_count = 0

        target_distance = random.uniform(0.5, 50)
        current_distance = 0

        left_speed_cof = random.uniform(0.8, 1.0)
        right_speed_cof = random.uniform(0.8, 1.0)

        max_accell = random.uniform(2.8,4)
        max_vel = random.uniform(2.5, 3.2)

        current_vel = 0
        current_accel = 0
        time_step = 0.1
        steps = []

        friction_coeff = random.uniform(0.5, 0.95)
        
        max_throttle = 0
        
        while not is_done:
            throttle = self.controller.process(current_distance, target_distance, current_vel, current_accel, step_count * time_step)
            
           # throttle *= left_speed_cof

            if throttle > max_throttle:
                max_throttle = throttle


            current_accel = max_accell * throttle
            current_accel -= (friction_coeff * current_vel)
            current_vel += time_step*current_accel
            

            current_vel = max(min(current_vel, max_vel), - max_vel)

        

            current_distance += current_vel * time_step
            step_count+=1
        
            steps.append( (throttle, current_accel ,current_vel, current_distance, target_distance))
            
            if abs(current_distance - target_distance) < 0.05 and abs(current_vel) < 0.05:
                is_done = True

            if step_count * time_step > 100:
                is_done = True

        time_total = step_count * time_step
        print("Took: " + str(time_total)  + "s. to go " + str(target_distance) + "m. Max Speed: " + str(max_throttle) + " avg speed " + str(target_distance/time_total))
        error_norm = ((target_distance - current_distance) / target_distance  )
        error_norm = abs(error_norm)
        #error_norm = max(min(error_norm, 1), 0)
        error_norm *= 10
        current_vel = current_vel / 5
        current_accel = current_accel / 5

        
        self.controller.result([error_norm , current_vel, current_accel, step_count * time_step], time_total)
       # error_norm = max(min(error_norm, 1), -1)
        return (steps, time_total, error_norm)
       
    def graph_run(self, run):
        plt.plot(run)
        
        

            
                

            