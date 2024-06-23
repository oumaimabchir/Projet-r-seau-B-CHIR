import pygame as pg
from GameControl.game import Game
from GameControl.EventManager import show_menu, EtatJeu, open_network_setting, waiting_room
from GameControl.game_online import Game_Online
from pygame.locals import *
from GameControl.setting import Setting
import sys

flags = HWSURFACE | DOUBLEBUF

def main():
    pg.init()
    pg.mixer.init()
    
    # Get the current display's dimensions
    display_info = pg.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    
    # Set up the screen to fit the display dimensions
    screen = pg.display.set_mode((screen_width, screen_height), flags)

    clock = pg.time.Clock()
    
    etat = EtatJeu.getEtatJeuInstance()
    
    while etat.running:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                etat.running = False
        
        if etat.open_menu:
            show_menu(screen, clock)
        elif etat.playing:
            game = Game.getInstance(screen, clock)
            if etat.game_instance == 0:
                game.createNewGame()
            else: 
                game.loadGame(etat.game_instance)
            game.run()
        elif etat.online_menu:
            open_network_setting(screen, clock)
        elif etat.waiting_room:
            waiting_room(screen, clock)
        elif etat.online_game:
            game_online = Game_Online.getInstance(screen, clock)
            if etat.game_instance == 0:
                game_online.createNewGame()
            else: 
                game_online.loadGame(etat.game_instance)
            game_online.run()
        
        # Update the display
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
