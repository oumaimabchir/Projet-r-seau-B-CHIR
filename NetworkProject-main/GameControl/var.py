import pygame as pg
from GameControl.setting import *
import GameControl
from GameControl.gameControl import GameControl
pg.init()
pg.mixer.init()

selected_value_index = None



# Couleurs  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PATH = "./NetworkProject-main/assets/graphics/"

################ Game instance ################
setting = Setting.getSettings()
gameController = GameControl.getInstance()

settings_open = False
load_open = False
return_to_menu = False



# Création de la fenêtre en plein écran
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption("Game Menu")
#boutton
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 300
mid_width = (screen.get_width() // 2) - (WIDTH_BUTTON // 2)
mid_height = (screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
GAP = 75

#################################### Theme, musique et police ####################################
# Charger l'image de fond, plusieurs images disponibles dans le dossier (à en choisir une)
background_image = pg.image.load(PATH + "bg.png")
background_image = pg.transform.scale(background_image, screen.get_size())

background_image1 = pg.image.load(PATH + "bg.png")
background_image1 = pg.transform.scale(background_image1, screen.get_size())

background_image2 = pg.image.load(PATH + "bg.png")
background_image2 = pg.transform.scale(background_image2, screen.get_size())

# Police pour les boutons
font = pg.font.Font(None, 40)
####################################### ############################################################\

############################ Gestion des boutons ####################################################
# Déclaration des rectangles des boutons de base
button_width, button_height = 300, 50
big_button_width, big_button_height = 400, 400
play_button_rect = pg.Rect((screen.get_width() - button_width) // 2, 200, button_width, button_height)
settings_button_rect = pg.Rect((screen.get_width() - button_width) // 2, 300, button_width, button_height)
quit_button_rect = pg.Rect((screen.get_width() - button_width) // 2, 400, button_width, button_height)
back_button_rect = pg.Rect(20, 20, button_width, button_height)

grid_value_rects = dict()  # Réinitialise la liste des rectangles
grid_dict = { "FPS": setting.getFps() ,"GRID LENGTH": setting.getGridLength(),
               "NUMBER BOB": setting.getNbBob(), "NUMBER SPAWNED FOOD": setting.getNbSpawnFood(),  "FOOD ENERGY": setting.getFoodEnergy(),
               "BOB SPAWN ENERGY": setting.getBobSpawnEnergy(), "BOB MAX ENERGY": setting.getBobMaxEnergy() ,"BOB NEWBORN ENERGY": setting.getBobNewbornEnergy(), "SEXUAL BORN ENERGY": setting.getSexualBornEnergy(), 
               "BOB STATIONARY ENERGY LOSS": setting.getBobStationaryEnergyLoss(), "BOB SELF REPRODUCTION ENERGY LOSS": setting.getBobSelfReproductionEnergyLoss(), "BOB SEXUAL REPRODUCTION LOSS": setting.getBobSexualReproductionLoss(), "BOB SEXUAL REPRODUCTION LEVEL": setting.getBobSexualReproductionLevel(),
                "PERCEPTION FLAT PENALTY": setting.getPerceptionFlatPenalty(), "MEMORY FLAT PENALTY": setting.getMemoryFlatPenalty(),
                "DEFAULT VELOCITY": setting.getDefaultVelocity(), "DEFAULT MASS": setting.getDefaultMass(), "DEFAULT VISION": setting.getDefaultVision(), "DEFAULT MEMORY POINT": setting.getDefaultMemoryPoint(),
                "MASS VARIATION": setting.getMassVariation(), "VELOCITY VARIATION": setting.getVelocityVariation(), "VISION VARIATION": setting.getVelocityVariation() , "MEMORY VARIATION": setting.getMemoryVariation(),
                "SELF REPRODUCTION": setting.getSelfReproduction(),"SEXUAL REPRODUCTION": setting.getSexualReproduction()
               }

ingameparam = [ "FPS", "NUMBER SPAWNED FOOD" ,  "FOOD ENERGY", "BOB MAX ENERGY", "BOB NEWBORN ENERGY", "SEXUAL BORN ENERGY", "BOB STATIONARY ENERGY LOSS", "BOB SELF REPRODUCTION ENERGY LOSS", 
               "BOB SEXUAL REPRODUCTION LOSS", "BOB SEXUAL REPRODUCTION LEVEL", "PERCEPTION FLAT PENALTY", "MEMORY FLAT PENALTY"
               , "MASS VARIATION", "VELOCITY VARIATION", "VISION VARIATION" , "MEMORY VARIATION", "SELF REPRODUCTION", "SEXUAL REPRODUCTION" ]



grid_x = (screen.get_width() - len(max(grid_dict.keys(), key=len)) * 10) // 2
grid_y = (screen.get_height() - len(grid_dict.keys()) * 50) // 2