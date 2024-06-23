
import pygame as pg
import sys
import time
from GameControl.var import *
pg.init()
pg.mixer.init()

selected_value_index = None
from GameControl.setting import Setting
import GameControl.game as Game
from GameControl.gameControl import GameControl
from view.world import *
from view.utils import *
from Tiles.Bob import *
from Tiles.tiles import *
from GameControl.saveAndLoad import *
from network.file_py.net import *
from GameControl.join_waiting import *

# Fonction pour dessiner du texte sur l'écran
def drawText(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Fonction pour dessiner les boutons avec transparence 
def draw_transparent_button(text, rect, transparency):
    button_surface = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
    button_surface.fill((WHITE[0], WHITE[1], WHITE[2], transparency))
    screen.blit(button_surface, (rect.x, rect.y))
    drawText(text, WHITE, rect.x + rect.width // 2, rect.y + rect.height // 2)  # Utilisation du texte blanc

# Fonction pour dessiner les grilles avec transparence (la transparence des grilles des settings à revoir)
def draw_transparent_grids(labels, values, x, y, transparency):
    # global grid_value_rects
    # grid_value_rects = dict()  # Réinitialise la liste des rectangles
    cliquer = dict()
    for i, (label, value) in enumerate(zip(labels, values)):
        drawText(label, WHITE, x, y + 20 + i * 50) # Vẽ label thông số
        value_rect = pg.Rect(x + 320, y + i * 50, 200, 40) # Tạo hình chữ nhật thông số
        pg.draw.rect(screen, (WHITE[0], WHITE[1], WHITE[2], transparency), value_rect) # Vẽ hình chữ nhật thông số
        drawText(str(value), BLACK, x + 420, y + 20 + i * 50) # Vẽ giá trị thông số
        # grid_value_rects[label] = value_rect #  Pour cliquer 
        cliquer[label] = value_rect
    return cliquer

##############################################################################################################

########################################## openIngamesetting  ##########################################
def openIngamesetting():
    global selected_value_index, grid_value_rects, grid_dict, input_text, settings_open, ingameparam, input_active
    input_active = False
    input_text = ""
    back_button_rect = pg.Rect(20, 20, button_width, button_height)

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    # save_settings()
                    settings_open = False
                    return  # Retourner au menu principal
                
                # Vérifie si la souris a cliqué sur une valeur spécifique
                for key,value in grid_value_rects.items():
                    if value.collidepoint(event.pos):
                        selected_value_index = key
                        input_active = True
                        print("input_active")
                        # input_text = str(grid_dict[selected_value_index])  # Utiliser la valeur actuelle pour l'affichage initial
                        input_text = ""  # Utiliser la valeur actuelle pour l'affichage initial

            elif event.type == pg.KEYDOWN:
                if input_active:
                    valueEvaluator(event)
                            
        screen.blit(background_image, (0, 0))
        new = [(key,value) for key, value in grid_dict.items() if key in ingameparam]
        new1 = dict(new)
        labels = list(new1.keys())
        values = list(new1.values())
        # Dessiner les grilles avec transparence
        grid_value_rects.update(draw_transparent_grids(labels[:len(labels)//2], values[:len(values)//2], 400, 300, 50))
        grid_value_rects.update(draw_transparent_grids(labels[len(labels)//2:], values[len(values)//2:], 1300, 300, 50))
   


        # Dessiner le bouton de retour avec transparence  
        draw_transparent_button("BACK", back_button_rect, 1)
        # Si une valeur est sélectionnée, dessine un contour autour de cette valeur
        if selected_value_index is not None:
            pg.draw.rect(screen, WHITE, grid_value_rects[selected_value_index], 2)

        # Si l'entrée est active, affiche le texte saisi
        if input_active:
            # Effacer l'ancien texte avec un rectangle blanc
            pg.draw.rect(screen, WHITE, (grid_value_rects[selected_value_index].x, grid_value_rects[selected_value_index].y, 200, 40))
            input_surface = font.render(input_text, True, BLACK)  # Couleur de la police en noir
            input_rect = input_surface.get_rect(center=(grid_value_rects[selected_value_index].centerx, grid_value_rects[selected_value_index].centery))
            # pg.draw.rect(screen, WHITE, (input_rect.x - 5, input_rect.y - 5, input_rect.width + 10, input_rect.height + 10), border_radius=5)  # Couleur de fond du rectangle en blanc
            screen.blit(input_surface, input_rect)

        pg.display.flip()


        
def drawModifiable(surface, camera):
    etat = EtatJeu.getEtatJeuInstance()
    net = Network.getNetworkInstance()

    
    global mod_food, mod_bob, new_object_dict
    textureImg = loadGrassImage()
    flowImg = loadFlowerImage()
    darkGrass = loadDarkGrassImage()
    darkFlower = loadDarkFlowerImage()
    brightGrass = loadGrassBrightImage()
    brightFlower = loadFlowerBrightImage()
    
    net =Network.getNetworkInstance()
    etat=EtatJeu.getEtatJeuInstance()
    for row in gameController.getMap(): # x is a list of a double list Map
        for tile in row: # tile is an object in list
            territoire_true = net.this_client.color == 1 and tile.gridX < setting.gridLength//2 and tile.gridY < setting.gridLength//2 or\
                        net.this_client.color == 2 and tile.gridX < setting.gridLength//2 and setting.gridLength//2 <= tile.gridY or\
                        net.this_client.color == 3 and setting.gridLength//2 <= tile.gridX and setting.gridLength//2 <= tile.gridY or \
                        net.this_client.color == 4 and setting.gridLength//2 <= tile.gridX and tile.gridY < setting.gridLength//2 
    
            (x, y) = tile.getRenderCoord()
            offset = (x + setting.getSurfaceWidth()/2 , y + setting.getTileSize())
            a,b = offset
            if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                if tile.seen and not tile.hover:
                    if tile.flower:
                        surface.blit(flowImg, offset)
                    else:
                        surface.blit(textureImg, offset)
                else:
                    if tile.flower:
                        surface.blit(darkFlower, offset)
                    else:
                        surface.blit(darkGrass, offset)
                if tile.hover:
                    if not etat.online_game or territoire_true:
                        if tile.flower:
                            surface.blit(brightFlower, offset)
                        else:
                            surface.blit(brightGrass, offset)
                        tile.hover = False
            else: pass

    greenLeft = loadGreenLeft()
    blueLeft = loadBlueLeft()
    purpleLeft = loadPurpleLeft()

    explode1 = loadExplosionImage()[1]
    explode2 = loadExplosionImage()[2]
    explode3 = loadExplosionImage()[3]
    explode4 = loadExplosionImage()[4]
    explode5 = loadExplosionImage()[5]
    explode6 = loadExplosionImage()[6]
    explode7 = loadExplosionImage()[7]
    explode8 = loadExplosionImage()[8]

    spawn1 = loadSpawnImage()[1]
    spawn2 = loadSpawnImage()[2]
    spawn3 = loadSpawnImage()[3]
    spawn4 = loadSpawnImage()[4]
    spawn5 = loadSpawnImage()[5]
    spawn6 = loadSpawnImage()[6]
    spawn7 = loadSpawnImage()[7]
    spawn8 = loadSpawnImage()[8]
    

    for bob in gameController.listBobs:
        if (bob not in gameController.diedQueue) and (bob not in gameController.newBornQueue):
            # if(gameController.getTick() % 2 == 0 ):
                nbInteval = len(bob.getPreviousTiles()) - 1
                if ( gameController.renderTick < setting.getFps()/2):
                    if nbInteval == 0:
                        (destX, destY) = bob.getCurrentTile().getRenderCoord()
                        (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                        finish = (desX, desY + setting.getTileSize())
                        a,b = finish
                        if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                            bar_width = int((bob.energy / bob.energyMax) * 50)
                            pg.draw.rect(surface, (255, 0, 0), (finish[0], finish[1] - 5, bar_width, 5))
                            if bob.isHunting:
                                surface.blit(purpleLeft, finish)
                            else: surface.blit(greenLeft, finish)
                        else: pass
                    else:
                        for i in range( nbInteval):
                            if ( i*setting.getFps()) / (nbInteval * 2) <= gameController.renderTick < (i+1)*setting.getFps() / (nbInteval * 2):
                                (x, y) = bob.getPreviousTiles()[i].getRenderCoord()
                                (X, Y) = (x + surface.get_width()/2 , y - (50 - setting.getTileSize() ) )
                                (destX, destY) = bob.getPreviousTiles()[i+1].getRenderCoord()
                                (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                                pos = (X + (desX - X) * (gameController.renderTick - (i*setting.getFps())/(2 * nbInteval)) * (2 * nbInteval) / setting.getFps() , Y + (desY - Y) * (gameController.renderTick - (i*setting.getFps())/(2 * nbInteval) ) * (2 * nbInteval) / setting.getFps()  + setting.getTileSize()  )
                                a,b = pos
                                if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                                    bar_width = int((bob.energy / bob.energyMax) * 50)
                                    pg.draw.rect(surface, (255, 0, 0), (pos[0], pos[1] - 5, bar_width, 5))
                                    if bob.isHunting:
                                        surface.blit(purpleLeft, pos)
                                    else: surface.blit(greenLeft, pos)
                                else: pass
                            else: pass
                else:
                    (destX, destY) = bob.getCurrentTile().getRenderCoord()
                    (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                    finish = (desX, desY + setting.getTileSize())
                    a,b = finish
                    if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                        bar_width = int((bob.energy / bob.energyMax) * 50)
                        pg.draw.rect(surface, (255, 0, 0), (finish[0], finish[1] - 5, bar_width, 5))
                        if bob.isHunting:
                            surface.blit(purpleLeft, finish)
                        else: surface.blit(greenLeft, finish)
                    else: pass
    for bob in gameController.diedQueue:
        (x, y) = bob.getPreviousTile().getRenderCoord()
        (X, Y) = (x + surface.get_width()/2 , y - (50 - setting.getTileSize() ) )
        position = (X, Y)
        # print(bob.getNextTile())
        (destX, destY) = bob.getCurrentTile().getRenderCoord()
        (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
        start = (X + (desX - X) * (2 *gameController.renderTick/setting.getFps()), Y + (desY - Y) * (2* gameController.renderTick/setting.getFps()) + setting.getTileSize())
        finish = (desX, desY + setting.getTileSize())
        a , b = finish
        if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
            if (gameController.renderTick < setting.getFps()/2):
                surface.blit(greenLeft, start)
            elif setting.getFps()/2 <= gameController.renderTick < setting.getFps()/2 + setting.getFps()/16:
                surface.blit(explode1, finish)
            elif setting.getFps()/2 + setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 2*setting.getFps()/16:
                surface.blit(explode2, finish)
            elif setting.getFps()/2 + 2*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 3*setting.getFps()/16:
                surface.blit(explode3, finish)
            elif setting.getFps()/2 + 3*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 4*setting.getFps()/16:
                surface.blit(explode4, finish)
            elif setting.getFps()/2 + 4*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 5*setting.getFps()/16:
                surface.blit(explode5, finish)
            elif setting.getFps()/2 + 5*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 6*setting.getFps()/16:
                surface.blit(explode6, finish)
            elif setting.getFps()/2 + 6*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 7*setting.getFps()/16:
                surface.blit(explode7, finish)
            else:
                surface.blit(explode8, finish)
        else: pass

    for bob in gameController.newBornQueue:
        if bob not in gameController.diedQueue:
            (destX, destY) = bob.getCurrentTile().getRenderCoord()
            (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
            finish = (desX, desY + setting.getTileSize())
            a,b = finish
            if -64 <= (a  + camera.scroll.x) <= 1920 and -64 <= (b  + camera.scroll.y)  <= 1080:
                if gameController.renderTick < setting.getFps()/2:
                    pass
                elif setting.getFps()/2 <= gameController.renderTick < setting.getFps()/2 + setting.getFps()/16:
                    surface.blit(spawn1, finish)
                elif setting.getFps()/2 + setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 2*setting.getFps()/16:
                    surface.blit(spawn2, finish)
                elif setting.getFps()/2 + 2*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 3*setting.getFps()/16:
                    surface.blit(spawn3, finish)
                elif setting.getFps()/2 + 3*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 4*setting.getFps()/16:
                    surface.blit(spawn4, finish)
                elif setting.getFps()/2 + 4*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 5*setting.getFps()/16:
                    surface.blit(spawn5, finish)
                elif setting.getFps()/2 + 5*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 6*setting.getFps()/16:
                    surface.blit(spawn6, finish)
                elif setting.getFps()/2 + 6*setting.getFps()/16 <= gameController.renderTick < setting.getFps()/2 + 7*setting.getFps()/16:
                    surface.blit(spawn7, finish)
                else:
                    surface.blit(spawn8, finish)
            else: pass
    
    foodTexture = loadFoodImage()
    for food in gameController.getFoodTiles():
        (x, y) = food.getRenderCoord()
        (X, Y) = (x + surface.get_width()/2  , y - ( 50 - setting.getTileSize() ) )
        position = (X , Y + setting.getTileSize() )
        a,b = position
        if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
            
            bar_width = int((food.foodEnergy / setting.getFoodEnergy()) * 50)
            pg.draw.rect(surface, (0, 0, 255), (position[0] + 5, position[1] - 5, bar_width, 5))
            surface.blit(foodTexture, position)
        else: pass
    mouse_x, mouse_y = pg.mouse.get_pos()
    camera.update()
    if mod_bob:
        surface.blit(greenLeft, (mouse_x - greenLeft.get_width()//2 - camera.scroll.x, mouse_y - greenLeft.get_height()//2 - camera.scroll.y))
        listRect = []
        for row in gameController.getMap():
            for tile in row:
                 
                territoire_true = net.this_client.color == 1 and tile.gridX < setting.gridLength//2 and tile.gridY < setting.gridLength//2 or\
                        net.this_client.color == 2 and tile.gridX < setting.gridLength//2 and setting.gridLength//2 <= tile.gridY or\
                        net.this_client.color == 3 and setting.gridLength//2 <= tile.gridX and setting.gridLength//2 <= tile.gridY or \
                        net.this_client.color == 4 and setting.gridLength//2 <= tile.gridX and tile.gridY < setting.gridLength//2 
    
                (x,y) = tile.getRenderCoord()
                offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                a, b = offset
                if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                    if not etat.online_game or territoire_true: 
                        listRect.append((tile,(a + camera.scroll.x, b + camera.scroll.y)))

        for coord in listRect:
            if coord[1][0] <= mouse_x <= coord[1][0] + 64 and coord[1][1] + 8 <= mouse_y <= coord[1][1] + 24:
                print(coord[0].gridX, coord[0].gridY)
                coord[0].hover = True
                nb = 1
                # for bob in coord[0].getBobs():
                if ( mouse_y - 150 >= 0 ):
                    if ( mouse_x - 50*nb < 0 ):
                        pg.draw.rect(surface, (34, 139, 34), pg.Rect( mouse_x - camera.scroll.x +50 , mouse_y - camera.scroll.y -50 , 100 * nb, 100))
                        
                        draw_text(surface, f"Energy: {new_object_dict['Bob Energy']}", 15,(0,0,0),(mouse_x - camera.scroll.x +50  + 5 , mouse_y - camera.scroll.y -50 + 5))
                        draw_text(surface, f"Mass {new_object_dict['Bob Mass']}", 15,(0,0,0),(mouse_x - camera.scroll.x +50 + 5 , mouse_y - camera.scroll.y -50 + 15))
                        draw_text(surface, f"Vision {new_object_dict['Bob Vision']}",15,(0,0,0), ((mouse_x - camera.scroll.x +50 + 5 , mouse_y - camera.scroll.y -50 + 25)))
                        draw_text(surface, f"Velocity: {new_object_dict['Bob Velocity']}",15,(0,0,0), ((mouse_x - camera.scroll.x +50 + 5 , mouse_y - camera.scroll.y -50 + 35)))
                        draw_text(surface, f"Memory: {new_object_dict['Bob Memory Point']}",15,(0,0,0), ((mouse_x - camera.scroll.x +50 + 5 , mouse_y - camera.scroll.y -50 + 45)))
                        draw_text(surface, f"Food {new_object_dict['Food Energy']}",15,(0,0,0) , ((mouse_x - camera.scroll.x +50 + 5 , mouse_y - camera.scroll.y -50 + 55)))

                    elif( mouse_x + 50*nb > 1920  ):
                        pg.draw.rect(surface, (34, 139, 34), pg.Rect( mouse_x - camera.scroll.x - 50 - 100*nb , mouse_y - camera.scroll.y - 50 , 100 * nb, 100))

                        draw_text(surface, f"Energy: {new_object_dict['Bob Energy']}", 15,(0,0,0),(mouse_x - camera.scroll.x - 50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 5))
                        draw_text(surface, f"Mass {new_object_dict['Bob Mass']}", 15,(0,0,0),(mouse_x - camera.scroll.x -50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 15))
                        draw_text(surface, f"Vision {new_object_dict['Bob Vision']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 25)))
                        draw_text(surface, f"Velocity: {new_object_dict['Bob Velocity']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 35)))
                        draw_text(surface, f"Memory: {new_object_dict['Bob Memory Point']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 45)))
                        draw_text(surface, f"Food {new_object_dict['Food Energy']}",15,(0,0,0) , ((mouse_x - camera.scroll.x -50 -100*nb  + 5 , mouse_y - camera.scroll.y -50 + 55)))



                    else:
                        pg.draw.rect(surface, (34, 139, 34), pg.Rect( mouse_x - camera.scroll.x -50 * nb , mouse_y - camera.scroll.y - 150 , 100 * nb, 100))
                        draw_text(surface, f"Energy: {new_object_dict['Bob Energy']}", 15,(0,0,0),(mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 5))
                        draw_text(surface, f"Mass {new_object_dict['Bob Mass']}", 15,(0,0,0),(mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 15))
                        draw_text(surface, f"Vision {new_object_dict['Bob Vision']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 25)))
                        draw_text(surface, f"Velocity: {new_object_dict['Bob Velocity']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 35)))
                        draw_text(surface, f"Memory: {new_object_dict['Bob Memory Point']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 45)))
                        draw_text(surface, f"Food {new_object_dict['Food Energy']}",15,(0,0,0) , ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y -150 + 55)))

                else:
                    pg.draw.rect(surface, (34, 139, 34), pg.Rect( mouse_x - camera.scroll.x -50 * nb , mouse_y - camera.scroll.y + 50 , 100 * nb, 100))
                    draw_text(surface, f"Energy: {new_object_dict['Bob Energy']}", 15,(0,0,0),(mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 5))
                    draw_text(surface, f"Mass {new_object_dict['Bob Mass']}", 15,(0,0,0),(mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 15))
                    draw_text(surface, f"Vision {new_object_dict['Bob Vision']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 25)))
                    draw_text(surface, f"Velocity: {new_object_dict['Bob Velocity']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 35)))
                    draw_text(surface, f"Memory: {new_object_dict['Bob Memory Point']}",15,(0,0,0), ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 45)))
                    draw_text(surface, f"Food {new_object_dict['Food Energy']}",15,(0,0,0) , ((mouse_x - camera.scroll.x -50 * nb  + 5 , mouse_y - camera.scroll.y + 50 + 55)))
    if mod_food:
        surface.blit(foodTexture, (mouse_x - foodTexture.get_width()//2 - camera.scroll.x, mouse_y - foodTexture.get_height()//2 - camera.scroll.y))
        listRect = []
        for row in gameController.getMap():
            for tile in row: 
                territoire_true = net.this_client.color == 1 and tile.gridX < setting.gridLength//2 and tile.gridY < setting.gridLength//2 or\
                        net.this_client.color == 2 and tile.gridX < setting.gridLength//2 and setting.gridLength//2 <= tile.gridY or\
                        net.this_client.color == 3 and setting.gridLength//2 <= tile.gridX and setting.gridLength//2 <= tile.gridY or \
                        net.this_client.color == 4 and setting.gridLength//2 <= tile.gridX and tile.gridY < setting.gridLength//2 

                (x,y) = tile.getRenderCoord()
                offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                a, b = offset
                if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                    if not etat.online_game or territoire_true:
                        listRect.append((tile,(a + camera.scroll.x, b + camera.scroll.y)))
        for coord in listRect:
            if coord[1][0] <= mouse_x <= coord[1][0] + 64 and coord[1][1] + 8 <= mouse_y <= coord[1][1] + 24:
                print(coord[0].gridX, coord[0].gridY)
                coord[0].hover = True

