import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))        # main floor 
    screen.blit(floor_surface,(floor_x_pos + 288,450))  # duplicate floor to the right

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)                                # chooses 1 out of 3 given options 
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))         # 350 is lil bit to the right margin
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos - 180))   # dist b/w pipes
    return bottom_pipe, top_pipe                                                # returns a rect tuple

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=2    # moves every pipe in the list  

    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]  
    # effectively kills all pipes to the left of -50  
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:            
            screen.blit(pipe_surface,pipe)  # if bottom pipe, cuz only bottom can touch 512
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)  # flips along y axis
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bee_rect.colliderect(pipe):                  # bee touching pipe
            death_sound.play()
            can_score = True                            # reset score flag to True
            return False
    if bee_rect.top <= -50 or bee_rect.bottom >= 450:   # out of bounds
        death_sound.play()
        can_score = True                                # reset score flag to True                              
        return False
    return True                                         # returns flag for collision

def rotate_bee(bee):
    new_bee = pygame.transform.rotozoom(bee,bee_movement * -3,1)
    # syntax pygame.transform.rotozoom(surface,angle,zoom)
    return new_bee

def bee_animation():
    new_bee = bee_frames[bee_index]
    new_bee_rect = new_bee.get_rect(center = (50, bee_rect.centery)) 
    # creates a rect for every frame at it's proper coordinates       
    return new_bee, new_bee_rect
    
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = score_font.render(str(int(score)),False,(255,255,255))   
        # False means anti-aliasing off
        # rbg tuple, given color is white
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = score_font.render(f'Score: {int(score)}',False,(255,255,255))   
        # f string
        score_rect = score_surface.get_rect(center = (144,60))
        screen.blit(score_surface,score_rect)

        high_score_surface = score_font.render(f'High Score: {int(high_score)}',False,(255,255,255))   
        high_score_rect = score_surface.get_rect(center = (120,100))
        screen.blit(high_score_surface,high_score_rect)

def title_display(game_state):
    if game_state == 'game_over':
        title_surface = title_font.render('FlappyBug',False,(255,255,255))   
        title_rect = title_surface.get_rect(center = (145,190))
        screen.blit(title_surface,title_rect)


def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 48 < pipe.centerx < 52 and can_score == True:    # bird passing the pipe condition
                score += 1
                score_sound.play()
                can_score = False       # contingency to prevent duplicate score 
            if pipe.centerx < 0:
                can_score = True        # resets contingency  

# start pygame module
pygame.init()
screen = pygame.display.set_mode((288,512))       # main window res
clock = pygame.time.Clock()                       # for timer
score_font = pygame.font.Font('04B_19.ttf',20)    # Font(style,size)  
title_font = pygame.font.Font('04B_19.ttf',40)

# game variables
gravity = 0.3        # arbitrary gravity value
bee_movement = 0     # the actual value that affects the bee
game_active = True   # main flag variable
score = 0
high_score = 0
can_score = True     # score flag

bg_surface = pygame.image.load('images/background-moon.png').convert()      # background, convert reduces load
bg_surface = pygame.transform.scale(bg_surface, (288,512))                  # rescale bg
floor_surface = pygame.image.load('images/base.png').convert()              # adds floor png
floor_x_pos = 0                                                             # variable

# load images, scale it and convert to alpha to remove bg

bee1 = pygame.transform.scale(pygame.image.load('images/bee1.png'), (60,60)).convert_alpha()
bee2 = pygame.transform.scale(pygame.image.load('images/bee2.png'), (60,60)).convert_alpha()
bee3 = pygame.transform.scale(pygame.image.load('images/bee3.png'), (60,60)).convert_alpha()
bee4 = pygame.transform.scale(pygame.image.load('images/bee3.png'), (60,60)).convert_alpha()
bee5 = pygame.transform.scale(pygame.image.load('images/bee3.png'), (60,60)).convert_alpha()
bee_frames = [bee1,bee2,bee3,bee4,bee5]                 # frames for wing animation
bee_index = 0                                           # frame index
bee_surface = bee_frames[bee_index]                     # frame at index pos to display
bee_rect = bee_surface.get_rect(center = (50,256))      # adds rect to the surface that's the bee frame 
BEEFLAP = pygame.USEREVENT + 1          # variable that senses timer event
pygame.time.set_timer(BEEFLAP,200)      # frame changes every 200ms

pipe_surface = pygame.image.load('images/pipe-green.png')       # pipe png
pipe_list = []                                                  # empty rect list for spawning pipe tuples
SPAWNPIPE = pygame.USEREVENT                                    # variable that senses a timer event  
pygame.time.set_timer(SPAWNPIPE,2000)                           # pipe spwans every 2400ms                                          
pipe_height = [200,300,400]

game_over_surface = pygame.image.load('images/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    # event loop
    for event in pygame.event.get():                                    # senses event
        if event.type == pygame.QUIT:                                   # clicking close button
            pygame.quit()                                               # pygame quits                        
            sys.exit()                                                  # everything quits                            
        if event.type == pygame.KEYDOWN:                                # senses key    
            if event.key == pygame.K_SPACE and game_active:             # senses spacebar and truth of flag
                bee_movement = 0                                        # resets gravity        
                bee_movement -= 6                                       # bee jumps   
                flap_sound.play()     
            if event.key == pygame.K_SPACE and game_active == False:    # senses spacebar and falsehood of flag
                game_active = True
                pipe_list.clear()
                bee_rect.center = (50,256)
                score = 0
                bee_movement = 0                                        # reset and resart
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())                             # extend will unpack the tuple pair of pipes
        if event.type == BEEFLAP:
            if bee_index < 4:
                bee_index += 1
            else:
                bee_index = 0
            bee_surface,bee_rect = bee_animation()
    
    # game loop
    screen.blit(bg_surface,(0,0))   # adds the bg png to the top left

    if game_active:
        # bee
        bee_movement += gravity                     # gravity constantly acts on our bee
        rotated_bee = rotate_bee(bee_surface)
        bee_rect.centery += bee_movement            # centery is the y coor of bee_rect
        screen.blit(rotated_bee,bee_rect)           # blits the bee into its rectangle instead of coor
        game_active = check_collision(pipe_list)    # updates flag

        # pipes
        pipe_list = move_pipes(pipe_list)           
        draw_pipes(pipe_list)                       # moves and draws the pipe every loop
        
        # score
        pipe_score_check()
        score_display('main_game')
    
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        title_display('game_over')

    # floor
    floor_x_pos -= 1                                # moves floor to left every loop
    draw_floor()
    if floor_x_pos <= -288: 
        floor_x_pos = 0                             # resets pipe
    pygame.display.update()                         # updates every change
    clock.tick(60)                                  # frames per sec