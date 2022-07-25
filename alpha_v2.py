#!/usr/bin/env python

## NOTES TO SELF + TO DO #####
# - Rooms to the sides (alpha v3)
# - 3 Power-ups (alpha v4)
# - Basic minimap (alpha v5)
# - Monsters (alpha final)
# - Title and game over screens
# - Art and music (v1.0)
# - Adjustable window size (v1.1)

######### Modules ################
import pygame, sys, random, math
pygame.init() # Initiate pygame


######### Window ######################################
class Window:
    def __init__(self):
        self.x = 960 # This is full HD  1920p / 2
        self.y = 540 # but cut in half  1080p / 2
Window = Window()

window = pygame.display.set_mode((Window.x, Window.y)) # The actual window
pygame.display.set_caption("Movement alpha_v2") # Window name here


######### Color ##########################
def random_color(): # Returns random RGB val as a tuple
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

class Color: 
    def __init__(self):
        self.darkishBlue = (16, 128, 192) #1080C0
        self.rainBlue = (0, 64, 255) #0040FF
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.cloudWhite = (238, 238, 238)
Color = Color()

### Time ####################
fps = 60
clock = pygame.time.Clock()

######### Ball class ##############
class Ball:
    def __init__(self):
        self.x = int(Window.x / 2) # X and Y positions
        self.y = int(Window.y / 2) 
        self.Vx = 0 # Velocities
        self.Vy = 0
        self.termVelX = 8 # Terminal (horizontal) velocity
        self.Ax = 2 # Horizontal acceleration
        self.Adx = -1 # Horizontal deceleration
        self.Ay = -15 # Jump acceleration
        self.termVelY = 20 # Terminal (vertical) velocity
        
        self.canGoL = True # For colission
        self.canGoR = True #
        self.canGoU = True #
        self.canGoD  = True #
        
        self.radius = 25
        self.color = (255, 0, 0) # Holy shit it's Redball
        
        self.g = 1 # Gravity
        self.inair = False
        self.doDJump = False # Toggles Double-jumping (currently unused)
        self.airSlowDown = 0.75 # Slows down Ball if airborne
        self.onPlatform = True
        
        self.collisionTol = 20 # Collision tolerance
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                  self.radius * 2, self.radius * 2)
        
        self.l = False # Holds Button values
        self.r = False # 
        self.u = False #
Ball = Ball()

######### Platforms #######################################
geometry =[ [(100, 100, 100), (300, 490, 100, 50),  ],
            [(200, 200, 200), (100, 100, 100, 100)  ],
            [(33, 33, 33),    (50, 300, 30, 20)     ],
            [(64, 64, 64),    (250, 250, 20, 20)    ],
            [(214, 33, 121),  (315, 112, 30, 30)    ],
            [(255, 255, 255), (50, 490, 50, 50)     ],
            [Color.rainBlue, (500, 400, 100, 50)    ]
          ]

###########################################################
######### Main game loop ##################################
while True:
    
    # Window BG ###############
    window.fill(Color.darkishBlue)
    
    ######## Quit  ########################################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # For close window button
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # For ESC
            pygame.quit()
            exit()
    
    ### Returns the state of the button linked to direction #########
        if event.type == pygame.KEYDOWN: # Is it pressed?
            if event.key == pygame.K_LEFT:
                Ball.l = True
        
            if event.key == pygame.K_RIGHT:
                Ball.r = True
       
            if event.key == pygame.K_UP:
                Ball.u = True
        
        if event.type == pygame.KEYUP: # Is it released?
            if event.key == pygame.K_LEFT:
                Ball.l = False
             
            if event.key == pygame.K_RIGHT:
                Ball.r = False
                
            if event.key == pygame.K_UP:
                Ball.u = False
    

 ### Movement ######################################
    # Limits ball to the screen #######################
    if Ball.x < Ball.radius: # To the left
        Ball.Vx *= 0
        Ball.x = Ball.radius
    elif Ball.x > Window.x - Ball.radius: # To the right
        Ball.Vx *= 0
        Ball.x = Window.x - Ball.radius

    if Ball.y > Window.y - Ball.radius: # Down
        Ball.Vy = 0
        Ball.y = Window.y - Ball.radius
        Ball.inair = False # Lets ball jump if it's on the floor
        
        
    # Now it's time to get funky
    if Ball.r == True: # To the right now
        Ball.Vx += Ball.Ax
    if Ball.l == True: # To the left
        Ball.Vx -= Ball.Ax
    # Take it back now y'all
    
    if Ball.inair == False and Ball.u or Ball.onPlatform and Ball.u: # One hop this time,
        Ball.Vy += Ball.Ay                                           # One hop this time
        Ball.inair = True
        Ball.onPlatform = False
    
    if Ball.l == False and Ball.Vx < 0: # Slide to the left
        Ball.Vx -= Ball.Adx
    if Ball.r == False and Ball.Vx > 0:  # Slide to the right
        Ball.Vx += Ball.Adx
    
    if Ball.Vx > Ball.termVelX:  # Right foot.
        Ball.Vx = Ball.termVelX  
    if Ball.Vx < -Ball.termVelX: # Two stomps
        Ball.Vx = -Ball.termVelX 
    if Ball.Vy > Ball.termVelY:  # Left foot.
        Ball.Vy = Ball.termVelY  
    if Ball.Vy < -Ball.termVelY: # Two stomps
        Ball.Vy = -Ball.termVelY

    
    if Ball.inair or Ball.onPlatform == False: # Criss cross,
        Ball.Vy += Ball.g                      # Criss cross (gravity)
    # Cha cha real smooth
    
    ### Execute the movement and render ##################################
    ### Collision #####
    
    Ball.hitbox = pygame.Rect(Ball.x - Ball.radius, Ball.y - Ball.radius,
                              Ball.radius * 2, Ball.radius * 2)
    for x in range(len(geometry)):
        cola, colb, colc, cold = geometry[x][1]
        rectangle = pygame.Rect(cola, colb, colc, cold)
        
        if Ball.hitbox.colliderect(rectangle):
            if abs(rectangle.top - Ball.hitbox.bottom) < Ball.collisionTol:
                Ball.y = rectangle.top - Ball.radius + 1
                if Ball.Vy > 0:
                    Ball.Vy *= 0
                if Ball.u:
                    Ball.Vy += Ball.Ay
                
            if abs(rectangle.bottom - Ball.hitbox.top) < Ball.collisionTol:
                Ball.y = rectangle.bottom + Ball.radius
                if Ball.Vy < 0:
                    Ball.Vy *= 0
            
            if abs(rectangle.right - Ball.hitbox.left) < Ball.collisionTol:
                Ball.x = rectangle.right + Ball.radius
                if Ball.Vx < 0:
                    Ball.Vx *= 0
            
            if abs(rectangle.left - Ball.hitbox.right) < Ball.collisionTol:
                Ball.x = rectangle.left - Ball.radius
                if Ball.Vx > 0:
                    Ball.Vx *= 0
        else:
            Ball.onPlatform = False
    
    Ball.x += Ball.Vx
    Ball.y += Ball.Vy
    
    pygame.draw.circle(window, Ball.color, (Ball.x, Ball.y), Ball.radius)
    
    for x in range(len(geometry)):
        pygame.draw.rect(window, geometry[x][0], geometry[x][1])
                       
    ######## Update Game screen ##
    pygame.display.flip()
    clock.tick(fps)
    
####################### END OF CODE ###########################################    