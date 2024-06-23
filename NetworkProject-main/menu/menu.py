from menu import *
import pygame as pg
import sys
from menu.settings import *
from menu.boutton_Menu import *

class Menu():
    def __init__(self, screen, lanceur):
        self.lanceur = lanceur
        self.screen = screen
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Constantia', 50)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.current = "Main"

        self.background = pg.transform.scale(background_of_menu, screen.get_size())

        self.background_name = pg.image.load(PATH + "background_name.png")
        self.longueur_image_menu_name = self.background_name.get_width()
        self.largeur_image_menu_name = self.background_name.get_height()
        self.new_longueur_image_menu_name = self.longueur_image_menu_name // 6
        self.new_largeur_image_menu_name = self.largeur_image_menu_name // 6
        self.background_name = pg.transform.scale(self.background_name, (self.new_longueur_image_menu_name, self.new_largeur_image_menu_name))

        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)

        self.displayed = True
        self.start = False
        self.load = False
        self.save = False
        self.pause = False

    def display_main(self):
        if self.displayed:
            self.Create_multiplayer = Button_Menu(self.screen, self.mid_width, self.mid_height + (GAP), 'Create Multiplayer Game')
            self.QUIT = Button_Menu(self.screen, self.mid_width, self.mid_height + (2* GAP), 'Good Bye')

    def events(self):
        for event in pygame.event.get():

            if self.Create_multiplayer.check_button(event):
                self.active = False
                return "create multiplayer"

            if self.QUIT.check_button(event):
                run = False
                sys.exit()

    def run(self):
        self.display_main()
        self.active = True
        while self.active:
            next = self.events()
            self.draw()
        return next

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background_name, (self.screen.get_width() // 2 - self.background_name.get_width() // 2, self.screen.get_height() // 4 - self.background_name.get_height() // 1.3))

        self.Create_multiplayer.draw()
        #self.Join_game.draw()
        self.QUIT.draw()

        pg.display.flip()
