import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Pantalla
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Mejorado")

# Reloj
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Cargar imágenes de fondo y tuberías
background = pygame.image.load("sky.png")
tuberiaSuperior = pygame.image.load("tuberia_superior.png")
tuberiaInferior = pygame.image.load("tuberia_inferior.png")

# ---------------------------
#     MANEJO DE SKINS
# ---------------------------

skins = {
    "yellow": [
        pygame.image.load("bird_yellow1.png"),
        pygame.image.load("bird_yellow2.png"),
        pygame.image.load("bird_yellow3.png")
    ],
    "red": [
        pygame.image.load("bird_red1.png"),
        pygame.image.load("bird_red2.png"),
        pygame.image.load("bird_red3.png")
    ],
    "blue": [
        pygame.image.load("bird_blue1.png"),
        pygame.image.load("bird_blue2.png"),
        pygame.image.load("bird_blue3.png")
    ]
}

selected_skin = "yellow"
current_frame = 0
frame_counter = 0

def get_bird_frame():
    global current_frame, frame_counter
    frame_counter += 1
    if frame_counter >= 8:  # velocidad animación
        current_frame = (current_frame + 1) % 3
        frame_counter = 0
    return skins[selected_skin][current_frame]

# ---------------------------
#     RÉCORD
# ---------------------------

def load_record():
    if not os.path.exists("record.txt"):
        with open("record.txt", "w") as f:
            f.write("0")
        return 0
    with open("record.txt", "r") as f:
        return int(f.read())

def save_record(score):
    record = load_record()
    if score > record:
        with open("record.txt", "w") as f:
            f.write(str(score))

# ---------------------------
#     BOTONES
# ---------------------------

class Button:
    def __init__(self, text, x, y):
        self.font = pygame.font.SysFont("Arial", 30)
        self.text = text
        self.image = self.font.render(text, True, WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------------------
#     VARIABLES DEL JUEGO
# ---------------------------

def reset_game():
    return 200, 150, 0, 200, 500, False, True, 0

def game_loop():

    global selected_skin

    birdY = 200
    bird_vel = 0
    pipe_x = 500
    pipe_gap = 150
    score = 0
    lost = False
    playing = True

    pause = False

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not lost:
                    bird_vel = -7
                if event.key == pygame.K_p:
                    pause = not pause

        if pause:
            font = pygame.font.SysFont("Arial", 40)
            pausetxt = font.render("PAUSA (P)", True, WHITE)
            screen.blit(pausetxt, (150, 200))
            pygame.display.update()
            continue

        if not lost:
            bird_vel += 0.5
            birdY += bird_vel
            pipe_x -= 4

            if pipe_x < -50:
                pipe_x = 500
                score += 1

            if birdY > 450 or birdY < 0:
                lost = True
                save_record(score)

            if (pipe_x < 50 < pipe_x + 50) and not (150 < birdY < 150 + pipe_gap):
                lost = True
                save_record(score)

        screen.blit(background, (0, 0))
        screen.blit(tuberiaSuperior, (pipe_x, -200))
        screen.blit(tuberiaInferior, (pipe_x, 150))

        screen.blit(get_bird_frame(), (50, birdY))

        font = pygame.font.SysFont("Arial", 30)
        scoretxt = font.render(f"Score: {score}", True, WHITE)
        screen.blit(scoretxt, (10, 10))

        if lost:
            losttxt = font.render("PERDISTE - ENTER para volver", True, RED)
            screen.blit(losttxt, (50, 200))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return "menu"

        pygame.display.update()
        clock.tick(30)

# ---------------------------
#     PANTALLA SKINS
# ---------------------------

def skin_menu():
    global selected_skin

    while True:
        screen.blit(background, (0, 0))

        font = pygame.font.SysFont("Arial", 40)
        title = font.render("Selecciona un Skin", True, WHITE)
        screen.blit(title, (100, 50))

        skins_buttons = {
            "yellow": Button("Amarillo", 250, 180),
            "red": Button("Rojo", 250, 260),
            "blue": Button("Azul", 250, 340)
        }

        for name, btn in skins_buttons.items():
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for name, btn in skins_buttons.items():
                    if btn.is_clicked(pos):
                        selected_skin = name
                        return "menu"

        pygame.display.update()

# ---------------------------
#     MENÚ PRINCIPAL
# ---------------------------

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        title_font = pygame.font.SysFont("Arial", 45)
        title = title_font.render("FLAPPY BIRD", True, WHITE)
        screen.blit(title, (130, 60))

        play_btn = Button("Jugar", 250, 200)
        skin_btn = Button("Skins", 250, 280)
        exit_btn = Button("Salir", 250, 360)

        play_btn.draw(screen)
        skin_btn.draw(screen)
        exit_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if play_btn.is_clicked(pos):
                    return "play"
                if skin_btn.is_clicked(pos):
                    return "skins"
                if exit_btn.is_clicked(pos):
                    return "exit"

        pygame.display.update()

# ---------------------------
#     LOOP PRINCIPAL
# ---------------------------

running = True
while running:
    menu = main_menu()

    if menu == "play":
        action = game_loop()
        if action == "exit":
            running = False

    elif menu == "skins":
        skin_menu()

    elif menu == "exit":
        running = False

pygame.quit()
