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

        self.theta_max = pi/5
        self.alpha = 0

        self.T = 2 #[s]
        self.w = 2*pi/self.T #[rad/s]


    def set_snake(self):
        
        obs = self.env.reset()
        time_steps = self.time_steps

        alpha = self.alpha

        w = self.w
        theta_max = self.theta_max


        return  obs, alpha, time_steps, w, theta_max


    def control(self, alpha, time_step, w, theta_max ):
        self.env.render()

        #window size
        width,height = 1000,900
        #width,height = 2000,1000
        
        glfw.set_window_size(self.env.viewer.window, width, height)

        t = time_step*self.sim_timestep #実時間        
        
        action = self.action(alpha, w, t, theta_max)

        obs, reward, done, info = self.env.step(action)

        return obs
    
    def action(self, alpha, w, t, theta_max):
        action = np.zeros(12)
        for i in range(12):
            action[i] = theta_max*cos( pi/2  - i*pi/6 + w*t) + alpha*pi/10
            #action[11-i] = theta_max*cos( pi/2  - i*pi/6 + w*t) - alpha*pi/10 #forward <--> back

        return action




def main():

    ctrl = controller()

    obs,  alpha, time_steps, w, theta_max = ctrl.set_snake()

    for time_step in range(time_steps):

        obs = ctrl.control(alpha, time_step, w, theta_max)


if __name__=="__main__":
    main()
