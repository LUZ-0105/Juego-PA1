import pygame 
from sys import exit


#Variables del juego

GAME_WIDTH = 360
GAME_HEIGHT = 640

#game imagenes 
backgroung_image = pygame.image.load("sky.png")


def draw(): 
    window.blit(backgroung_image, (0, 0))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH , GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

    draw()
    pygame.display.update()
    clock.tick(60)  #60 fps
