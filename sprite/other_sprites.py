import pygame
from pygame.math import Vector2
from pygame.locals import *
import numpy as np
import copy
pygame.font.init()
class Button(pygame.sprite.Sprite):

    BLACK = (0, 0, 0)
    FRONT = pygame.font.SysFont(None, 18)
    def __init__(self,posx,posy,TEXT = 'OPEN'):
        super().__init__()
        self.image = pygame.Surface((60,30))
        self.image.fill((128,255,0))
        self.rect = self.image.get_rect()
        self.posx,self.posy = posx,posy
        self.rect.center = Vector2(posx+30,posy+15)
        img = Button.FRONT.render(TEXT, True, Button.BLACK)
        self.image.blit(img, (10, 10))

    def update(self,screen):
        self.draw(screen)
        return self.click()

    def draw(self,screen):
        screen.blit(self.image, (self.posx,self.posy))

    def click(self):
       if self.rect.collidepoint(pygame.mouse.get_pos()):
           if pygame.mouse.get_pressed()[0]:
               return True

class arrival_timeline(pygame.sprite.Sprite):

    def __init__(self,):
        super().__init__()
        self.surface = pygame.Surface((320,640), pygame.SRCALPHA, 32).convert_alpha()
        self.image = pygame.transform.scale(pygame.image.load(f"./images/Arrival_timeline.JPG"),(160,640)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(1600+100*0.8,50+400*0.8)

    def update(self,screen,time_line_group,toggle):

        if toggle:
            self.surface = pygame.Surface((320,640), pygame.SRCALPHA, 32).convert_alpha()
            self.image = pygame.transform.scale(pygame.image.load(f"./images/Arrival_timeline.JPG"),(160,640)).convert_alpha()
            self.rect = self.image.get_rect()
            self.surface.blit(self.image,(80,0))
            self.rect.center = Vector2(1600+100*0.8,50+400*0.8)
            for i in time_line_group:
                i.update(self.surface,toggle)
            self.draw(screen)
        else:
            for i in time_line_group:
                i.update(self.surface,toggle)

    def draw(self,screen):
        screen.blit(self.surface, (1600,50))

class timeline_for_plane(pygame.sprite.Sprite):

    GREEN = (0, 255, 0)
    FRONT = pygame.font.SysFont(None, 25)
    def __init__(self,total_indx,flight_no,type_traj,cutoff_point):
        super().__init__()
        self.type = type_traj
        self.image = pygame.transform.scale(pygame.image.load(f"./images/Timeline_bracket{str(self.type)}.png"),(80,20)).convert_alpha()
        self.rect = self.image.get_rect()
        self.total_indx = cutoff_point
        self.indx = 0
        self.flight_no = flight_no

        #self.rect.center = Vector2(30,30)

    def update(self,screen,toggle):

        if toggle:
            self.image = pygame.transform.scale(pygame.image.load(f"./images/Timeline_bracket{str(self.type)}.png"),(120,30)).convert_alpha()
            remianing_time = round((self.total_indx-self.indx)/60,3)
            TEXT = 'F No: '+str(self.flight_no)#+'  Remaining time: '+str(remianing_time)+' mins'
            img = timeline_for_plane.FRONT.render(TEXT, True, timeline_for_plane.GREEN)
            if self.flight_no%2:
                self.image.blit(img,(5,5))
                screen.blit(self.image, (10, 615-((self.total_indx-self.indx)/3600)*565-(668-655)))
            else:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.blit(img,(49,5))
                screen.blit(self.image, (190, 615-((self.total_indx-self.indx)/3600)*565-(668-655)))
        if self.indx >= self.total_indx-1:
            self.kill()
        self.indx+=1
