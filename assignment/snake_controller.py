import gym
from gym import wrappers
from math import cos, sin, acos, asin, atan, pi
import numpy as np
import snake
import glfw


class controller():

    def __init__(self):
        self.env = gym.make('Snake-v0')
        self.time_steps = 1000000000
        self.sim_timestep = 0.005 #[s] 

    def set_snake(self):
        
        obs = self.env.reset()
        time_steps = self.time_steps

        return  time_steps


    def control(self, time_step):
        self.env.render()

        #mujoco window size
        width,height = 1000,900
        glfw.set_window_size(self.env.viewer.window, width, height)

        t = time_step*self.sim_timestep #real time        
        
        action = self.action(t) #get action

        obs, reward, done, info = self.env.step(action)

        return obs
    
    "-------- change here -------------------------------------------------------------------------------------"
    def action(self, t):
        action = np.zeros(12) # joint angle -pi/4 ~ pi/4
        action[0] = sin(t)

        return action
    "-----------------------------------------------------------------------------------------------------------"




def main():

    ctrl = controller()

    time_steps = ctrl.set_snake()

    for time_step in range(time_steps):

        ctrl.control(time_step)


if __name__=="__main__":
    main()
