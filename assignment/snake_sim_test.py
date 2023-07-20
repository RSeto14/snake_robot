import gym
from gym import wrappers
from math import cos, sin, acos, asin, atan, pi
import numpy as np
import snake
import glfw

def main():

    ## Setting ################
    env = gym.make('Snake-v0')
    sim_timestep = 0.005 #[s]
    obs = env.reset()
    Done = False
    time_step = 0
    ###########################

    while Done == False:

        t = time_step*sim_timestep #real time        
        
        ## controller #################################################
        "-------- change here ----------------------------------------"
        action = np.zeros(12) # joint angle -pi/4 ~ pi/4
        action[0] = sin(t)
        "-------------------------------------------------------------"
        ###############################################################

        ## gym mujoco ##################################################
        env.render()
        glfw.set_window_size(env.viewer.window, width=1000, height=900)
        obs, reward, done, info = env.step(action)
        ################################################################

        time_step += 1




if __name__=="__main__":
    main()
