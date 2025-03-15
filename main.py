""" Early Bird 

A game similar to Google Chrome's Dino Game, built using the pygame library. Tbe player must collect as many unhatched eggs while dodging the breakfast enemies. 
Made without custom classes. 
Created for ICS3U1 by Neeya H. 
Last Edited June 12, 2024
"""

import pygame
from random import randint
from random import choice 

def display_score():
    """ Calculates and displays the current game score (the duration the player has lasted in the game) and egg score (the amount of eggs the player has collected)
    
    Returns:
        int: the current duration the player has lasted in the game 
    """
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = game_font.render(f"score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(topleft = (650,30))
    egg_score_surf = game_font.render(f"eggs: {egg_score}", False, (64,64,64))
    egg_score_rect = egg_score_surf.get_rect(topleft = (650, 70))
    pygame.draw.rect(screen, (111,196,169), egg_score_rect, 30)
    pygame.draw.rect(screen, (111,196,169), score_rect, 30)
    screen.blit(score_surf,score_rect)
    screen.blit(egg_score_surf, egg_score_rect)
    return current_time # returns as the response so can be used later 

def obstacle_movement(obstacle_list):
    """ Displays obstacle movement across the screen
    
    Argument:
        list: obstacles currently displayed on the screen
    Returns:
        list: obstacles currently remaining on the screen (removes any that have passed the x position of 0)  
    """
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= (5 + (display_score() // 50)) # increases the obstacle's speed as the score increases 

            if obstacle_rect.bottom == GROUND_Y: 
                if obstacle_rect.top < 250: # differentiates between the 2 toasts using their height 
                    screen.blit(burnt_toast_surf,obstacle_rect) 
                else:
                    screen.blit(toast_surf,obstacle_rect) 
            else:
                screen.blit(fried_egg_surf,obstacle_rect) # if obstacle isn't on the ground, display the fried egg

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0] # only keeps obstacles that are currently on the screen
        
        return obstacle_list
    else:
        return []
    
def collectible_movement(collectible_list):
    """ Displays the movement of collectible items across the screen
    
    Argument:
        list: collectbles currently displayed on the screen
    Returns:
        list: collectibles currently remaining on the screen (removes any that have passed the x position of 0)  
    """
    if collectible_list:
        for collectible_rect in collectible_list:
            collectible_rect.x -= (5 + (display_score() // 50)) # increases the speed of the collectible items as the score increases (each speed increase level is in increments of 50)
            if collectible_rect.bottom == 100:
                screen.blit(triple_egg_surf, collectible_rect) # displays a triple egg 
            else:
                screen.blit(egg_surf, collectible_rect) # displays a single unhatched egg 

        collectible_list = [collectible for collectible in collectible_list if collectible.x > 0] # only keeps items that are currently on the screen
        return collectible_list
    else:
        return []

def obstacle_collisions(player, obstacles):
    """ Checks if player collides with any obstacles. If they collide with the fried egg, they lose any collected eggs. Otherwise, if they collide with another obstacle, game over
   
     Argument:
        player (rectangle): rectangle surface of main character
        obstacles (rectangle): rectangle surface of an obstacle
    
    Returns:
        boolean: True (if no collision, or only a fried egg collision. (sets is_playing as True as well))
        boolean: False (if collision, occurs. (Sets is_playing to False))
    """
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                if obstacle_rect.bottom == 260: # Detects the fried egg
                    lose_sound.play()
                    global egg_score
                    egg_score = 0 # Wipes the egg score if the player collides with a fried egg
                    obstacles.remove(obstacle_rect)
                    continue
                obstacle_sound.play() 
                return False 
    return True

def collectible_collisions(player, collectibles):
    """ Checks if player collides with any collectibles. If they collect an egg, their egg_score goes up by 1 point. 

    Argument:
        player (rectangle): rectangle surface of main character
        obstacles (rectangle): rectangle surface of a collectible
    """
    global egg_score
    if collectibles:
        for collectible_rect in collectibles:
            if player.colliderect(collectible_rect):
                if collectible_rect.bottom == 100:
                    egg_score += 3 # Increases the egg_score by 3 the player collects a triple egg
                else:
                    egg_score += 1  # Increases the egg_score by 1 if the player collects a single egg
                collect_sound.play()
                collectibles.remove(collectible_rect) # Removes item once collected
    
def jump():
    """ Makes the player's surface jump. 
    
    Inreases gravity speed, and moves the avatar first upwards, and then downwards, stopping at the floor (GROUND_Y)
    """
    global player_rect, players_gravity_speed    
    # Adjusts the player's vertical location, then blits it 
    players_gravity_speed += 1
    player_rect.y += players_gravity_speed # Adjusts the player's y position given the velocity of gravity 
    if player_rect.bottom > GROUND_Y: # creates a floor
        player_rect.bottom = GROUND_Y
    
def player_animation():
    """ Controls which image surface of the player's avatar to display """
    global player_surf, player_index, player_rect, players_gravity_speed
    if pygame.key.get_pressed()[pygame.K_DOWN]: # Displays the duck surface when the bottom arrow is held 
        player_surf = player_duck 
    elif player_rect.bottom < GROUND_Y: # Displays the jump surface when the player isn't on the floor
        player_surf = player_jump
    else: # Displays the walking animation when the player is on the floor
        player_index += 0.1 
        if player_index >= len(player_frames):
            player_index = 0
        player_surf = player_frames[int(player_index)]
    jump()
    if player_rect.bottom == GROUND_Y:
        player_rect = player_surf.get_rect(bottomleft=(100, GROUND_Y)) # Re-draws the shape of the player-rectangle (duck)

def read_leaderboard():
    """ Opens the leaderboard file and stores all the scores currently listed in a global variable"""
    global leaderboard
    file = open("leaderboard.txt", "a") # opens leaderboard file (creates one if it doesn't exist)
    with open("leaderboard.txt", "r") as file: 
        leaderboard = file.readlines() 
        leaderboard = leaderboard[1:]
        leaderboard = [int(score.strip("")) for score in leaderboard] # Converts each score entered from a string to an integer

def update_leaderboard():
    """ Updates the leaderboard given the player's current game score. Outputs the new leaderboard on the same text file """
    with open("leaderboard.txt", "w") as file:
        if len(leaderboard) < 10 or score > min(leaderboard): # Only adds the player's score if it qualifies for the top 10 
            if len(leaderboard) >= 10:
                leaderboard.remove(min(leaderboard)) 
            leaderboard.append(score)
            leaderboard.sort(reverse = True) # Organizes the leaderbaord from highest to lowest
        file.write("TOP 10 EARLY BIRD SCORES \n")
        for entry in leaderboard:
            file.write(f"{entry} \n")

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Early Bird")
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills the pygame when False
bg_music = pygame.mixer.Sound("audio/bgmusic.mp3") # free-to-use license: https://www.youtube.com/watch?v=-gxjiZHPj54
bg_music.play(loops= -1)

# Game state variables
is_playing = False  # Whether the game is currently being played
GROUND_Y = 300  # The Y-coordinate of the ground level
ground_x = 0  # The X-coordinate of the ground level (variable to implement infinite scrolling)
game_speed = 4 # The speed at which infinite scrolling will occur
JUMP_GRAVITY_START_SPEED = -14  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
start_time = 0 # The start time of each round of the game 
jump_level = 0 # The # of jumps the player has taken (at a given time)
score = 0 # The duration of time the player has lasted during the game 
egg_score = 0 # The number of eggs collected 

# Load level assets
display_font = pygame.font.Font("font/PartyConfetti.ttf", 50) 
game_font = pygame.font.Font("font/PartyConfetti.ttf", 30) 
sky_surf = pygame.image.load("graphics/scenery/sky.png").convert()
ground_surf = pygame.image.load("graphics/scenery/ground.png").convert_alpha()

# Load sound effects (free-to-use license: #https://www.youtube.com/watch?v=8usQCG6WHzE)
collect_sound = pygame.mixer.Sound("audio/collect.mp3")
collect_sound.set_volume(0.5)
lose_sound = pygame.mixer.Sound("audio/lose.mp3")
obstacle_sound = pygame.mixer.Sound("audio/enemy.mp3")
jump_sound = pygame.mixer.Sound("audio/jump.mp3")
jump_sound.set_volume(0.5)

# Load sprite assets:

# Player assets
player_1 = pygame.image.load("graphics/player/run1.png").convert_alpha()
player_2 = pygame.image.load("graphics/player/run2.png").convert_alpha()
player_frames = [player_1, player_2] 
player_index = 0 # manipulated later on to switch between 2 surfaces (creates animation)
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_duck = pygame.image.load("graphics/player/duck.png").convert_alpha()

player_surf = player_frames[player_index]
player_rect = player_surf.get_rect(bottomleft=(100, GROUND_Y))

# Animated obstacle assets
toast_1 = pygame.image.load("graphics/obstacles/toast1.png").convert_alpha()
toast_2 = pygame.image.load("graphics/obstacles/toast2.png").convert_alpha()
toast_frames = [toast_1,toast_2]
toast_index = 0 
toast_surf = toast_frames[toast_index]

burnt_toast_1 = pygame.image.load("graphics/obstacles/burntman1.png").convert_alpha()
burnt_toast_2 = pygame.image.load("graphics/obstacles/burntman2.png").convert_alpha()
burnt_toast_frames = [burnt_toast_1, burnt_toast_2]
burnt_toast_index = 0 
burnt_toast_surf = burnt_toast_frames[burnt_toast_index]

# Static obstacle assets
fried_egg_surf = pygame.image.load("graphics/obstacles/friedegg.png").convert_alpha()

obstacle_rect_list = []

# Static collectible assets
egg_surf = pygame.image.load("graphics/collectibles/egg.png").convert_alpha()
triple_egg_surf = pygame.image.load("graphics/collectibles/tripleegg.png").convert_alpha()
collectible_list = []
                        
# Intro Screen
player_display = pygame.image.load("graphics/startscreen/panic.png").convert_alpha() 
player_display = pygame.transform.scale_by(player_display, 2)
player_display_rect = player_display.get_rect(center=(380,200))
game_name = display_font.render("Early Bird", False,(111,196,169)) 
game_name_rect = game_name.get_rect(center=(390,80))

game_message = display_font.render("Press space to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

# Timers
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1400 + display_score()) # generates a new obstacle at an increasing interval (initially 1400 milliseconds) 

toast_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(toast_animation_timer, 200)

burnt_toast_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(burnt_toast_animation_timer, 250)

egg_timer = pygame.USEREVENT + 4 
pygame.time.set_timer(egg_timer, 2000)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ):
                if player_rect.bottom >= GROUND_Y:
                    jump_level = 0 
                if jump_level < 2:
                    players_gravity_speed = JUMP_GRAVITY_START_SPEED # double jump 
                    jump_level += 1
                    jump_sound.play()

            if event.type == obstacle_timer:
                choice = randint(0,3) # Randomly chooses which obstacle to display
                if choice == 0:
                    obstacle_rect_list.append(toast_surf.get_rect(midbottom = (randint(900,1100), GROUND_Y))) # randomly generates toast position 
                elif choice == 1:
                    obstacle_rect_list.append(burnt_toast_surf.get_rect(midbottom = (randint(900,1100), GROUND_Y))) # randomly generates burnt toast position
                else:
                    if egg_score > 0: # only blits fried egg if the player has collected any unhatched eggs
                        obstacle_rect_list.append(fried_egg_surf.get_rect(midbottom = (randint(900,1100), 260 ))) # randomly generates fried egg position
                
            if event.type == egg_timer: # Displays collectible eggs in randomly generated positions
                choice = randint(0,2) # Random True or False choice
                if choice == 0 and display_score() >= 40:
                    collectible_list.append(triple_egg_surf.get_rect(bottomleft = (randint(900,1100), 100)))
                else:
                    collectible_list.append(egg_surf.get_rect(center = (randint(900,1100), randint(120,260))))

            # Obstacle animation timers
            if event.type == toast_animation_timer: 
                if toast_index == 0:
                    toast_index = 1
                else:
                    toast_index = 0
                toast_surf = toast_frames[toast_index]
            
            if event.type == burnt_toast_animation_timer:
                if burnt_toast_index == 0:
                    burnt_toast_index = 1
                else:
                    burnt_toast_index = 0
                burnt_toast_surf = burnt_toast_frames[burnt_toast_index]

        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                start_time = pygame.time.get_ticks() // 1000
                egg_score = 0 # resets the number of eggs collected 
                read_leaderboard()
                update_leaderboard()
            


    if is_playing:
        ground_x -= game_speed # Adjust scrolling factor
        # Blit the scenery assets
        screen.blit(sky_surf, (-200, 0))
        screen.blit(ground_surf, (ground_x, GROUND_Y))
        screen.blit(ground_surf, (ground_x + 800, GROUND_Y))
        if ground_x <= -800:
            ground_x = 0
        game_speed += 0.0055 # Increases the game_speed each iteration 
        score = display_score()

        player_animation()
        screen.blit(player_surf, player_rect)
   
        # Obstacle Movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Egg Movement
        collectible_list = collectible_movement(collectible_list)

        # Obstacle Collision - checks if the player collides with any obstacles (if yes, game_over)
        is_playing = obstacle_collisions(player_rect, obstacle_rect_list)

        # Collectible Collisions - checks if the player collects any eggs 
        collectible_collisions(player_rect, collectible_list)


    # When game is over, display game over message
    else:
        # Reset the game state variables 
        JUMP_GRAVITY_START_SPEED = -14 # resets the gravity
        players_gravity_speed = 0 # resets the speed at which the player falls
        obstacle_rect_list.clear() #removes the obstacles from the screen
        collectible_list.clear() #removes the eggs from the screen
        player_rect.midbottom = (100, GROUND_Y) #player returns to starting position
        game_speed = 4 # rests the game_speed 

        # Decides which screen to display
        screen.fill((254, 252, 200))
        if score == 0: # Displays the start screen
            screen.blit(player_display, player_display_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            # Displays the game over screen
            crying_chicken = pygame.image.load("graphics/gameover/crying.png").convert_alpha()
            crying_chicken = pygame.transform.scale_by(crying_chicken, 2)
            crying_chicken_rect = crying_chicken.get_rect(center=(325,180))
            dead_egg = pygame.image.load("graphics/gameover/deadegg.png").convert_alpha()
            dead_egg = pygame.transform.scale_by(dead_egg,2)
            dead_egg_rect = dead_egg.get_rect(center=(500,180))
            screen.blit(crying_chicken, crying_chicken_rect)
            screen.blit(dead_egg, dead_egg_rect)
            score_message = display_font.render(f"Your score: {score}", False, (111,196,169))
            score_message_rect = score_message.get_rect(center = (400, 300))
            egg_score_message = display_font.render(f"Eggs collected: {egg_score}", False, (111,196,169))
            egg_score_message_rect = egg_score_message.get_rect(center = (400, 350))
            screen.blit(score_message, score_message_rect)
            screen.blit(egg_score_message, egg_score_message_rect)


    # flip() the display to show the code results on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
            
pygame.quit()


