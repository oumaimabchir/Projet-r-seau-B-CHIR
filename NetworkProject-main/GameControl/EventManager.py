import pygame as pg
import sys
import time
from GameControl.var import *
from menu.menu import Menu
from menu.boutton_Menu import *

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

##################### État du jeu #####################
class EtatJeu:
    instance = None
    def __init__(self):
        self.running = True
        self.playing = False
        self.game_instance = 0
        self.create_room = False
        self.open_menu = True
        self.online_menu = False
        self.waiting_room = False
        self.online_game = False
    def kill(self):
        self.running = False
        self.playing = False
        self.game_instance = 0
        self.open_menu = False
        self.online_menu = False

    @staticmethod
    def getEtatJeuInstance():
        if EtatJeu.instance == None:
            EtatJeu.instance = EtatJeu()
        return EtatJeu.instance 


new_object_dict = { "Bob Energy": setting.getBobSpawnEnergy(), 
                "Bob Mass": setting.getDefaultMass(), 
                "Bob Vision": setting.getDefaultVision(), 
                "Bob Velocity": setting.getDefaultVelocity(),
                "Bob Memory Point": setting.getDefaultMemoryPoint(), 
                "Food Energy": setting.getFoodEnergy() }

allow_mod = False
modding = False
mod_food = False
mod_bob = False

def newObjectMenu (screen, clock , camera ):
    global allow_mod, modding
    modding = True
    while True:
        print("New Object Menu: ", allow_mod, modding)
        if allow_mod == False and modding == False:
            print("Returning")
            return
        elif allow_mod == True and modding == False:
            modifiableMode(screen, clock, camera)
        elif allow_mod == False and modding == True:
            moddingFunc( screen, clock, camera)


def modifiableMode(screen, clock, camera):

    global allow_mod, modding, mod_food, mod_bob, new_object_dict

    while True: 
        clock.tick(30)
        print("Modifiable Mode")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    allow_mod = False
                    modding = True
                    return
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                listRect = []
                for row in gameController.getMap():
                    for tile in row:
                        (x,y) = tile.getRenderCoord()
                        offset = ( x + setting.getSurfaceWidth()//2 , y + setting.getTileSize()  ) 
                        a, b = offset
                        if -64 <= (a + camera.scroll.x) <= 1920 and -64 <= (b + camera.scroll.y)  <= 1080:
                            listRect.append((tile,(a + camera.scroll.x, b + camera.scroll.y)))

                for coord in listRect:
                    if mod_bob:
                        if coord[1][0] <= mouse_x <= coord[1][0] + 64 and coord[1][1] + 8 <= mouse_y <= coord[1][1] + 24:
                            createBob(coord[0])
                    if mod_food:
                        if coord[1][0] <= mouse_x <= coord[1][0] + 64 and coord[1][1] + 8 <= mouse_y <= coord[1][1] + 24:
                            createFood(coord[0])


        gameController.updateRenderTick()
        screen.fill((137, 207, 240))
        surface = pg.Surface((setting.getSurfaceWidth(), setting.getSurfaceHeight())).convert_alpha()
        surface.fill((195, 177, 225))
        drawModifiable(surface, camera)
        screen.blit(surface, (camera.scroll.x, camera.scroll.y))    
        drawIndex ( screen)
        pg.display.flip()

def createFood(tile):
    tile.foodEnergy += new_object_dict["Food Energy"]
    

def createBob(tile):
    global new_object_dict
    bob = Bob()
    bob.setCurrentTile(tile)
    bob.PreviousTiles.append(tile)
    bob.CurrentTile.addBob(bob)
    bob.setEnergy(new_object_dict["Bob Energy"])
    bob.setMass(new_object_dict["Bob Mass"])
    bob.setVision(new_object_dict["Bob Vision"])
    bob.setVelocity(new_object_dict["Bob Velocity"])
    bob.setMemoryPoint(new_object_dict["Bob Memory Point"])
    bob.determineNextTile()
    gameController.getListBobs().append(bob)
    gameController.setNbBobs(gameController.getNbBobs() + 1)
    gameController.setNbBobsSpawned(gameController.getNbBobsSpawned() + 1)

def handle_next_action(next_action, etat):
    if next_action == "nouvelle partie":
        etat.playing = True
        etat.open_menu = False
        etat.game_instance = 0
    #elif next_action == "join game":
        #etat.open_menu = False
        #etat.online_menu = True
    elif next_action == "create multiplayer":
        etat.open_menu = False
        etat.online_menu = True


def show_menu(screen, clock):
    etat = EtatJeu.getEtatJeuInstance()
    menu = Menu(screen, None)  # Assuming 'None' for lanceur; replace with the correct instance if needed

    while etat.open_menu:
        next_action = menu.run()
        handle_next_action(next_action, etat)
        clock.tick(60)  # Limit the frame rate to 60 FPS


def drawIndex( surface):

    draw_text(
        surface,
        'Day: {}'.format(round(gameController.getDay())),
        25,
        (0,0,0),
        (10, 50)
    )  
    
    draw_text(
        surface,
        'Tick: {}'.format(round(gameController.getTick())),
        25,
        (0,0,0),
        (10, 30)
    )  
    
    draw_text(
        surface,
        'Number of bobs: {}'.format(gameController.getNbBobs()) ,
        25,
        (0,0,0),
        (10, 70)
    )
    draw_text(
        surface,
        'Number of bob spawned: {}'.format(gameController.getNbBobsSpawned()) ,
        25,
        (0,0,0),
        (10, 90)
    )


def moddingFunc(screen, clock, camera ):
    global allow_mod, modding, new_object_dict, input_active, input_text, selected_value_index,gameController, mod_food, mod_bob
    input_active = False
    input_text = ""

    back_button_rect = pg.Rect(500, 500, button_width, button_height)
    add_food_button_rect = pg.Rect(20, 100, button_width, button_height)
    add_bob_button_rect = pg.Rect(20, 180, button_width, button_height)

    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    allow_mod = False
                    modding = False
                    return
                elif add_food_button_rect.collidepoint(event.pos):
                    mod_food = True
                    mod_bob = False
                    allow_mod = True
                    modding = False
                    return
                elif add_bob_button_rect.collidepoint(event.pos):
                    mod_food = False
                    mod_bob = True
                    allow_mod = True
                    modding = False
                    return

                for key, value in grid_value_rects.items():
                    if value.collidepoint(event.pos):
                        selected_value_index = key
                        input_active = True
            elif event.type == pg.KEYDOWN:
                if input_active:
                    NewObjectValueEvaluator(event)
        
        gameController.updateRenderTick()
        screen.blit(background_image, (0, 0))
        new = [(key,value) for key, value in new_object_dict.items()]
        new1 = dict(new)
        labels = list(new1.keys())
        values = list(new1.values())
        grid_value_rects.update(draw_transparent_grids(labels[:len(labels)//2], values[:len(values)//2], 400, 300, 50))
        grid_value_rects.update(draw_transparent_grids(labels[len(labels)//2:], values[len(values)//2:], 1300, 300, 50))

        draw_transparent_button("BACK", back_button_rect, 128)
        draw_transparent_button("ADD FOOD", add_food_button_rect, 128)
        draw_transparent_button("ADD BOB", add_bob_button_rect, 128)

        if input_active:
            # Effacer l'ancien texte avec un rectangle blanc
            pg.draw.rect(screen, WHITE, (grid_value_rects[selected_value_index].x, grid_value_rects[selected_value_index].y, 200, 40))
            input_surface = font.render(input_text, True, BLACK)  # Couleur de la police en noir
            input_rect = input_surface.get_rect(center=(grid_value_rects[selected_value_index].centerx, grid_value_rects[selected_value_index].centery))
            # pg.draw.rect(screen, WHITE, (input_rect.x - 5, input_rect.y - 5, input_rect.width + 10, input_rect.height + 10), border_radius=5)  # Couleur de fond du rectangle en blanc
            screen.blit(input_surface, input_rect)

        pg.display.flip()

        
etat = EtatJeu.getEtatJeuInstance()

ip_port_dict = { "IP": "", "PORT": 1961 }


def join_room(screen, clock ):
    global selected_value_index, grid_value_rects, input_text, input_active, ip_port_dict
    input_active = False
    input_text = ""
    back_button_rect = Button_Menu(screen, mid_width, mid_height + (2*GAP), "BACK")
    join_button_rect = Button_Menu(screen, mid_width, mid_height + (GAP), "JOIN")
    etat = EtatJeu.getEtatJeuInstance()
    while etat.online_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
                if back_button_rect.check_button(event):
                    etat.open_menu = True
                    etat.online_menu = False
                    return
                if ip_port_dict["IP"] != "" and ip_port_dict["PORT"] != 0:
                    if join_button_rect.check_button(event):
                        etat.open_menu = False
                        etat.online_menu = False
                        etat.waiting_room = True
                        etat.create_room = False
                        return
                for key, value in grid_value_rects.items():
                    if value.collidepoint(event.pos):
                        selected_value_index = key
                        input_active = True
                        print("input_active")
                        input_text = ""  # Utiliser la valeur actuelle pour l'affichage initial
            
            elif event.type == pg.KEYDOWN:
                if input_active:
                    match selected_value_index:
                        case "IP":
                            if event.key == pg.K_RETURN:
                                if input_text == "":
                                    input_active = False
                                    input_text = ""
                                    selected_value_index = None
                                else:
                                    ip_port_dict["IP"] = input_text
                                    input_active = False
                                    input_text = ""
                                    selected_value_index = None
                            elif event.key == pg.K_BACKSPACE:
                                input_text = input_text[:-1]
                            else:
                                if len(input_text) < 15:
                                    input_text += event.unicode
                        case "PORT":
                            if event.key == pg.K_RETURN:
                                if input_text == "":
                                    input_active = False
                                    input_text = ""
                                    selected_value_index = None
                                else:
                                    ip_port_dict["PORT"] = int(input_text)
                                    input_active = False
                                    input_text = ""
                                    selected_value_index = None
                            elif event.key == pg.K_BACKSPACE:
                                input_text = input_text[:-1]
                            else:
                                if len(input_text) < 5:
                                    if event.unicode.isdigit():
                                        input_text += event.unicode
                                    else:
                                        print("La valeur doit être un entier.")
                                else:
                                    print("La valeur ne doit pas dépasser 5 caractère.")
                    

        screen.blit(background_image2, (0, 0))
        new = [(key,value) for key, value in ip_port_dict.items()]
        new1 = dict(new)
        labels = list(new1.keys())
        values = list(new1.values())

        # Adjust the vertical positions of the grids
        grid_value_rects.update(draw_transparent_grids(labels[:1], values[:1], 400, 300, 50))
        grid_value_rects.update(draw_transparent_grids(labels[1:], values[1:], 400, 400, 50))

        back_button_rect.draw()
        

        if ip_port_dict["IP"] != "" and ip_port_dict["PORT"] != 0:
            join_button_rect.draw()
            

        if selected_value_index is not None:
            pg.draw.rect(screen, WHITE, grid_value_rects[selected_value_index], 2)
        
        if input_active:
            pg.draw.rect(screen, WHITE, (grid_value_rects[selected_value_index].x, grid_value_rects[selected_value_index].y, 200, 40))
            input_surface = font.render(input_text, True, BLACK)
            input_rect = input_surface.get_rect(center=(grid_value_rects[selected_value_index].centerx, grid_value_rects[selected_value_index].centery))
            screen.blit(input_surface, input_rect)

        pg.display.flip()


def waiting_room( screen, clock):
    global selected_value_index, grid_value_rects, input_text, input_active
    input_active = False
    input_text = ""
    etat = EtatJeu.getEtatJeuInstance()
    net = Network.getNetworkInstance()
    back_button_rect = Button_Menu(screen, mid_width, mid_height + (2*GAP), "BACK") # Ajustez les coordonnées ici
    start_button_rect =Button_Menu(screen, mid_width, mid_height + (GAP), "LET'S GO") # Ajustez les coordonnées ici

    green = loadGreenLeft()
    blue = loadBlueLeft()
    purple = loadPurpleLeft()
    red = loadRedLeft()

    greenblack = loadGreenRight()
    blueblack = loadBlueRight()
    purpleblack = loadPurpleRight()
    redblack = loadRedRight()

    net.init_listen()
    if etat.create_room:
        packet = Package(PYMSG_CREATE_ROOM)
        net.send_package(packet)
    else:
        pkg = Package(PYMSG_JOIN_ROOM)
        pkg.packData()
        pkg.pushData(net.pack_ip_port(ip_port_dict["IP"], ip_port_dict["PORT"]))
        net.send_package(pkg)
    time = 0

    while etat.waiting_room:
        net.listen()
        time += 1
        connected_players = [player for player in net.clientList.values() if player is not None]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
                if back_button_rect.check_button(event):
                    print(net.port)
                    net.close_socket()
                    etat.waiting_room = False
                    etat.online_menu = True
                    return
                if start_button_rect.check_button(event) and time >= 5:
                    pkg = Package(PYMSG_GAME_READY)
                    pkg.packData()
                    net.send_package(pkg)
                    net.this_client.readyReq = True


                    
        #timer:

        if net.this_client != None and net.this_client.readyReq:
            ready_for_play = True
            for color, player in net.clientList.items():
                if player is not None and player.ready:
                    if player.ready_rep_pkg == None:
                        ready_for_play = False
                        break
            if ready_for_play:
                net.this_client.readyReq = False
                net.this_client.ready = True
                etat.waiting_room = False
                etat.online_game = True

        # Vérifiez si le nombre de joueurs est suffisant pour jouer
        screen.blit(background_image2, (0, 0))
        back_button_rect.draw()
        
        if time >= 5:
            start_button_rect.draw()
        if net.clientList["Green"]:
            if net.clientList["Green"].ready:
                screen.blit(green, (screen.get_width() // 2 - 100, 300))
            else:
                screen.blit(greenblack, (screen.get_width() // 2 - 100, 300))
        if net.clientList["Blue"]:
            if net.clientList["Blue"].ready:
                screen.blit(blue, (screen.get_width() // 2 - 100, 400))
            else:
                screen.blit(blueblack, (screen.get_width() // 2 - 100, 400))
        if net.clientList["Purple"]:
            if net.clientList["Purple"].ready:
                screen.blit(purple, (screen.get_width() // 2 - 100, 500))
            else:
                screen.blit(purpleblack, (screen.get_width() // 2 - 100, 500))
        if net.clientList["Red"]:
            if net.clientList["Red"].ready:
                screen.blit(red, (screen.get_width() // 2 - 100, 600))
            else:
                screen.blit(redblack, (screen.get_width() // 2 , 400))
        
        pg.display.flip()
        



def NewObjectValueEvaluator(event):
    global selected_value_index, new_object_dict, input_text, input_active
    match selected_value_index:
        case None:
            pass
        case "Food Energy": # Food Energy
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = int(input_text)
                        if not isinstance(new_value, int):
                            # print("La valeur doit être un entier.")
                            input_text = ""
                            input_active = False
                        else:
                            if 0 < new_value <= 2000:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 4:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    else:
                        print("La valeur doit être un entier.")
                else:
                    print("La valeur ne doit pas dépasser 4 caractère.")
        case "Bob Energy": # Bob Spawned Energy
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = int(input_text)
                        if not isinstance(new_value, int):
                            # print("La valeur doit être un entier.")
                            input_text = ""
                            input_active = False
                        else:
                            if 0 < new_value <= 1000:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 4:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    else:
                        print("La valeur doit être un entier.")
                else:
                    print("La valeur ne doit pas dépasser 4 caractère.")
        case "Bob Velocity": # Default velocity
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = float(input_text)
                        if not isinstance(new_value, float):
                            # print("La valeur doit être un entier.")
                            input_text = ""
                            input_active = False
                        else:
                            if 0 < new_value <= 10:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 5:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    elif event.unicode == ".":
                        if "." in input_text:
                            print("La valeur doit être just 1 point.")
                        else:
                            input_text += event.unicode
                    else:
                        print("La valeur doit être un float.")
                else:
                    print("La valeur ne doit pas dépasser 5 caractère.")   
        case "Bob Mass": # Default mass
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = float(input_text)
                        if not isinstance(new_value, float):
                            # print("La valeur doit être un entier.")
                            input_text = ""
                            input_active = False
                        else:
                            if 0 < new_value <= 10:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 5:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    elif event.unicode == ".":
                        if "." in input_text:
                            print("La valeur doit être just 1 point.")
                        else:
                            input_text += event.unicode
                    else:
                        print("La valeur doit être un float.")
                else:
                    print("La valeur ne doit pas dépasser 5 caractère.")   
        case "Bob Vision": 
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = int(input_text)
                        if not isinstance(new_value, int):
                            input_text = ""
                            input_active = False
                        else:
                            if 0 <= new_value <= 10:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 5:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    elif event.unicode == ".":
                        if "." in input_text:
                            print("La valeur doit être just 1 point.")
                        else:
                            input_text += event.unicode
                    else:
                        print("La valeur doit être un float.")
                else:
                    print("La valeur ne doit pas dépasser 5 caractère.")   

        case "Bob Memory Point": # Default Memory point
            if event.key == pg.K_RETURN:
                    if input_text == "":
                            input_active = False
                            input_text = ""
                            selected_value_index = None
                    else:                                
                        new_value = int(input_text)
                        if not isinstance(new_value, int):
                            # print("La valeur doit être un entier.")
                            input_text = ""
                            input_active = False
                        else:
                            if 0 <= new_value <= 10:
                                new_object_dict[selected_value_index] = new_value
                                input_active = False
                                input_text = ""
                                selected_value_index = None
                            else: 
                                input_text = ""
                                input_active = False
            elif event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 5:
                    if event.unicode.isdigit():
                        input_text += event.unicode
                    elif event.unicode == ".":
                        if "." in input_text:
                            print("La valeur doit être just 1 point.")
                        else:
                            input_text += event.unicode
                    else:
                        print("La valeur doit être un float.")
                else:
                    print("La valeur ne doit pas dépasser 5 caractère.")  


def open_network_setting(screen, clock):
    global selected_value_index, grid_value_rects, input_text, input_active

    back_button_rect = Button_Menu(screen, mid_width, mid_height + (2*GAP), 'BACK')
    create_room_button = Button_Menu(screen, mid_width, mid_height + GAP, 'Create ROOM')
    join_room_button = Button_Menu(screen, mid_width, mid_height + (3*GAP), 'JOIN')

    etat = EtatJeu.getEtatJeuInstance()

    while etat.online_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
                if back_button_rect.check_button(event):
                    etat.open_menu = True
                    etat.online_menu = False
                elif create_room_button.check_button(event):
                    etat.open_menu = False
                    etat.online_menu = False
                    etat.waiting_room = True
                    etat.create_room = True
                elif join_room_button.check_button(event):
                    join_room(screen, clock)

        screen.blit(background_image2, (0, 0))  # Draw the background
        create_room_button.draw()  # Draw the create room button
        back_button_rect.draw()
        join_room_button.draw()
        pg.display.flip()
        clock.tick(60)

    return
