import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# from stable_baselines import PPO2
from environment import MA_gym
import argparse
import pygame

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FPS')
    parser.add_argument('--fps', type=int, help='game fps')
    args = parser.parse_args()
    env = MA_gym(args.fps)
    env.update_display()

    #env.close
