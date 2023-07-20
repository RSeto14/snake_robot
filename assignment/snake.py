import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

from math import cos, sin, acos, asin, atan, pi
import numpy as np
from gym.envs.registration import register
import os



class SnakeEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        utils.EzPickle.__init__(self)
        xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snake.xml')
        mujoco_env.MujocoEnv.__init__(self, xml_path,3)#mujoco_env.MujocoEnv.__init__(self, xml_path,self.frame_skip)

    def step(self, a):
        
        self.do_simulation(a,3)
        #self.do_simulation(a, self.frame_skip)
        obs = self._get_obs()
        done = False
        reward = 1
        info = {}
        return obs, reward,done,info

    
    def viewer_setup(self):
        self.viewer.cam.trackbodyid = 0

    
    def reset_model(self):
        qpos = self.init_qpos
        "-------- change here -------------------------------------------------------------------------------------"
        for i in range(12):
            qpos[8+2*i] = 0
        "-----------------------------------------------------------------------------------------------------------"
        self.set_state(qpos,self.init_qvel)
        return self._get_obs()

    def _get_obs(self):
        obs =[]
        for i in range(12):
            obs.append(self.sim.data.qpos[8+2*i])
        #print(self.sim.data.qpos)
        #print("obs",obs)
        return np.concatenate([obs])

register(
id='Snake-v0',
entry_point='snake:SnakeEnv',
max_episode_steps=1000000000,
)
