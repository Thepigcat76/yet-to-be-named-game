import pygame
import random
from registries.colors import *
from registries.json_lang import *
import registries.animations
import registries.elements
import registries.buttons
import registries.gui
import registries.item

#pygame initialization
pygame.init()
gameStarted = False
class Player:
    #Initial Player attribute assignment
    def __init__(currentImage):
        Player.defaultSpeed = 11
        Player.jumpsound = pygame.mixer.Sound("src/main/assets/sounds/jump.wav")
        Player.jumpsound.set_volume(0.25)
        Player.deathSound = pygame.mixer.Sound("src\main/assets\sounds\death.mp3")
        Player.deathSound.set_volume(0.25)
        Player.hurtSound = pygame.mixer.Sound("src\main/assets\sounds\hurt.mp3")
        Player.hurtSound.set_volume(0.25)
        Player.speed = Player.defaultSpeed
        Player.jumpvar = 16 #Important for jumping calculation
        Player.facingRight = True
        Player.facingLeft = False
        Player.standing = True
        Player.jumping = False
        Player.walking = False
        Player.collidingLeft = False
        Player.collidingRight = False
        Player.rect = pygame.Rect((800, 562), (100, 200)) # Create the players hitbox
        Player.animationFrameUpdate = 1
        Player.debuggingMode = False
        Player.visible = True
        Player.movementLocked = False
        Player.locked = False
        Player.debuggingMenu = False
        Player.flying = 0
        Player.colliding = 0
        Player.defaultHealth = 6 #most of the time it's 6
        Player.health = Player.defaultHealth
        Player.dead = False
        Player.playedDeathSound = False
        Player.chatOpen = False
        Player.world = None
        Player.langCounter = 0
        Player.languageList = ["en_us", "de_de"]
        Player.language = Player.languageList[Player.langCounter]

    def keybinds(self,camera_pos):
        global player_x
        global player_y
        self.doorhandling = 0 #Door mechanics
        player_x = self.rect.x #Camera following the player
        player_y = self.rect.y

        player_x, player_y = camera_pos #Assign variables to the camera position

        key = pygame.key.get_pressed() #Receive keyboard input
        if key[pygame.K_UP] and Player.jumpvar == 16 and Player.visible == True and Player.movementLocked == False and Player.locked == False: #Jumping
            Player.jumpvar = -14.3
        elif key[pygame.K_SPACE] and Player.jumpvar == 16 and Player.visible == True and Player.movementLocked == False and Player.locked == False: #Alternative jumping keybind
            Player.jumpvar = -14.3

        if Player.jumpvar == -14.3: #Play jump sound when the player jumps
            pygame.mixer.Sound.play(Player.jumpsound)

        if Player.jumpvar <= 15: #Jumping movement
            n = -1
            if Player.jumpvar < 0:
                n = 1
            Player.rect.y -= (Player.jumpvar**2)*0.17*n
            Player.jumping = True
            Player.jumpvar += 1
        else:
            Player.jumpvar = 16
            Player.jumping = False

        if key[pygame.K_RIGHT] and Player.visible == True and Player.collidingRight == True and Player.movementLocked == False and Player.movementLocked == False and Player.locked == False: #Player walking
            Player.facingLeft = False
            Player.facingRight = True
        elif key[pygame.K_RIGHT] and Player.collidingRight == False and Player.movementLocked == False and Player.locked == False:
            Player.facingLeft = False
            Player.facingRight = True
            Player.standing = False
            self.rect.x += Player.speed
        else:
            Player.standing = True
            Player.walking = False

        if key[pygame.K_LEFT] and Player.visible == True and Player.collidingLeft == True and Player.movementLocked == False and Player.locked == False: #Player walking
            Player.facingLeft = True
            Player.facingRight = False
        elif key[pygame.K_LEFT] and Player.collidingLeft == False and Player.movementLocked == False and Player.collidingLeft == False and Player.locked == False:
            Player.facingLeft = True
            Player.facingRight = False
            Player.standing = False
            self.rect.x -= Player.speed
        else:
            Player.standing = True
            Player.walking = False

        if Player.collidingLeft == True:
            print("colliding left")
        if Player.collidingRight == True:
            print("colliding right")

        #Debug mode to help developers
        if key[pygame.K_d] and Player.debuggingMode == False and Player.locked == False:
            pygame.time.wait(200)
            Player.debuggingMode = True
        elif key[pygame.K_d] and Player.debuggingMode == True and Player.debuggingMenu == False and Player.locked == False:
            pygame.time.wait(200)
            Player.debuggingMode = False
        
        #The chat    
        if key[pygame.K_c] and Player.chatOpen == False and Player.debuggingMenu == False:
            pygame.time.wait(200)
            Player.chatOpen = True
            
        elif key[pygame.K_ESCAPE] and Player.chatOpen == True:
            pygame.time.wait(200)
            Player.chatOpen = False

        if key[pygame.K_0] and Player.debuggingMode == True and Player.debuggingMenu == False and Player.locked == False:
            pygame.time.wait(200)
            Player.movementLocked = True
            Player.debuggingMenu = True
        elif key[pygame.K_0] or key[pygame.K_ESCAPE] and Player.debuggingMode == True and Player.locked == False:
            pygame.time.wait(200)
            Player.movementLocked = False
            Player.debuggingMenu = False

        if key[pygame.K_DOWN] and Player.visible == True and Player.debuggingMode == True and Player.movementLocked == False and Player.flying == 1 and Player.locked == False:
            Player.standing = False
            Player.facingLeft = False
            Player.facingRight = True
            self.rect.y += Player.speed 
        else:
            Player.standing = True
            Player.walking = False
            
        if key[pygame.K_u] and Player.visible == True and Player.debuggingMode == True and Player.movementLocked == False and Player.flying == 1 and Player.locked == False:
            Player.standing = False
            Player.facingLeft = False
            Player.facingRight = True
            self.rect.y -= Player.speed 
        else:
            Player.standing = True
            Player.walking = False
    
    #End of debugging mode functions

        if key[pygame.K_LEFT] and Player.visible == True and Player.movementLocked == False and Player.locked == False or key[pygame.K_RIGHT] and Player.visible == True  and Player.movementLocked == False and Player.locked == False: #Walking animations
            Player.walking = True

        if Player.walking == True and key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT] and Player.locked == False: #Sprinting
            Player.speed = 18
            Player.countUp = 2
        else:
            Player.speed = Player.defaultSpeed

        return (-self.rect.x + 680, -self.rect.y + 350) # Return new player position

    def renderDebugMenu(self, language):
        toggleCollisionsText = registries.gui.registerFont(30, translatableComponent("text.debug_menu.collide", language), BLACK, 15, 30)
        toggleAdvMoveText = registries.gui.registerFont(30, translatableComponent("text.debug_menu.fly", language), BLACK, 15, 130)
        if Player.debuggingMenu == True:
            debugMenu.draw(screen, BLUISH_GRAY)
            if toggleAdvMove.drawToggle(debugMenu.window, 320, 250, 75, 100):
                if Player.flying > 1:
                    Player.flying = 0
                Player.flying += 1
                if Player.flying == 1:
                    print("selected")
                if Player.flying == 2:
                    print("not selected") 
            toggleAdvMoveText.drawFont(debugMenu.window)
            if damage.draw(debugMenu.window, 225, 350, -35, -10, 75, 100, translatableComponent("button.debug_menu.damage", language), BLACK, "joystixmonospaceregular"):
                print("button pressed")
                if Player.health > 0:
                    Player.health -= 1
                    if Player.health > 0.5:
                        pygame.mixer.Sound.play(Player.hurtSound)
            if heal.draw(debugMenu.window, 225, 450, -60, -10, 75, 100, translatableComponent("button.debug_menu.heal", language), BLACK, "joystixmonospaceregular"):
                print("pressed other button")
                if Player.health < Player.defaultHealth:
                    Player.health += 1
            if toggleCollisions.drawToggle(debugMenu.window, 320, 150, 75, 100):
                if Player.colliding > 1:
                    Player.colliding = 0
                Player.colliding += 1
                if Player.colliding == 1:
                    print("selected")
                if Player.colliding == 2:
                    print("not selecteduwu")
            toggleCollisionsText.drawFont(debugMenu.window)

    def collisions(self):
        #Wall collisions, do not delete!!!
        if Player.rect.x < 500:
            Player.collidingLeft = True
        else:
            Player.collidingLeft = False
        if Player.rect.x > 3780:
            Player.collidingRight = True
        else:
            Player.collidingRight = False

Player()
#Loading element textures
grassElement = registries.elements.registerElement("elements/Environment/blocks/grass_dirt", 3)
dirtElement = registries.elements.registerElement("elements/Environment/blocks/Dirt", 3)
coarseDirtElement = registries.elements.registerElement("elements/Environment/blocks/Coarse_Dirt", 3)
coarseGrassElement = registries.elements.registerElement("elements/Environment/blocks/Coarse_Grass", 3)
cobbleElement = registries.elements.registerElement("elements/Environment/blocks/cobble", 3)
cobbleMossyElement = registries.elements.registerElement("elements/Environment/blocks/cobble_mossy", 3)
waterFluid = registries.elements.registerElement("elements/Environment/fluids/water", 3)
waterWavingFluid = registries.elements.registerElement("elements/Environment/fluids/water_top", 3)
leverOffDeco = registries.elements.registerElement("elements/Environment/decoration/lever_0", 3)
leverOnDeco = registries.elements.registerElement("elements/Environment/decoration/lever_1", 3)
poppyDeco = registries.elements.registerElement("elements/Environment/decoration/poppy", 3)
grassDeco = registries.elements.registerElement("elements/Environment/decoration/grass", 3)
torchLeftDeco = registries.elements.registerElement("elements/Environment/decoration/Torches/Torch(wall=left)", 3)
torchRightDeco = registries.elements.registerElement("elements/Environment/decoration/Torches/Torch(wall=right)", 3)
torchTopDeco = registries.elements.registerElement("elements/Environment/decoration/Torches/Torch(wall=top)", 3)
torchDeco = registries.elements.registerElement("elements/Environment/decoration/Torches/Torch", 3)
chainDeco = registries.elements.registerElement("elements/Environment/decoration/Chain/Chain", 3)
chainPartedDeco = registries.elements.registerElement("elements/Environment/decoration/Chain/Chain(parted)", 3) 
shieldDeco = registries.elements.registerElement("elements/Environment/decoration/Shields/Shield1", 3)
shieldDamagedDeco = registries.elements.registerElement("elements/Environment/decoration/Shields/Shield1(harmed)", 3)
bannerRedDeco = registries.elements.registerElement("elements/Environment/decoration/Banners/Banner1", 3)
bannerBlueDeco = registries.elements.registerElement("elements/Environment/decoration/Banners/Banner2", 3)
bannerYellowDeco = registries.elements.registerElement("elements/Environment/decoration/Banners/Banner3", 3)
doorOpenLargeElement = registries.elements.registerElement("elements/doors/door_1_open", 3)
doorClosedLargeElement = registries.elements.registerElement("elements/doors/door_1_closed", 3)
leverDeco = leverOffDeco

enemy_img = pygame.image.load("src\main/assets/textures\entities\enemies\placeholder_enemy.png")
enemy_img_Scaled=pygame.transform.scale(enemy_img,(enemy_img.get_width( ) * 8, enemy_img.get_width() * 8))

health = pygame.image.load("src\main/assets/textures\elements\gui\player\Heart(full).png")
healthScaled = pygame.transform.scale(health, (70, 70))

halfHealth = pygame.image.load("src\main/assets/textures\elements\gui\player\Heart(half).png")
halfHealthScaled = pygame.transform.scale(halfHealth, (70, 70))

emptyHealth = pygame.image.load("src\main/assets/textures/elements\gui\player\Heart(empty).png")
emptyHealthScaled = pygame.transform.scale(emptyHealth, (70, 70))

npc = pygame.image.load('src/main/assets/textures/entities/npc/npc.png')
npc_scaled = pygame.transform.scale(npc, (npc.get_width() * 8, npc.get_height() * 8))
door_closed = pygame.image.load('src/main/assets/textures/elements/doors/door_1_closed.png')
door_open = pygame.image.load('src/main/assets/textures/elements/doors/door_1_open.png')
door_sprite = door_closed
n = 0

debugMenu = registries.gui.registerGui(70, 100, 300, 400, False)

font = pygame.font.SysFont('joystixmonospaceregular', 25)

def renderText(entry, language):
    debugMenuText = font.render(translatableComponent("text.debug_menu", language), True, DARK_ORANGE)
    debugModeText = font.render(translatableComponent("text.debug_mode", language), True, BLUE)
    texts = [debugMenuText, debugModeText]
    return texts[entry]

debug_menu = pygame.Rect((70, 70), (300, 400))

damage = registries.gui.registerButton("button", 4.0)
heal = registries.gui.registerButton("button", 4.0)

toggleCollisions = registries.gui.registerButton("toggle", 12.0)
toggleAdvMove = registries.gui.registerButton("toggle", 12.0)

screen_width = 1000
screen_height = 800

chatBackground = registries.gui.registerGui(110, 100, 800, 600, False)
chat = registries.gui.registerChat(6, 30, BLACK, BLACK, BLACK, BLACK, 170, 110, 100, 800, 600, 140, 575, 735, 100)
chat.inputLocked = True
exitChat = registries.gui.registerExitButton(85, 80, None)

doorsound = pygame.mixer.Sound('src/main/assets/sounds/Door_Closing.wav')

item = registries.item.registerItem("item", "Item", "Environment\decoration\poppy", 800, 562)

"""game_map = [[0,0,0,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0],
            [0,0,1,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [2,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,2,2,2,2,0,0,2,2,2,2,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,0,0,2,2,2,0,2,2,2,2,2,0,0,2,2,2,2,0]]""" #Lovely css map

tut1_map = [[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,10, 9,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 1, 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 1, 1, 2,00,11,11,11,12,11,11,11,11,00,00,11,11,00,11,11,11,00,12,11,11,00,11,11,11,00,00,11,11,00,00,00,11,00,11,12,00],
            [ 1, 1, 1, 6, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [ 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 1, 1, 6, 6, 6, 1],
            [ 1, 1, 1, 1, 6, 6, 6, 1, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 1],
            [ 1, 1, 1, 1, 1, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 1, 1, 1, 6, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

tut2_map = [[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [16, 3,16, 3, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00, 9,00,00],
            [16,16, 3, 3, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 3,16, 3, 3, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 3, 3,16, 3, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [16, 3, 3,16, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00, 3],
            [ 3,16, 3,16, 3,14,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,15, 3],
            [ 3, 3, 3, 3,16,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00, 8, 3],
            [ 3, 3,16, 3,16,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00, 3],
            [16, 3, 3,16, 3, 3, 3, 3, 3, 3, 3, 3, 3,00,00,00,00, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [16, 3, 3, 3, 3,16,16, 3, 3, 3, 3, 3, 3,00,00,00,00, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [ 3,16, 3, 3,16, 3, 3,16, 3, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [ 3,16, 3,16, 3, 3,16, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [ 3, 3,16, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]

def genWorld(world, map):
    global door_sprite, tileRect2, n
    tile_rects = []
    y = 0
    
    for row in map:
        x = 0
        for tile in row:
            if tile == 1:
                dirtElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 2:
                grassElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 3:
                cobbleElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 4:
                waterFluid.drawElement(world, x, y, Player.debuggingMode)
            if tile == 5:
                waterWavingFluid.drawElement(world, x, y, Player.debuggingMode)
            if tile == 6:
                coarseDirtElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 7:
                coarseGrassElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 8:
                grassElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 9:
                doorClosedLargeElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 10:
                doorClosedLargeElement.drawElement(world, x, y, Player.debuggingMode)
            if tile == 11:
                grassDeco.drawElement(world, x, y, Player.debuggingMode)
            if tile == 12:
                poppyDeco.drawElement(world, x, y, Player.debuggingMode)
            if tile == 13:
                leverOffDeco.drawElement(world, x, y, Player.debuggingMode)
            if tile == 14:
                torchLeftDeco.drawElement(world, x, y, Player.debuggingMode)
            if tile == 15:
                torchRightDeco.drawElement(world, x, y, Player.debuggingMode)
            if tile == 16:
                torchDeco.drawElement(world, x, y, Player.debuggingMode)

            x += 1
        y += 1
    door_sprite = pygame.transform.scale(door_sprite, (int(door_open.get_width() * 5), int(door_open.get_height() * 5)))

    if Player.rect.colliderect(doorClosedLargeElement.rect) and Player.visible == True and pygame.key.get_pressed()[pygame.K_e]:
        door_sprite = door_open
        n += 1
    if n == 40:
        Player.visible = False
        door_sprite = door_closed
        pygame.mixer.Sound.play(doorsound)
    if n == 50:
        n = 0
        Tut2(Player.language)
    if n >= 1 and n <= 70:
        n += 1
        print(n)
    door_sprite = pygame.transform.scale(door_sprite, (int(door_open.get_width() * 5), int(door_open.get_height() * 5)))
        
def health():
        for i in range(Player.defaultHealth):
            if (i % 2) == 0:
                screen.blit(emptyHealthScaled, (10 + i * emptyHealthScaled.get_width()//2, 0))

        for i in range(Player.health):
            if (i % 2) == 0:
                screen.blit(halfHealthScaled, (10 + i * halfHealthScaled.get_width()//2, 0))
            else:
                screen.blit(healthScaled, (10 + i * healthScaled.get_width()//2 - halfHealthScaled.get_width()//2, 0))

def Start(language):
    Player()
    i = 0
    Player.world = None
    startButton = registries.gui.registerButton("button", 6.0)
    optionsButton = registries.gui.registerButton("button", 6.0)
    quitButton = registries.gui.registerButton("button", 6.0)
    clock = pygame.time.Clock()
    while True:
        language = Player.languageList[i]
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and Player.world == None:
                pygame.quit()
                exit()

        startFont = registries.gui.registerFont(40, "YET-BE-NAMED-GAME", DARKER_GRAY, screen.get_width()//2 - 250, screen.get_height()//9)
        screen.fill(BLUISH_GRAY)
        if startButton.drawAnimated(screen, screen.get_width()//2, screen.get_height()//8 * 2.75, registries.animations.startButton, 0, 0, 6, -125, -25, translatableComponent("button.start", language), BLACK, "joystixmonospaceregular"):
            Tut1(language)
        if optionsButton.drawAnimated(screen, screen.get_width()//2, screen.get_height()//2, registries.animations.optionsButton, 48, 48, 6, -125, -25, translatableComponent("button.options", language), BLACK, "joystixmonospaceregular"):
            if i < len(Player.languageList) -1:
                i += 1
            else:
                i = 0
        if quitButton.drawAnimated(screen, screen.get_width()//2, screen.get_height()//8 * 5.25, registries.animations.quitButton, 0, 0, 6, -125, -25, translatableComponent("button.quit", language), BLACK, "joystixmonospaceregular"):
            pygame.quit()
            exit()
            
        if key[pygame.K_RETURN] and Player.world == None:
            pygame.quit()
            exit()
            
        print(language)

        startFont.drawFont(screen)
        #print(str(screen.get_width()) + str(screen.get_height()))
        pygame.display.flip()
        clock.tick(1000)
        
def commandEvent(event, language):
            if chat.userInput.lower() == "/world tut2" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not Player.world == "tut2" and Player.debuggingMode == True:
                chat.userInput = ""
                chat.linesLoaded[0] = translatableComponent("command.teleport.tut2", language)
                chat.x = chat.markerDefaultPos
                Tut2(language)
                
            if chat.userInput.lower() == "/world tut1" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not Player.world == "tut1" and Player.debuggingMode == True:
                chat.userInput = ""
                chat.linesLoaded[0] = translatableComponent("command.teleport.tut1", language)
                chat.x = chat.markerDefaultPos
                Tut1(language)
    

def Tut1(language):
    world = pygame.Surface((8000,8000)) # Create Map
    player = Player() # Initialize Player Class
    camera_pos = (0, 0) #camera starting position

    #values for animation calculation
    idleValue = 0
    walkingValue = 0
    Player.world = "tut1" 
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if chat.userInput.lower() == "/lang de_de" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                chat.userInput = ""
                chat.x = chat.markerDefaultPos
                language = Player.languageList[1]
                chat.linesLoaded[0] = translatableComponent("command.lang", language) + language
            
            if chat.userInput.lower() == "/lang en_us" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                chat.userInput = ""
                chat.x = chat.markerDefaultPos
                language = Player.languageList[0]
                chat.linesLoaded[0] = translatableComponent("command.lang", language) + language
            commandEvent(event, language)
            chat.event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and Player.chatOpen == False and Player.debuggingMenu == False:
                Start(language)

        #idle animation calculation
        if idleValue >= len(registries.animations.idle_sprite):
            idleValue = 0

        #loading the idle animation
        Player.currentSprite = registries.animations.idle_sprite[idleValue]
        
        if walkingValue >= len(registries.animations.walking_sprite):
            walkingValue = 0
        
        #Player movement
        camera_pos = player.keybinds(camera_pos) 

        #Movement animation rendering
        if Player.walking == True:
            Player.currentSprite = registries.animations.walking_sprite[walkingValue]
        if Player.facingLeft == True:
            Player.currentSprite = pygame.transform.flip(Player.currentSprite, True, False)

        #Render background
        world.fill(AQUA)

        #Fill the background outside of the map
        screen.fill(AQUA)

        genWorld(world, tut1_map)

        #blitng to the world

        if Player.visible == True:
            Player.currentSprite = pygame.transform.scale(Player.currentSprite, (32 * 8, 32 * 8))
            # Drawing the player to the screen
            world.blit(Player.currentSprite,(player.rect.x - 75, player.rect.y -50))
            if Player.debuggingMode == True:
                # Drawing the hitbox to the screen
                pygame.draw.rect(world, (0, 255, 0), Player.rect, 4)

        #Render the player
        player.collisions()

        #Render the map to the screen
        screen.blit(world, (player_x, player_y))

        if Player.debuggingMode == True:
            screen.blit(renderText(0, language), (440, 90))
            
        screen.blit(renderText(1, language), (440, 30))

        #Rendering the debug menu
        player.renderDebugMenu(language)
        
        health()
        
        if Player.health > Player.defaultHealth:
            Player.health = Player.defaultHealth
            
        if Player.health <= 0 and Player.defaultHealth != 0:
            Player.dead = True
        else:
            Player.dead = False
            
        if Player.dead == True:
            Player.movementLocked = True
        else:
            Player.movementLocked = False
            
        if Player.dead == True and Player.playedDeathSound == False:
            pygame.mixer.Sound.play(Player.deathSound)
            Player.playedDeathSound = True

        elif Player.dead == False:
            Player.playedDeathSound = False

        #Idle animations
        if Player.standing == True:
            idleValue += 1
        if Player.walking == True:
            walkingValue += Player.animationFrameUpdate
        
        item.drawItem(world)
            
        #print(str(Player.rect.x) + ", " + str(Player.rect.y))
        if Player.chatOpen == True:
            chatBackground.draw(screen, "default")
            chat.drawChat(screen)
            chat.inputLocked = False
            Player.locked = True
            if exitChat.draw(screen):
                Player.chatOpen = False
        else:
            chat.inputLocked = True
            Player.locked = False

        print(Player.rect.x)

        clock.tick(400)
        pygame.display.flip()
        
def Tut2(language):
    world = pygame.Surface((8000,8000)) # Create Map
    player = Player() # Initialize Player Class
    camera_pos = (0, 0) #camera starting position

    #values for animation calculation
    idleValue = 0
    walkingValue = 0
    
    Player.rect.y = 850
    Player.world = "tut2"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if chat.userInput.lower() == "/lang de_de" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                chat.userInput = ""
                chat.x = chat.markerDefaultPos
                language = Player.languageList[1]
                chat.linesLoaded[0] = translatableComponent("command.lang", language) + language

            if chat.userInput.lower() == "/lang en_us" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                chat.userInput = ""
                chat.x = chat.markerDefaultPos
                language = Player.languageList[0]
                chat.linesLoaded[0] = translatableComponent("command.lang", language) + language
            commandEvent(event, language)
            chat.event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and Player.chatOpen == False and Player.debuggingMenu == False:
                Start(language)
        
        #idle animation calculation
        if idleValue >= len(registries.animations.idle_sprite):
            idleValue = 0

        #loading the idle animation
        Player.currentSprite = registries.animations.idle_sprite[idleValue]
        
        if walkingValue >= len(registries.animations.walking_sprite):
            walkingValue = 0
        
        #Player movement
        camera_pos = player.keybinds(camera_pos) 

        #Movement animation rendering
        if Player.walking == True:
            Player.currentSprite = registries.animations.walking_sprite[walkingValue]
        if Player.facingLeft == True:
            Player.currentSprite = pygame.transform.flip(Player.currentSprite, True, False)
            
        screen.fill(DARK_GRAY)
        world.fill(DARK_GRAY)
            
        genWorld(world, tut2_map)

        if Player.visible == True:
            Player.currentSprite = pygame.transform.scale(Player.currentSprite, (32 * 8, 32 * 8))
            # Drawing the player to the screen
            world.blit(Player.currentSprite,(player.rect.x - 75, player.rect.y-50))
            if Player.debuggingMode == True:
                # Drawing the hitbox to the screen
                pygame.draw.rect(world, (0, 255, 0), Player.rect, 4)

        #Render the player
        
        player.collisions()

        #Render the map to the screen
        screen.blit(world, (player_x, player_y))

        if Player.debuggingMode == True:
            screen.blit(renderText(0, language), (440, 90))
            
        screen.blit(renderText(1, language), (440, 30))

        #Rendering the debug menu
        player.renderDebugMenu(language)	
        
        #print(str(Player.rect.x) + ", " + str(Player.rect.y)) Player coordinates
        #print(str(tileRect.x) + ", " + str(tileRect.y)) World generator last generation coordinate
        
        health()
        
        if Player.health > Player.defaultHealth:
            Player.health = Player.defaultHealth
            
        if Player.health <= 0 and Player.defaultHealth != 0:
            Player.dead = True
        else:
            Player.dead = False
            
        if Player.dead == True:
            Player.movementLocked = True
        else:
            Player.movementLocked = False
            
        if Player.dead == True and Player.playedDeathSound == False:
            pygame.mixer.Sound.play(Player.deathSound)
            Player.playedDeathSound = True

        elif Player.dead == False:
            Player.playedDeathSound = False

        #Idle animations
        if Player.standing == True:
            idleValue += 1
        if Player.walking == True:
            walkingValue += Player.animationFrameUpdate
        
        item.drawItem(world)
            
        #print(str(Player.rect.x) + ", " + str(Player.rect.y))
        if Player.chatOpen == True:
            chatBackground.draw(screen, "default")
            chat.drawChat(screen)
            chat.inputLocked = False
            Player.locked = True
            if exitChat.draw(screen):
                Player.chatOpen = False
        else:
            chat.inputLocked = True
            Player.locked = False

        print(language)

        clock.tick(400)
        pygame.display.flip()

if __name__ in "__main__":
    Player()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("CameraView")
    clock = pygame.time.Clock()
    Tut1(Player.language)