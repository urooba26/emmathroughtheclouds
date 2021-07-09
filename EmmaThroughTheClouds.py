import pygame
from pygame.locals import *
import sys
import random

# Game Font
font = "small_pixel-7.ttf"

# Game Initialization
pygame.init()

# Game Resolution
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(77, 77, 77, 255)
lightskyblue=(135, 206, 250, 255)
lightpink=(219, 112, 147, 255)

# Game Framerate
clock = pygame.time.Clock()         # Object to help track time
FPS=60                              # Frames per second setting

# Text Renderer
def text_format(displaytext, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(displaytext, 0, textColor)
    return newText


# Main Menu
def main_menu():
    click=False
    menu=True
    selected="start"
    while menu:
        mx, my = pygame.mouse.get_pos()
        start_button = pygame.Rect(228.0, 300, 344, 75)
        quit_button = pygame.Rect(339.5, 360, 121, 75)
        # Handle input commands
        for event in pygame.event.get():
            if event.type==pygame.QUIT:                     # To check if cross icon on top right is pressed (quits the game)
                pygame.quit()
                sys.exit()
            #Keyboard Input
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:              # Input for Enter key
                    if selected=="start":
                        EmmaThroughTheClouds().game()
                    if selected=="quit":
                        pygame.quit()
                        sys.exit()
            # Mouse Input
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click=True
            if start_button.collidepoint(mx, my):
                selected="start"
                if click:
                    EmmaThroughTheClouds().game()
            elif quit_button.collidepoint(mx, my):
                selected="quit"
                if click:
                    pygame.quit()
                    sys.exit()
            click=False
        # Main Menu UI
        screen.fill(lightskyblue)
        text_title=text_format("Emma Through The Clouds", font, 70, lightpink)          # text_format calls the text_format() function defined in the beginning
        if selected=="start":
            text_start=text_format("START GAME", font, 75, white)
        else:
            text_start = text_format("START GAME", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)
        # Main Menu Text
        title_rect= text_title.get_rect()           # Creates a rectangular object for the text objects
        start_rect= text_start.get_rect()
        quit_rect= text_quit.get_rect()
        # Draw title, start, quit texts on screen surface
        screen.blit(text_title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        
        pygame.display.update()                                           # Updates portion(surface objects) of the screen
        pygame.display.set_caption("Emma Through The Clouds")             # Displays game's name on title bar

# Reference:  f-prime (Frankie) - DoodleJump game
class EmmaThroughTheClouds:
    # init initializes the attribute, quit() ends the attribute
    def __init__(self):
        # Game Variables
        self.screen = pygame.display.set_mode((screen_width, screen_height))                   # Displays a window of size 800(width)x600(height)
        self.score = 0
        # Platform Variables
        self.fixedplatform = pygame.image.load("assets/fixedplatform.png").convert_alpha()
        self.movingplatform = pygame.image.load("assets/movingplatform.png").convert_alpha()
        self.breakplatform = pygame.image.load("assets/breakplatform.png").convert_alpha()
        self.brokenplatform = pygame.image.load("assets/brokenplatform.png").convert_alpha()
        # Player Variables
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        # Spring Variables
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()

        self.direction = 0                          # Variable for the looking direction of the player(0=RIGHT, 1=LEFT)
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0                            # For Point on y axis(for moving the screen upward)
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0                          # Variable for Horizontal movement of character(on x-axis)

    # Character Movement
    def updatePlayer(self):
        # Character jumping movement
        if self.jump:
            self.playery -= self.jump
            self.jump -= 1
        elif not self.jump:
            self.playery += self.gravity
            self.gravity += 0.5
        # User input to move character
        key = pygame.key.get_pressed()             # Get input for which key is pressed
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1                # Move player towards right
            self.direction = 0                     # Change the direction to 0 (means right)
        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1                # Move player towards left
            self.direction = 1                     # Change the direction to 1 (means left)
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        # Check if character goes outside screen and make it appear on other side
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        # Camera movement as character progresses
        if self.playery - self.cameray <= 200:       # Keeps character on 500 at y-axis
            self.cameray -= 10
        if self.direction==0:                        # Check if player is looking to RIGHT
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))     # Draws image of jumping character looking right if jump
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))       # Draws image of standing character looking right otherwise
        else:                                     # else character is looking to the LEFT
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))      # Draws image of jumping character looking left if jump
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))        # Draws image of standing character looking left otherwise

    # Player interaction with platforms and movement of movingplatform
    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.fixedplatform.get_width() - 10, self.fixedplatform.get_height())                      # Controls the movement of rectangle
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):                                    # Make sure that platforms don't overlap or collide
                if p[2] != 2:                   # Jump only on moving and fixed platforms
                    self.jump = 18
                    self.gravity = 0
                else:
                    p[-1] = 1                   # To display image of brokenplatform when hit breakplatform
            if p[2] == 1:                       # Controls movement of blue platforms
                if p[-1] == 1:
                    p[0] += 5                   # For smooth movement of blue platforms towards right side
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5                   # For smooth movement of blue platforms towards left side
                    if p[0] <= 0:
                        p[-1] = 1

    # Decides which platforms to draw at what position and where to draw springs and jump if player hits a spring
    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:                                                     # To spawn new platforms as player goes upward
                platform = random.randint(0, 950)
                # Which platforms to display 0=fixedplatform, 1=movingplatform, 2=breakplatform
                if platform < 800:
                    platform = 0
                elif platform > 900:
                    platform = 1
                else:
                    platform = 2
                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 75, platform, 0])        # x coordinate, y coordinate, which platform, for breakplatform
                coords = self.platforms[-1]                                                 # Spring coordinate variable
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])                     # Coordinates appended to springs
                self.platforms.pop(0)                                                       # Removes platforms list at 0 index for new platforms
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.fixedplatform, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.movingplatform, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.breakplatform, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.brokenplatform, (p[0], p[1] - self.cameray))
                
        for spring in self.springs:
            if spring[-1]:                                                              # Controls number of springs
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):   # Checks if player collide on spring
                self.jump = 50
                self.cameray -= 50

    # Generates platforms at the start
    def generatePlatforms(self):
        on = 500
        while on > -100:                        # Generate platforms till -50
            x = random.randint(0,700)                       # For position on x-axis
            platform = random.randint(0, 1000)              # Random number for deciding which platform to display
            # Which platforms to display 0=fixedplatform, 1=movingplatform, 2=breakplatform
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    # Main Game Code
    def game(self):
        bg_surface= pygame.image.load("assets/background.png").convert()         # Background surface, covert() helps pygame to run the game at a consistent speed
        bg_x=0                                            # X coordinate for background image
        bg_y=0                                            # Y coordinate for background image
        self.generatePlatforms()
        #Game loop
        while True:
            # Background image
            self.screen.blit(bg_surface,(bg_x,bg_y))                    # Puts bg_surface on screen surface
            clock.tick(FPS)                                             # Limits the runtime speed of the game
            for event in pygame.event.get():
                if event.type == QUIT:                                  # When cross icon on title bar is pressed game will close/quit
                    pygame.quit()
                    sys.exit()
            if self.playery - self.cameray > 600:                       # If player falls to the bottom of screen
                self.game_over()                                        # Calls the game over function
                #Reset All Game Variables after game over
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(text_format(str(self.score), font, 50, gray), (25, 25))        # Display score on top-left corner
            pygame.display.flip()                                                           # Updates entire screen display

    # Game Over Screen
    def game_over(self):
        click=False
        menu=True
        selected="playagain"
        while menu:
            mx, my = pygame.mouse.get_pos()
            playagain_button = pygame.Rect(235.5, 300, 329, 75)
            quit_button = pygame.Rect(339.5, 360, 329, 75)
            # Handle input commands
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Keyboard Input
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        selected="playagain"
                    elif event.key==pygame.K_DOWN:
                        selected="quit"
                    if event.key==pygame.K_RETURN:
                        if selected=="playagain":
                            return
                        if selected=="quit":
                            pygame.quit()
                            sys.exit()
                # Mouse Input
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    click=True
                if playagain_button.collidepoint(mx, my):
                    selected="playagain"
                    if click:
                        return
                elif quit_button.collidepoint(mx, my):
                    selected="quit"
                    if click:
                        pygame.quit()
                        sys.exit()
                click=False
            # Game Over Screen UI
            self.screen.fill(lightskyblue)
            text_gameover=text_format("GAME OVER!", font, 80, lightpink)
            text_score=text_format("Score", font, 65, gray)
            text_displayscore=text_format(str(self.score), font, 65, gray)
            if selected=="playagain":
                text_playagain=text_format("PLAY AGAIN", font, 75, white)
            else:
                text_playagain = text_format("PLAY AGAIN", font, 75, black)
            if selected=="quit":
                text_quit=text_format("QUIT", font, 75, white)
            else:
                text_quit = text_format("QUIT", font, 75, black)
            # Game Over Screen Text
            text_gameover_rect=text_gameover.get_rect()
            playagain_rect=text_playagain.get_rect()
            quit_rect=text_quit.get_rect()
            text_score_rect=text_score.get_rect()
            text_displayscore_rect=text_displayscore.get_rect()
            # Draw game over, score, play again and quit texts on screen surface
            self.screen.blit(text_gameover, (screen_width/2 - (text_gameover_rect[2]/2), 80))
            self.screen.blit(text_score, (screen_width/2.5 - (text_score_rect[2]/2), 180))
            self.screen.blit(text_displayscore, (screen_width-320 - (text_displayscore_rect[2]/2), 180))
            self.screen.blit(text_playagain, (screen_width/2 - (playagain_rect[2]/2), 300))
            self.screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
            pygame.display.update()

# Start of main program
main_menu()
