import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np
import copy



class Arrival_controller(object):

    def load_traj(self,):
        self.traj = np.load('./data/customized.npy')

    def landing_traj_preprocessing(self,):
        #for consider of reduce computing complex
        landing_traj = copy.deepcopy(self.traj[0][-107:,:])
        frames = len(landing_traj)
        percentage = np.sum((landing_traj-landing_traj[-1])**2,axis = 1)
        percentage = percentage/percentage[0]
        runway_coord = np.array([[2000,150] for _ in range(len(percentage))])

        runway_coord[:,0] = runway_coord[:,0]*percentage
        runway_coord = runway_coord+np.random.normal(0,0.5,runway_coord.shape)
        return runway_coord

    def invoke_random_interval(self,):
        return int(np.random.normal(100, 1, 1)[0])

    def invoke_random_departure_interval(self,):
        return int(np.random.normal(100, 3, 1)[0])

    def __init__(self,):
        self.Departure_entry = Departure_entry()
        self.group = pygame.sprite.Group()
        self.departure_group = pygame.sprite.Group()
        self.ground_arrival_plane_group = pygame.sprite.Group()
        self.release_index = 0
        self.departure_release_index = 0
        self.interval = self.invoke_random_interval()
        self.crash = 0
        self.load_traj()
        self.landing_traj = self.landing_traj_preprocessing()
        self.flight_no = 0


    def collide_checker_on_air(self,):
        tmp_group = self.group.copy()
        check_group = self.group.copy()
        for i in tmp_group:
            if len(i.traj)-i.frame_index>=340:
                tmp_group.remove(i)
                check_group.remove(i)
        for i in check_group:
            tmp_group.remove(i)
            self.crash+=len(pygame.sprite.spritecollide(i,tmp_group,True) )
            tmp_group.add(i)

    def update(self, frame_index, radar_screen, airport_screen):
        self.Departure_entry.update(airport_screen)
        # add flight into it
        if frame_index-self.release_index > self.interval:
            size = np.random.choice(['MEDIUM','LIGHT','HEAVY'])
            sub_traj = np.random.choice(5)
            self.group.add(Airplane(self.flight_no, copy.deepcopy(self.traj[sub_traj]), self.landing_traj, 'Arrival', size=size, delay_round=np.random.choice([0,1,2,3])))
            self.flight_no+=1
            self.release_index = frame_index
            self.interval = self.invoke_random_interval()

        if not pygame.sprite.spritecollideany(self.Departure_entry,self.departure_group) and frame_index - self.departure_release_index>self.invoke_random_departure_interval():
            self.departure_group.add(Ground_departure_plane(self.flight_no)) #test
            self.departure_release_index= frame_index
            self.flight_no+=1

        #update pos of each flight
        for i in self.group:
            if len(i.traj) - i.frame_index == 107:
                self.ground_arrival_plane_group.add(Ground_arrival_plane(i.flight_no, self.landing_traj, i.type, i.size))
            i.update(radar_screen)

        for i in self.ground_arrival_plane_group:   #test
            i.update(airport_screen)                #test
        #check for the collide
        self.collide_checker_on_air()

        for i in self.departure_group:
            i.update(airport_screen)





class Airplane(pygame.sprite.Sprite):

    def load_img(self, type, size):
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(20,20)).convert_alpha()
        self.rect = self.image.get_rect()
        self.type = type
        self.size = size

    def traj_preprocessing(self, traj, delay_round):
        #for mutiple circle delay
        circle = traj[160:360,:]
        circle = np.tile(circle,(delay_round,1))
        if not len(circle):
            return np.vstack((traj[:160,:], traj[360:,:]))
        return np.vstack((traj[:160,:], circle, traj[360:,:]))


    def __init__(self,flight_no, traj, landing_traj, type='Arrival', size='MEDIUM', delay_round=0):
        super().__init__()
        self.flight_no = flight_no
        self.frame_index = 0
        self.load_img(type,size)
        self.traj = self.traj_preprocessing(traj, delay_round)
        self.landing_traj = landing_traj

    def draw(self,rotated_image,screen):
        screen.blit(rotated_image, self.rect.center)

    def update(self, radar_screen):
        self.rect.center = self.traj[self.frame_index]+np.array([-10,-10])
        angle = self.rotate()
        rotated_image = pygame.transform.rotate(self.image, angle)
        self.draw(rotated_image,radar_screen)
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

    #def ready_land(self,airport_screen):
        #if len(self.traj) - self.frame_index <= 107:

class Ground_arrival_plane(pygame.sprite.Sprite):

    def __init__(self, flight_no, traj, type='Arrival', size='MEDIUM'):
        super().__init__()
        self.flight_no = flight_no
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(40,40)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.frame_index = 0
        self.traj = traj

    def update(self, airport_screen):
        self.rect.center = self.traj[self.frame_index]+np.array([-20,-20])
        self.draw(airport_screen)
        self.frame_index+=1
        if self.frame_index >= len(self.traj)-1:
            self.kill()

    def draw(self, airport_screen):
        airport_screen.blit(self.image, self.rect.center)

class Ground_departure_plane(pygame.sprite.Sprite):
    desnation = np.array([[850,255],[910,255],[950,255],[950,205]])
    release_seq = np.array([[950,150],[0,150]])
    def __init__(self, flight_no, type='Departure', size='MEDIUM', status = 1):
        super().__init__()
        self.flight_no = flight_no
        self.reached_take_off_point = False
        self.image =  pygame.transform.scale(pygame.image.load(f"./images/planes/{type}/{size}.png"),(40,40)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.status = status
        #self.rect.center = [750-30,265-30]#Vector2([750,1065])
        self.frame_index = 0
        self.pos = np.array([720,255])
        self.speed = np.array([1,0])#Vector2(0.05,0)
        self.period = 0
        self.release = False

    def update(self,airport_screen):
        if self.release:
            if self.rect.center==(950,130):
                self.speed = np.array([-1,0])
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.rect.center[1]==130:
                self.speed = self.speed + np.array([-0.25,0])

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

    def draw(self,airport_screen):
        airport_screen.blit(self.image, self.rect.center)

class Departure_entry(pygame.sprite.Sprite):
    def __init__(self,):
        self.image = pygame.Surface((40,40), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center=(720,255)

    def update(self,runway_screen_image):
        self.draw(runway_screen_image)

    def draw(self,runway_screen_image):
        runway_screen_image.blit(self.image, (720,255))
