from __future__ import annotations
from typing import TYPE_CHECKING
import pygame as pg
import sys
from network.file_py.net import Network
from GameControl.setting import Setting
from view.utils import draw_text
from view.camera import Camera
from view.world import World
from GameControl.EventManager import *
from GameControl.gameControl import GameControl
from GameControl.saveAndLoad import *
from view.graph import *

class Game_Online:
    instance = None
    def __init__(self, screen, clock):
        self.setting = Setting.getSettings()
        self.gameController = GameControl.getInstance()
        self.network = Network.getNetworkInstance()
        self.etat = EtatJeu.getEtatJeuInstance()
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        
        self.camera = None

    def createNewGame(self):
        self.gameController.initiateGame()
        self.gameController.createWorld(self.setting.getGridLength(),self.setting.getGridLength()) 
        self.camera = Camera(self.width, self.height) 
        self.gameController.nbBobPut = 5
        # self.gameController.
        self.load_game()

    def load_game(self):
        for color, player in self.network.clientList.items():
            if player is not self.network.this_client and player is not None and player.ready:
                if player.ready_rep_pkg is None:
                    raise Exception("something is wrong !!!!")
                player.ready_rep_pkg.extractData()
                for data in player.ready_rep_pkg.data:
                    if data.type == BOB_STATUS:
                        bob = Bob()
                        bob.id = data.data['id']
                        bob.color = data.data['color']
                        for row in self.gameController.grid:
                            for tile in row:
                                if tile.getGameCoord() == data.data['currentTile']:
                                    bob.CurrentTile = tile
                                    tile.addBob(bob)
                                    break
                        for coord in data.data['previousTiles']:
                            for row in self.gameController.grid:
                                for tile in row:
                                    if tile.getGameCoord() == coord:
                                        bob.PreviousTiles.append(tile)
                        bob.energy = data.data['energy']
                        bob.mass = data.data['mass']
                        bob.velocity = data.data['velocity']
                        bob.speed = data.data['speed']
                        bob.vision = data.data['vision']
                        bob.memoryPoint = data.data['memoryPoint']
                        self.gameController.listBobs.append(bob)
                    elif data.type == FOOD_STATE:
                        for cas in data.data:
                            for row in self.gameController.grid:
                                for tile in row:
                                    if tile.getGameCoord() == cas['coord']:
                                        tile.foodEnergy = cas['foodEnergy']
                                        break
                    elif data.type == BOB_BORN:
                        bob = Bob()
                        bob.id = data.data['id']
                        bob.color = data.data['color']
                        for row in self.gameController.grid:
                            for tile in row:
                                if tile.getGameCoord() == data.data['currentTile']:
                                    bob.CurrentTile = tile
                                    tile.addBob(bob)
                                    break
                        for coord in data.data['previousTiles']:
                            for row in self.gameController.grid:
                                for tile in row:
                                    if tile.getGameCoord() == coord:
                                        bob.PreviousTiles.append(tile)
                        bob.energy = data.data['energy']
                        bob.mass = data.data['mass']
                        bob.velocity = data.data['velocity']
                        bob.speed = data.data['speed']
                        bob.vision = data.data['vision']
                        bob.memoryPoint = data.data['memoryPoint']
                        self.gameController.addToNewBornQueue(bob)

        def load_game(self):
            for color, player in self.network.clientList.items():
                if player is not self.network.this_client and player is not None and player.ready:
                    if player.ready_rep_pkg == None:
                        raise Exception("something is wrong!!")
                    player.ready_rep_pkg.extractData()
                    for data in player.ready_rep_pkg.data:
                        if data.type == BOB_STATUS:
                            bob = Bob()
                            bob.id = data.data['id']
                            bob.color = data.data['color']
                            for row in self.gameController.grid:
                                for tile in row:
                                    if tile.getGameCoord() == data.data['currentTile']:
                                        bob.CurrentTile = tile
                                        tile.addBob(bob)
                                        break
                            for coord in data.data['previousTiles']:
                                for row in self.gameController.grid:
                                    for tile in row:
                                        if tile.getGameCoord() == coord:
                                            bob.PreviousTiles.append(tile)
                            bob.energy = data.data['energy']
                            bob.mass = data.data['mass']
                            bob.velocity = data.data['velocity']
                            bob.speed = data.data['speed']
                            bob.vision = data.data['vision']
                            bob.memoryPoint = data.data['memoryPoint']
                            self.gameController.listBobs.append(bob)
                        elif data.type == FOOD_STATE:
                            for cas in data.data:
                                for row in self.gameController.grid:
                                    for tile in row:
                                        if tile.getGameCoord() == cas[0]:
                                            tile.foodEnergy = cas[1]
                                            break
                        elif data.type == BOB_BORN:
                            bob = Bob()
                            bob.id = data['id']
                            bob.color = data['color']
                            for row in self.gameController.grid:
                                for tile in row:
                                    if tile.getGameCoord() == data['currentTile']:
                                        bob.CurrentTile = tile
                                        tile.addBob(bob)
                                        break
                            for coord in data['previousTiles']:
                                for row in self.gameController.grid:
                                    for tile in row:
                                        if tile.getGameCoord() == coord:
                                            bob.PreviousTiles.append(tile)
                            bob.energy = data['energy']
                            bob.mass = data['mass']
                            bob.velocity = data['velocity']
                            bob.speed = data['speed']
                            bob.vision = data['vision']
                            bob.memoryPoint = data['memoryPoint']
                            self.gameController.addToNewBornQueue(bob)
    def run(self):
        self.playing = True
        self.gameController.phase = 1
        while self.playing:
            self.clock.tick(5 * self.setting.getFps())
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.etat.waiting_room = False
                        self.etat.online_menu = True
                        self.etat.online_game = False
                        self.playing = False
                        self.network.close_socket()
                        self.network.destroyNetwork()
                        return
                    elif event.key == pg.K_b:
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        listRect = []
                        for row in self.gameController.getMap():
                            for tile in row:
                                (x, y) = tile.getRenderCoord()
                                offset = (x + self.setting.getSurfaceWidth() // 2, y + self.setting.getTileSize())
                                a, b = offset
                                if -64 <= (a + self.camera.scroll.x) <= 1920 and -64 <= (b + self.camera.scroll.y) <= 1080:
                                    listRect.append((tile, (a + self.camera.scroll.x, b + self.camera.scroll.y)))
                        for coord in listRect:
                            if coord[1][0] < mouse_x < coord[1][0] + 64 and coord[1][1] + 8 < mouse_y < coord[1][1] + 24:
                                if self.gameController.nbBobPut > 0:
                                    self.gameController.add_bob_online(coord[0])
                                    self.gameController.nbBobPut -= 1
                    elif event.key == pg.K_n:
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        listRect = []
                        for row in self.gameController.getMap():
                            for tile in row:
                                (x, y) = tile.getRenderCoord()
                                offset = (x + self.setting.getSurfaceWidth() // 2, y + self.setting.getTileSize())
                                a, b = offset
                                if -64 <= (a + self.camera.scroll.x) <= 1920 and -64 <= (b + self.camera.scroll.y) <= 1080:
                                    listRect.append((tile, (a + self.camera.scroll.x, b + self.camera.scroll.y)))
                        for coord in listRect:
                            if coord[1][0] < mouse_x < coord[1][0] + 64 and coord[1][1] + 8 < mouse_y < coord[1][1] + 24:
                                self.gameController.add_food_online(coord[0])

            self.gameController.tick_online_update()
            sum = 0
            for bob in self.gameController.listBobs:
                sum += 1
            print(sum)
            self.network.listen()

            self.screen.fill((255, 255, 255))
            surface = pg.Surface((self.setting.getSurfaceWidth(), self.setting.getSurfaceHeight())).convert_alpha()
            surface.fill((255, 255, 255))
            self.drawModifiable_Online(surface, self.camera)
            self.screen.blit(surface, (self.camera.scroll.x, self.camera.scroll.y))
            self.drawIndex_Online(self.screen)
            pg.display.flip()

        if not self.etat.playing:
            return

    """ 
    def run(self):
        self.playing = True
        self.gameController.phase = 1
        while self.playing:
            self.clock.tick(5*self.setting.getFps())
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.etat.waiting_room = False
                        self.etat.online_menu = True
                        self.etat.online_game = False
                        self.playing = False
                        self.network.close_socket()
                        self.network.destroyNetwork()
                        return
                    elif event.key == pg.K_b:
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        listRect = []
                        for row in self.gameController.getMap():
                            for tile in row:
                                (x,y) = tile.getRenderCoord()
                                offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                                a, b = offset
                                if -64 <= (a + self.camera.scroll.x) <= 1920 and -64 <= (b + self.camera.scroll.y)  <= 1080:
                                    listRect.append((tile,(a + self.camera.scroll.x, b + self.camera.scroll.y)))
                        for coord in listRect:
                            if coord[1][0] < mouse_x < coord[1][0] + 64 and coord[1][1] + 8 < mouse_y < coord[1][1] + 24:
                                if coord[0].territoire == self.network.this_client.color:
                                    if self.gameController.nbBobPut > 0:
                                        self.gameController.add_bob_online(coord[0])
                                        self.gameController.nbBobPut -= 1   
                    elif event.key == pg.K_n:
                        mouse_x, mouse_y = pg.mouse.get_pos()
                        listRect = []
                        for row in self.gameController.getMap():
                          for tile in row:
                            (x,y) = tile.getRenderCoord()
                            offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                            a, b = offset
                            if -64 <= (a + self.camera.scroll.x) <= 1920 and -64 <= (b + self.camera.scroll.y)  <= 1080:
                                listRect.append((tile,(a + self.camera.scroll.x, b + self.camera.scroll.y)))
                          for coord in listRect:
                            if coord[1][0] < mouse_x < coord[1][0] + 64 and coord[1][1] + 8 < mouse_y < coord[1][1] + 24:
                              self.gameController.add_food_online(coord[0])

            self.gameController.tick_online_update()
            sum = 0
            for bob in self.gameController.listBobs:
                sum += 1
            print(sum)
            self.network.listen()

            screen.fill((255, 255, 255))
            surface = pg.Surface((setting.getSurfaceWidth(), setting.getSurfaceHeight())).convert_alpha()
            surface.fill((255, 255, 255))
            self.drawModifiable_Online(surface, self.camera)
            screen.blit(surface, (self.camera.scroll.x, self.camera.scroll.y))    
            self.drawIndex_Online(screen)
            pg.display.flip()

        if not self.etat.playing:
            return
    """ 
            

    def drawModifiable_Online(self, surface, camera):
        net = Network.getNetworkInstance()
        textureImg = loadGrassImage()
        flowImg = loadFlowerImage()
        darkGrass = loadGrassImage()
        darkFlower = loadGrassImage()
        brightGrass = loadGrassBrightImage()
        brightFlower = loadFlowerBrightImage()
        for row in self.gameController.getMap(): # x is a list of a double list Map
            for tile in row: # tile is an object in list
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
                        if tile.flower:
                            surface.blit(brightFlower, offset)
                        else:
                            surface.blit(brightGrass, offset)
                        tile.hover = False
                else: pass

        greenLeft = loadGreenLeft()
        blueLeft = loadBlueLeft()
        purpleLeft = loadPurpleLeft()
        redLeft = loadRedLeft()

        for bob in self.gameController.listBobs:
            if (bob not in self.gameController.diedQueue) and (bob not in self.gameController.newBornQueue):
                    nbInteval = len(bob.getPreviousTiles()) - 1
                    if ( self.gameController.renderTick < setting.getFps()/2):
                        if nbInteval == 0:
                            (destX, destY) = bob.getCurrentTile().getRenderCoord()
                            (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                            finish = (desX, desY + setting.getTileSize())
                            a,b = finish
                            if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                                bar_width = int((bob.energy / bob.energyMax) * 50)
                                pg.draw.rect(surface, (255, 0, 0), (finish[0], finish[1] - 5, bar_width, 5))
                                if bob.color == 1:
                                    surface.blit(redLeft, finish)
                                elif bob.color == 2:
                                    surface.blit(blueLeft, finish)
                                elif bob.color == 3:
                                    surface.blit(greenLeft, finish)
                                elif bob.color == 4:
                                    surface.blit(purpleLeft, finish)
                            else: pass
                        else:
                            for i in range( nbInteval):
                                if ( i*setting.getFps()) / (nbInteval * 2) <= self.gameController.renderTick < (i+1)*setting.getFps() / (nbInteval * 2):
                                    (x, y) = bob.getPreviousTiles()[i].getRenderCoord()
                                    (X, Y) = (x + surface.get_width()/2 , y - (50 - setting.getTileSize() ) )
                                    (destX, destY) = bob.getPreviousTiles()[i+1].getRenderCoord()
                                    (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                                    pos = (X + (desX - X) * (self.gameController.renderTick - (i*setting.getFps())/(2 * nbInteval)) * (2 * nbInteval) / setting.getFps() , Y + (desY - Y) * (self.gameController.renderTick - (i*setting.getFps())/(2 * nbInteval) ) * (2 * nbInteval) / setting.getFps()  + setting.getTileSize()  )
                                    a,b = pos
                                    if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                                        bar_width = int((bob.energy / bob.energyMax) * 50)
                                        pg.draw.rect(surface, (255, 0, 0), (pos[0], pos[1] - 5, bar_width, 5))
                                        if bob.color == 1:
                                            surface.blit(redLeft, pos)
                                        elif bob.color == 2:
                                            surface.blit(blueLeft, pos)
                                        elif bob.color == 3:
                                            surface.blit(greenLeft, pos)
                                        elif bob.color == 4:
                                            surface.blit(purpleLeft, pos)
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
                            if bob.color == 1:
                                surface.blit(redLeft, finish)
                            elif bob.color == 2:
                                surface.blit(blueLeft, finish)
                            elif bob.color == 3:
                                surface.blit(greenLeft, finish)
                            elif bob.color == 4:
                                surface.blit(purpleLeft, finish)
                        else: pass
        for bob in self.gameController.diedQueue:
            (x, y) = bob.getPreviousTile().getRenderCoord()
            (X, Y) = (x + surface.get_width()/2 , y - (50 - setting.getTileSize() ) )
            position = (X, Y)
            (destX, destY) = bob.getCurrentTile().getRenderCoord()
            (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
            start = (X + (desX - X) * (2 *self.gameController.renderTick/setting.getFps()), Y + (desY - Y) * (2* self.gameController.renderTick/setting.getFps()) + setting.getTileSize())
            finish = (desX, desY + setting.getTileSize())
            a , b = finish
            if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                if (self.gameController.renderTick < setting.getFps()/2):
                    if bob.color == 1:
                        surface.blit(redLeft, start)
                    elif bob.color == 2:
                        surface.blit(blueLeft, start)
                    elif bob.color == 3:
                        surface.blit(greenLeft, start)
                    elif bob.color == 4:
                        surface.blit(purpleLeft, start)
               
            else: pass

        for bob in self.gameController.newBornQueue:
            if bob not in self.gameController.diedQueue:
                (destX, destY) = bob.getCurrentTile().getRenderCoord()
                (desX, desY) = (destX + surface.get_width()/2 , destY - ( + 50 - setting.getTileSize() ) )
                finish = (desX, desY + setting.getTileSize())
                a,b = finish
                if -64 <= (a  + camera.scroll.x) <= 1920 and -64 <= (b  + camera.scroll.y)  <= 1080:
                    if self.gameController.renderTick < setting.getFps()/2:
                        pass
                else: pass
        
        foodTexture = loadFoodImage()
        for food in self.gameController.getFoodTiles():
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
        if net.this_client.color == 1:
            surface.blit(redLeft, (mouse_x - redLeft.get_width()//2 - camera.scroll.x, mouse_y - redLeft.get_height()//2 - camera.scroll.y))
        if net.this_client.color == 2:
            surface.blit(blueLeft, (mouse_x - blueLeft.get_width()//2 - camera.scroll.x, mouse_y - blueLeft.get_height()//2 - camera.scroll.y))
        if net.this_client.color == 3:
            surface.blit(greenLeft, (mouse_x - greenLeft.get_width()//2 - camera.scroll.x, mouse_y - greenLeft.get_height()//2 - camera.scroll.y))
        if net.this_client.color == 4:
            surface.blit(purpleLeft, (mouse_x - purpleLeft.get_width()//2 - camera.scroll.x, mouse_y - purpleLeft.get_height()//2 - camera.scroll.y))
        
        """ """
        listRect = []
        for row in self.gameController.getMap():
            for tile in row:
                territoire_true = net.this_client.color == tile.territoire
                (x,y) = tile.getRenderCoord()
                offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                a, b = offset
                if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                    if territoire_true: 
                        listRect.append((tile,(a + camera.scroll.x, b + camera.scroll.y)))
        
        for coord in listRect:
            if coord[1][0] <= mouse_x <= coord[1][0] + 64 and coord[1][1] + 8 <= mouse_y <= coord[1][1] + 24:
                coord[0].hover = True
                nb = 1
                
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
    """ """
    def drawIndex_Online(self, surface):
        
        net=Network.getNetworkInstance()
        connected_players = [player for player in net.clientList.values() if player is not None]
        greenLeft = loadGreenLeft()
        blueLeft = loadBlueLeft()
        purpleLeft = loadPurpleLeft()
        redLeft = loadRedLeft()

        half_width = surface.get_width()       
        top_right_rect = pg.Rect(half_width, 0, half_width, surface.get_height() )
        
        y_position = top_right_rect.top
        
        draw_text(
            surface,
            'Tick: {}'.format(round(self.gameController.getTick())),
            25,
            (0,0,0),
            (top_right_rect.left, y_position)
        )
        y_position += 20  

        draw_text(
            surface,
            'Nb de bob: {}'.format(self.gameController.getNbBobs()),
            25,
            (0,0,0),
            (top_right_rect.left, y_position)
        )
        y_position += 20

        draw_text(
            surface,
            'Nb de bob engendré: {}'.format(self.gameController.getNbBobsSpawned()),
            25,
            (0,0,0),
            (top_right_rect.left, y_position)
        )
        y_position += 20
        draw_text(
            surface,
            'Nb joueurs: {}'.format(len(connected_players)),
            25,
            (0,0,0),
        
            (top_right_rect.left, y_position)
        )
        if net.clientList["Red"] and net.clientList["Red"].ready:
            surface.blit(redLeft, (50, 1200))
        if net.clientList["Blue"] and net.clientList["Blue"].ready:
            surface.blit(blueLeft, (50, 1200))
        if net.clientList["Green"] and net.clientList["Green"].ready:
            surface.blit(greenLeft, (50, 1200))
        if net.clientList["Purple"] and net.clientList["Purple"].ready:
            surface.blit(purpleLeft, (50, 1200))
    
    @staticmethod
    def getInstance(screen, clock):
        if Game_Online.instance == None:
            Game_Online.instance = Game_Online(screen, clock)
        return Game_Online.instance