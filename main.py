import logging
from tkinter.constants import CENTER
import pygame, sys
import pygame_menu as pm
from astroid.bases import manager
from core.constants import CellValue
from core.logic import Logic
from core.state import World, GameState
from plotly.graph_objs import Volume
from pygame.examples.moveit import HEIGHT
from sympy.physics.units import volume
from tools.vector import vectorMulI, vectorSubDiv2I
from ui import UserInterface, Theme
from ui.mode import WorldGameMode
from ui.notification import Notification
from button import Button

pygame.init()
WIDTH = 665
HEIGHT = 614
CENTER = WIDTH // 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Main Menu")
pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

BG = pygame.image.load("assets/screen_cap_2.png")

def get_font(size):
    return pygame.font.Font('assets/font/lilliputsteps/lilliputsteps.ttf', size)

def play():
    while True:
        SCREEN.fill("black")

        # Load state
        world = World((100, 80))
        world.ground.fill(CellValue.GROUND_EARTH)
        state = GameState(world)
        state.load("level.json")
        logic = Logic(state)

        # Create a user interface and run it
        theme = Theme()
        tileSize = theme.getTileset("ground").tileSize
        theme.viewSize = vectorMulI((27, 15), tileSize)
        userInterface = UserInterface(theme)
        theme.init()
        # gameMode = EditGameMode(theme, logic)
        gameMode = WorldGameMode(theme, logic)
        userInterface.setGameMode(gameMode)
        worldSize = vectorMulI(state.world.size, tileSize)
        view = vectorSubDiv2I(worldSize, theme.viewSize)
        gameMode.viewChanged(view)
        background_sfx = pygame.mixer.Sound("assets/background-music.mp3")
        background_sfx.set_volume(0.1)
        background_sfx.play(-1)
        userInterface.run()
        userInterface.quit()
        Notification.getManager().checkEmpty()

def options():
    input_box = pygame.Rect(50, 150, 140, 32)
    color_inactive = pygame.Color('black')
    color_active = pygame.Color('grey')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        SCREEN.fill("white")
        SCREEN.blit(BG, (0, 0))
        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(CENTER, 45))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        VOLUME_TEXT = get_font(35).render("VOLUME 0.1-1.0:", True, "black")
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(input_box.x + 160, input_box.y - 35))
        SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

        # Render the current text.
        txt_surface = get_font(45).render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(SCREEN, color, input_box, 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                            volume = float(text)
                            print(volume)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        pygame.display.flip()
        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(55).render("IMMORTAL EMPIRES", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(CENTER, 35))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(CENTER, 250),
                                     text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(CENTER, 400),
                                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(CENTER, 550),
                                     text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()


