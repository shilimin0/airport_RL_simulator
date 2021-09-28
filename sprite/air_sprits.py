import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np
import copy
import json
from sprite.ground_sprites import *
from sprite.other_sprites import *

pygame.font.init()
radius_time = 120
class Arrival_controller(object):


    def load_traj(self,):
        FILE_NAME = './data/final_adjusted_coord.json'
        with open(FILE_NAME,'r') as f:
            raw_traj = json.load(f)['raw_traj']
        processed_traj = [[] for _ in range(4)]
        for ind,sub in enumerate(raw_traj):
            for line in sub:
                processed_traj[ind].append(np.array(line)+ np.array([839,480])+np.array([-10,-10]))
        self.traj = processed_traj

    def load_holding_point(self,):
        FILE_NAME = './data/holding_point.json'
        with open(FILE_NAME,'r') as f:
            self.holding_point = json.load(f)['holding_point']

    def invoke_random_interval(self,):
        return int(np.random.normal(300, 20, 1)[0])

    def invoke_random_departure_interval(self,):
        return int(np.random.normal(5, 10, 1)[0])

    def init_button(self,):
        self.toggle_button_open = Button(900,20,'OPEN')
        self.toggle_button_close = Button(1000,20,'CLOSE')

    def init_timeline(self,):
        self.timeline = arrival_timeline()
        FILE_NAME = './data/timeline_cutoff.json'
        with open(FILE_NAME,'r') as f:
            self.cutoff_point = json.load(f)['cut_off']

    def __init__(self,mode):
        self.mode = '' #mode
        self.Departure_entry = Departure_entry()
        self.group = pygame.sprite.Group()
        self.departure_group = pygame.sprite.Group()
        self.ground_arrival_plane_group = pygame.sprite.Group()
        self.release_index = 0
        self.departure_release_index = 0
        self.interval = self.invoke_random_interval()
        self.crash_in_air = 0
        self.load_holding_point()
        self.load_traj()
        self.flight_no = 0
        self.toggle = False
        self.departure_group_radar = pygame.sprite.Group()
        if self.mode != 'training':
            self.init_button()
            self.init_timeline()
            self.time_line_group = pygame.sprite.Group()



    def collide_checker_on_air(self,):
        tmp_group = self.group.copy()
        check_group = self.group.copy()
        for i in tmp_group:
            if len(i.traj)-i.frame_index>=340:
                tmp_group.remove(i)
                check_group.remove(i)
        for i in check_group:
            tmp_group.remove(i)
            crash_list = pygame.sprite.spritecollide(i,tmp_group,True,collided=pygame.sprite.collide_rect_ratio(.6))
            if crash_list:
                for fl in crash_list:
                    for timeline in self.time_line_group:
                        if timeline.flight_no == fl.flight_no or timeline.flight_no == i.flight_no:
                            timeline.kill()
                    for on_ground in self.ground_arrival_plane_group:
                        if on_ground.flight_no == fl.flight_no or on_ground.flight_no == i.flight_no:
                            on_ground.kill()
            self.crash_in_air+=len(crash_list )
            tmp_group.add(i)

    def collide_checker_on_ground(self,):
        for i in self.departure_group:
            if i.release:
                j = pygame.sprite.spritecollide(i,self.ground_arrival_plane_group,True)
                if j:
                    i.kill()
                    for on_air in self.group:
                        if on_air.flight_no == j[0].flight_no:
                            on_air.kill()

                    for timeline in self.time_line_group:
                        if timeline.flight_no == j[0].flight_no:
                            timeline.kill()
                    return True
        return False


    def update(self, frame_index, radar_screen, airport_screen):
        #######################################
        #showing mode
        if self.mode != 'training':
            open = self.toggle_button_open.update(radar_screen)
            if open:
                self.toggle = True
            close = self.toggle_button_close.update(radar_screen)
            if close:
                self.toggle = False
        if self.mode != 'training':
            self.timeline.update(radar_screen,self.time_line_group,self.toggle)
        #######################################
        self.Departure_entry.update(airport_screen)
        # add flight into it
        if frame_index-self.release_index > self.interval:
            size = np.random.choice(['MEDIUM','LIGHT','HEAVY'])
            type_traj = np.random.choice(4)
            sub_traj = np.random.choice(len(self.traj[type_traj]))
            holding_index = self.holding_point[type_traj][sub_traj]
            delay_round=np.random.choice([0,0,0,0,0,0,0,1,2,3])
            new_airplane = Airplane(self.flight_no, type_traj, copy.deepcopy(self.traj[type_traj][sub_traj]),holding_index,'Arrival', size=size, delay_round=delay_round)
            self.group.add(new_airplane)
            #######
            #showing mode
            if self.mode != 'training' :
                self.time_line_group.add(timeline_for_plane(len(new_airplane.traj),new_airplane.flight_no,type_traj,self.cutoff_point[type_traj][sub_traj]+delay_round*radius_time))
            #######
            self.flight_no+=1
            self.release_index = frame_index
            self.interval = self.invoke_random_interval()

        if not pygame.sprite.spritecollideany(self.Departure_entry,self.departure_group) and frame_index - self.departure_release_index>self.invoke_random_departure_interval():
            self.departure_group.add(Ground_departure_plane(self.flight_no)) #test
            self.departure_release_index= frame_index

        #update pos of each flight when appear in the ground
        for i in self.group:
            if len(i.traj) - i.frame_index == 300:
                self.ground_arrival_plane_group.add(Ground_arrival_plane(i.flight_no, copy.deepcopy(i.traj[-300::]), i.type, i.size))
            if self.toggle:
                i.update(radar_screen,True)
            else:
                i.update(radar_screen)


        for i in self.ground_arrival_plane_group:
            i.update(airport_screen)

        for i in self.departure_group:
            i.update(airport_screen,self.departure_group_radar,self.departure_group)
        self.departure_group_radar.update(radar_screen)
        #check for the collide
        self.collide_checker_on_air()
        self.collide_checker_on_ground()




class Airplane(pygame.sprite.Sprite):


    FRONT = pygame.font.SysFont(None, 30)
    #BLACK = (0, 0, 0)
    #RED = (255, 0, 0)
    #GREEN = (0, 255, 0)
    #BLUE = (0, 0, 255)
    #GRAY = (200, 200, 200)
    #YELLOW = (255,255,0)
    color_map = {0:(255,255,0),1:(255, 0, 0),2:(255,255,255),3:(0, 255, 0)}

    def load_img(self, type, size):
        self.surface = pygame.Surface((80,80), pygame.SRCALPHA, 32).convert_alpha()
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(20,20)).convert_alpha()
        self.rect = self.image.get_rect()
        self.type = type
        self.size = size


    def traj_preprocessing(self, traj,holding_index ,delay_round):
        #for mutiple circle delay

        traj = np.array(traj)
        speed = np.sqrt(np.sum((traj[holding_index] -traj[holding_index-2])**2))
        radius = speed*radius_time/(4*np.pi)
        direction = traj[holding_index] -traj[holding_index-4]
        unit = (direction/np.linalg.norm(direction, axis=0))*radius
        center= np.empty_like(direction)
        center[0] = -unit[1]
        center[1] = unit[0]
        center = center + traj[holding_index]
        #angle = self.rotate_circle(center[0],center[1])
        theta = np.linspace(0, 2*np.pi, int(radius_time))
        x1 = -radius*np.cos(theta)+center[0]   #anticlock-wise
        x2 = -radius*np.sin(theta)+center[1]
        circle = np.stack((x1,x2),axis = 1)     # create the figure
        dis = np.sum((circle - traj[holding_index])**2,axis = 1)
        start_indx = np.argmin(dis)
        circle = np.vstack((circle[start_indx+1::],circle[:start_indx]))
        circle = np.tile(circle,(delay_round,1))
        final_traj = np.vstack((traj[:holding_index+1],circle,traj[holding_index+1::]))
        return final_traj


    def __init__(self,flight_no,type_traj,  traj,holding_index ,type='Arrival', size='MEDIUM', delay_round=0):
        super().__init__()
        self.flight_no = flight_no
        self.frame_index = 0
        self.load_img(type,size)
        self.traj = self.traj_preprocessing(traj, holding_index, delay_round) + np.array([158,-29])
        self.type_traj = type_traj

    def draw(self,rotated_image,screen,open_numbr=False):
        if open_numbr:
            img = Airplane.FRONT.render(str(self.flight_no), True, Airplane.color_map[self.type_traj])
            rotated_image.blit(img, (25, 0))
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
        dx,dy = (self.traj[self.frame_index+1] - self.traj[self.frame_index])*np.array([1,-1])
        vector_1 = np.array([0, 1])
        vector_2 = np.array([dx, dy])
        cosTh = np.dot(vector_1,vector_2)
        sinTh = np.cross(vector_1,vector_2)
        res = np.rad2deg(np.arctan2(sinTh,cosTh))
        return res
