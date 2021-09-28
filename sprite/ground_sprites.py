import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np
import copy
import json
import os



class Ground_arrival_plane(pygame.sprite.Sprite):

    def transform_traj(self,traj):
        traj = np.array(traj) -  np.array([158,-29])
        rotation_matrix = np.array([[np.cos(1.166879),-np.sin(1.166879)],[np.sin(1.166879),np.cos(1.166879)]])
        traj = rotation_matrix.dot(traj.T).T
        traj[:,0] = traj[:,0]/0.012177966 - np.array([-8600.9]) + np.array([220])
        traj[:,1] = traj[:,1]/0.023095238 -  np.array([41002.9]) + np.array([60])
        return traj

    def __init__(self, flight_no, traj, type='Arrival', size='MEDIUM'):
        super().__init__()
        self.flight_no = flight_no
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(40,40)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.frame_index = 0
        self.traj = self.transform_traj(traj)


    def update(self, airport_screen):
        self.rect.center = self.traj[self.frame_index]#+np.array([-10,-10])
        angle = self.rotate()
        rotated_image = pygame.transform.rotate(self.image, angle-90)
        self.draw(rotated_image,airport_screen)
        self.frame_index+=1
        if self.frame_index >= len(self.traj)-1:
            self.kill()

    def rotate(self,):
        dx,dy = (self.traj[self.frame_index+1] - self.traj[self.frame_index])*np.array([1,-1])
        vector_1 = np.array([0, 1])
        vector_2 = np.array([dx, dy])
        cosTh = np.dot(vector_1,vector_2)
        sinTh = np.cross(vector_1,vector_2)
        res = np.rad2deg(np.arctan2(sinTh,cosTh))
        return res

    def draw(self, rotated_image,airport_screen):
        airport_screen.blit(rotated_image, self.rect.center)

    def rotated_image(self,degree):
        self.image = pygame.transform.rotate(self.image, degree)

class Ground_departure_plane(pygame.sprite.Sprite):

    desnation = np.array([[1160,230],[1220,230],[1280,230],[1280,160]])
    release_seq = np.array([[1280,64],[0,64]])

    def load_traj_depature(self,):
        with open('./data/precessed_runway_departure.json','r') as f:
            self.runway_traj_depature = json.load(f)
        with open('./data/precessed_radar_departure.json','r') as f:
            self.radar_traj_depature = json.load(f)
        self.runway_traj_depature , self.radar_traj_depature = np.array(self.runway_traj_depature), np.array(self.radar_traj_depature)


    def __init__(self, flight_no, type='Departure', size='MEDIUM', status = 0):
        super().__init__()
        self.size = size
        self.flight_no = flight_no
        self.reached_take_off_point = False
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(40,40)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.status = status
        self.frame_index = 0
        self.pos = np.array([1060,230])
        self.speed = np.array([1,0])#Vector2(0.05,0)
        self.period = 0
        self.release = False
        self.load_traj_depature()
        self.runway_traj = None
        self.on_runway = False


    def ready_take_off(self,):
        #print(self.rect.center[0] ,self.rect.center[1] ,self.rect.center[0] == 1280)
        return (self.rect.center[0] == 1280) and (self.rect.center[1] == 160)

    def update(self,airport_screen,departure_group_radar,departure_group):
        if self.on_runway:
            self.rect.center = self.runway_traj[self.frame_index]
        if self.rect.center[0] <=0:
            self.kill()
        if self.release and not self.on_runway:
            if self.rect.center==(1280,64):
                num = np.random.randint(len(self.radar_traj_depature))
                departure_group_radar.add(depature_on_radar(self.radar_traj_depature[num],'Departure',self.size))
                self.speed = np.array([-1,0])
                self.image = pygame.transform.rotate(self.image, 90)
                self.runway_traj = np.array(self.runway_traj_depature[num]) - np.array(self.runway_traj_depature[num][0]) + np.array([1280,64])
                self.frame_index = 0
                self.on_runway = True
            elif self.rect.center[1]==64:
                self.speed = self.speed + np.array([-0.25,0])
            else:
                self.speed = [0,-1]
                self.pos = self.pos + self.speed
                self.rect.center = self.pos
        if not self.on_runway and not self.check_front_jam(departure_group):
            self.pos = self.pos + self.speed
            self.rect.center = self.pos
        self.draw(airport_screen)
        if self.rect.center == tuple(Ground_departure_plane.desnation[-1]) and self.status:
            self.release = True
        elif self.rect.center == tuple(Ground_departure_plane.desnation[-1]):
            self.speed = np.array([0,0])
        elif self.rect.center == tuple(Ground_departure_plane.desnation[self.period]):
            self.speed =(Ground_departure_plane.desnation[self.period+1]-Ground_departure_plane.desnation[self.period])
            self.speed = self.speed/np.abs(self.speed)
            self.speed = np.where(np.isnan(self.speed ),0,self.speed)
            self.period+=1
            if self.period == 3:
                self.image = pygame.transform.rotate(self.image, 90)
        self.frame_index+=1

    def draw(self,airport_screen):
        airport_screen.blit(self.image, self.rect.center)

    def check_front_jam(self,departure_group):
        if self.period <=1:
            front = np.array([30,0])
        else:
            front = np.array([30,-30])
        self.rect.center = self.pos + front
        collide = len(pygame.sprite.spritecollide(self,departure_group,False))
        self.rect.center -= front
        return True if collide>1 else False

class Departure_entry(pygame.sprite.Sprite):

    def __init__(self,):
        self.image = pygame.Surface((80,800), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center=(1060,230)

    def update(self,runway_screen_image):
        self.draw(runway_screen_image)

    def draw(self,runway_screen_image):
        runway_screen_image.blit(self.image, (1060,230))

class depature_on_radar(pygame.sprite.Sprite):

    def load_img(self, type, size):
        self.surface = pygame.Surface((80,80), pygame.SRCALPHA, 32).convert_alpha()
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(20,20)).convert_alpha()
        self.rect = self.image.get_rect()
        self.type = type
        self.size = size

    def __init__(self, traj,type='Arrival', size='MEDIUM', ):
        super().__init__()
        self.frame_index = 0
        self.load_img(type,size)
        traj= np.array(traj)
        traj[:,1] = -traj[:,1]
        self.traj = traj+np.array([1000,447]) -np.array([10,10])

    def draw(self,rotated_image,screen,open_numbr=False):
        screen.blit(rotated_image, self.rect.center)


    def update(self, radar_screen, open_numbr = False):
        self.rect.center = self.traj[self.frame_index]#+np.array([-10,-10])
        angle = self.rotate()
        rotated_image = pygame.transform.rotate(self.image, angle)
        self.surface = pygame.Surface((80,80), pygame.SRCALPHA, 32).convert_alpha()
        self.surface.blit(rotated_image,(0,0))
        self.draw(self.surface ,radar_screen, open_numbr)
        self.frame_index+=1
        if self.frame_index >= len(self.traj)-1:
            self.kill()

    def rotate(self,):
        if self.frame_index<100:
            move_average = 50
        else:
            move_average = 1
        dx,dy = (self.traj[self.frame_index+move_average] - self.traj[self.frame_index])*np.array([1,-1])
        vector_1 = np.array([0, 1])
        vector_2 = np.array([dx, dy])
        cosTh = np.dot(vector_1,vector_2)
        sinTh = np.cross(vector_1,vector_2)
        res = np.rad2deg(np.arctan2(sinTh,cosTh))
        return res
