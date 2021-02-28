import pygame, math, random, time
from pygame.locals import *


pygame.init()


bg = (10, 10, 10)
black = (0, 0, 0)


bg_menu = (10, 10, 70) #(255, 175, 0)
ctext = (220, 220, 220)
ctextbg = (0, 80, 150)


ww = 800 # window size
wh = 600

window = pygame.display.set_mode((ww, wh))#, FULLSCREEN)
pygame.display.set_caption("Don't hit the asteroids!!!")

pygame.mouse.set_visible(0)
window.fill(bg)

fps = 60            # high values can cause unstable game speed, glitches


difficulty = 1 # 0 = Hard, 1 = Normal, 2 = Easy
diff_bgs   = ( (200, 0, 0), (180, 180, 0), (0, 200, 0) )    # text color for difficulty
diff_str   = ("Hard", "Normal",  "Easy")
diff_spawn = ( 1*fps, 1.5*fps, 2*fps) # seconds * framerate = frames


# text fonts
text_title = pygame.font.SysFont(None, 125)
text_subt  = pygame.font.SysFont(None, 75)
text_subt2 = pygame.font.SysFont(None, 25)


player_img = pygame.image.load("data/player_1.png")


# Startposition player
player_x = ww / 2
player_y = wh / 2

player = pygame.Rect(player_x, player_y, player_img.get_rect().width, player_img.get_rect().height)
player_radius = player.width/2
p_pos = [player.left, player.top] # I use it for more accurate (diagonal) player movement

pygame.mixer.music.load("data/noise.mp3")


# importing game images
asteroid_1 = pygame.image.load("data/asteroid_1.png")
asteroid_2 = pygame.image.load("data/asteroid_2.png")
asteroid_3 = pygame.image.load("data/asteroid_3.png")

asteroid_radius = asteroid_1.get_rect().width/2
w_aster = asteroid_radius * 2
h_aster = w_aster  #asteroid_1.get_rect().height

explosion = pygame.image.load("data/explosion.png")


# Main menu texts
title = text_title.render("aVoid", True, ctext)


subt1 = text_subt.render("Press [Space] to start.", True, ctext, ctextbg)
subt2 = text_subt.render("Press [Esc] to exit game.", True, ctext, ctextbg)

subt4 = text_subt2.render("Use arrow keys to change.", True, ctext)
subt5 = text_subt.render("Difficulty:", True, ctext)
subt6 = text_subt2.render("Press [F1] and [F2] to change Fullscreen", True, ctext)


########################################################################################################################################################


game = 1
while game == 1:

    #### Start config
# asteroids
    bilder_asteroids = [asteroid_1, asteroid_2, asteroid_3]
    asteroids = []
    angle_asteroids = []

    time_counter = 0            # measures time needed to spawn a new asteroid

# player
    angle_player = 0
    pr_player = False

    player_rot = 0
    turnrate = 300 /fps         # degree per frame

    mvsp = 210/fps #3.5         # Movespeed (pixel per frame) 210/60 = 3.5
    mvsp_asteroids = 240/fps    # 

    health = 1

# general
    clock = pygame.time.Clock()
    time_count = 0   # measuring time while playing for solution

    x = 1
    x2 = 1
    end = 0
    
    # Main Menu-loop
    while x2 == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                x = 0
                x2 = 0
                game = 0
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    x = 0
                    x2 = 0
                    game = 0

                if event.key == K_F1:
                    window = pygame.display.set_mode((ww, wh), FULLSCREEN)
                if event.key == K_F2:
                    window = pygame.display.set_mode((ww, wh))

                if event.key == K_SPACE:
                    x2 = 0

                if event.key == K_DOWN:
                    # up to 2
                    difficulty += (difficulty < 2) # True == 1          
                    
                if event.key == K_UP:
                    # down to 0
                    difficulty -= (difficulty > 0)


        diff_bg   = diff_bgs[difficulty]
        diff_text = diff_str[difficulty]
        spawn_count = diff_spawn[difficulty]

        window.fill(bg_menu)
        window.blit(title, (100, 50))

        mvsp_asteroids = (300 - difficulty*30) / fps
        health = difficulty + 1

        subt3 = text_subt.render(diff_text, True, ctext, diff_bg) # the only changing text line
        
        window.blit(subt1, (100, 325))
        window.blit(subt2, (100, 400))
        window.blit(subt3, (500, 100))
        window.blit(subt4, (500, 210))
        window.blit(subt5, (500, 10))#(325, 100))
        window.blit(subt6, (100, 550) )

        pygame.draw.polygon(window, ctext, ((500, 90), (525, 65), (550, 90)))
        pygame.draw.polygon(window, ctext, ((500, 167), (525, 192), (550, 167)))

        pygame.display.update()


    # in-GAME-loop

    while x == 1:
        time_count += 1

        angle_player += player_rot

    # Movement of the player
        if pr_player == True: 

            b = math.cos(math.radians(angle_player)) * mvsp # Berechnet die Laenge der am angle anliegenden Kathete.
            a = math.sin(math.radians(angle_player)) * mvsp # Brechnet die Laenge der des angles gegenueberliegenden Seite.

            p_pos[1] += b
            p_pos[0] += a
            

        player.left = p_pos[0]
        player.top  = p_pos[1]

    # player input
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                x = 0
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    x = 0
                if event.key == K_UP or event.key == K_w:
                    pr_player = True

                if event.key == K_LEFT or event.key == K_a:
                    player_rot += turnrate

                if event.key == K_RIGHT or event.key == K_d:
                    player_rot -= turnrate


            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    pr_player = False
                    
                if event.key == K_LEFT or event.key == K_a:
                    player_rot -= turnrate
                    
                if event.key == K_RIGHT or event.key == K_d:
                    player_rot += turnrate


    # Movement of the asteroids ######################################################

        for i in range(len(asteroids)):
                        
            if asteroids[i].top  <= 0 or asteroids[i].bottom >= wh:
                angle_asteroids[i] = 360 - angle_asteroids[i]


            elif asteroids[i].left <= 0 or asteroids[i].right >= ww:
                angle_asteroids[i] = 180 - angle_asteroids[i]


            b = math.cos(math.radians(angle_asteroids[i])) * mvsp_asteroids
            a = math.sin(math.radians(angle_asteroids[i])) * mvsp_asteroids
                
            asteroids[i].left += b
            asteroids[i].top += a

        
    # starts filling the surface
        window.fill(bg)

        # defines center of new rotated player image/rect
        player_rect = player_img.get_rect().center
        player_neu = pygame.transform.rotate(player_img, angle_player-180)
        player_neu.get_rect().center = player_rect

        player_rect = player_img.get_rect() 
        player_center_neu = player_neu.get_rect().center
        player_center_diff = (player.center[0]-player_center_neu[0], player.center[1]-player_center_neu[1])    

        for i in range(len(asteroids)):
            window.blit(bilder_asteroids[i], asteroids[i])


        window.blit(player_neu, player_center_diff)

        time_counter += 1

    
    # spawns a new asteroid
        if time_counter >= spawn_count:

            edges = ["x", "y"] 
            sedge = edges[random.randint(0, 1)] # select an edge (top-bottom or left-right edge) -> "x" or "y"

            if sedge == "x":
                spawnx = random.randint(0, ww - w_aster)
                edgex = random.randint(0, 1) * (ww - w_aster - 20) + 10 # -20 +10 to move the asteroid 10 px away from the edge ( +10 OR (-20+10) = -10)

                asteroids.append(pygame.Rect(spawnx, edgex, w_aster, h_aster))

            if sedge == "y":
                spawny = random.randint(0, wh - h_aster)
                edgey = random.randint(0, 1) * (wh - h_aster - 20) + 10

                asteroids.append(pygame.Rect(spawny, edgey, w_aster, h_aster))

            
            bilder_asteroids.append(bilder_asteroids[random.randint(0,2)])
            angle_asteroids.append(random.randint(0, 360))
  
            time_counter = 0


    # Collision (needs a list of indices to delete asteroid list items)
        del_list = []
        for i, ast in enumerate(asteroids):

            dist = ( (ast.center[0]-player.center[0])**2 + (ast.center[1]-player.center[1])**2 ) ** (1/2)  # circle collision is more accurate for rotating objects
            if dist < (player_radius + asteroid_radius):
                health -= 1
                del_list.append(i)

        
        del_list.reverse()
        
        for i in del_list:          # removes the items from the right to the left to avoid removing raised items
            del asteroids[i]
            del bilder_asteroids[i]
            del angle_asteroids[i]
            

    # player explodes
        if health <= 0:            
            window.blit(explosion, (player.left-explosion.get_rect().width/2+12, player.top-explosion.get_rect().height/2+12))
            pygame.display.update()
            pygame.mixer.music.play()
            time.sleep(1.5)
            
            x = 0
            end = 1
            p_pos = [ww/2 - player.width/2, wh/2 - player.height/2]
            player.left, player.top = p_pos

    # switch player position when colliding with screen edge
        p_pos[0] += (player.left <= 0)*ww - (player.right >= ww)*ww
        p_pos[1]  += (player.top  <= 0)*wh - (player.bottom >= wh)*wh




    # showing health points
        txt_hp = text_subt2.render("Shield:          x {}".format(health-1), True, ctext)

        window.blit(txt_hp, (10, wh-20))
        #window.blit(shield_img, (80, wh-28))
        pygame.draw.circle(window, (120, 180, 180), (90,wh-15), 14,2)

        if health > 1:
            pygame.draw.circle(window, (120, 180, 180), player.center, 20, 3)


        pygame.display.update()
        clock.tick(fps)

        
    # Game over Screen:
    if end == 1:
        waiting = True
        x = 1

        basicFont = pygame.font.SysFont(None, 100)#150)
        text = basicFont.render("You hit an asteroid. :-(", True, ctext)
        text_time = text_subt.render("survived: " + str(round(time_count/fps, 2)) + " seconds", True, ctext)
        text_Esc = text_subt.render("Press any key to continue.", True, ctext)

        while x == 1:
            window.fill(bg_menu)#(160, 120, 80))

            window.blit(text, (50, 100))
            window.blit(text_time, (75, 300))
            window.blit(text_Esc, (75, 500))
            pygame.display.update()


            if waiting == True: # avoid direct change of the screen, so that the player can see his time result 
                time.sleep(1.25)
                waiting = False

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    x = 0


#################################################################################################################

pygame.quit()
print("Goodbye :-)")


#
