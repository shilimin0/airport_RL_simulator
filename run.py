import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# from stable_baselines import PPO2
from environment import MA_gym

import pygame

if __name__ == '__main__':
    env = MA_gym()
    env.update_display()

    #env.close
