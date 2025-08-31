import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

game_over = False

# car vars
car_position_x = 0.0  
target_x = 0.0  
movement_speed = 0.05  
car_position_z = -5.0  
target_z = -5.0   
car_position_y = -0.25  
car_velocity_y = 0.0    
gravity = -0.008        
jump_strength = 0.24    
is_jumping = False      
ground_level = -0.25    
jump_start_time = 0.0   
JUMP_DURATION = 3.0  





# Multiplayer mode variables
multiplayer_mode = False

# Player 2 variables
player2_position_x = 0.0
player2_target_x = 0.0
player2_position_z = -5.0
player2_target_z = -5.0
player2_position_y = -0.25
player2_velocity_y = 0.0
player2_is_jumping = False
player2_jump_start_time = 0.0
player2_jump_powers = 0
player2_shoot_powers = 0
player2_score = 0
player2_last_powerup_score = 0
player2_frozen = False
player2_freeze_start_time = 0.0
player2_cheat_mode = False
player2_cheat_start_time = 0.0
player2_last_cheat_use = 0.0
player2_bullets = []

   

# track vars
track_width = 6.0 
track_position = 0.0  
track_speed = 0.15    

# obstacle vars
obstacle1_x = 0.0
obstacle1_z = -15.0
obstacle2_x = 0.0
obstacle2_z = -25.0
obstacle3_x = 0.0  
obstacle3_z = -20.0
obstacle_width = 0.3  
obstacle_height = 0.3  
obstacle_depth = 0.3  
max_jump_height = obstacle_height * 2  

# coin vars
coin1_x = 0.0
coin1_z = -12.0
coin2_x = 0.0 
coin2_z = -18.0
coin_radius = 0.1
score = 0

# track animation vars
initial_track_speed = 0.05 
track_speed = initial_track_speed
min_speed_multiplier = 1.0
max_speed_multiplier = 3.0  

# jump power-up vars
powerup_x = 0.0
powerup_z = -35.0 
powerup_radius = 0.15
jump_powers = 0  
max_jump_powers = 3
last_powerup_score = 0  
powerup_spawn_interval = 40  

# shooting power-up vars
POWERUP_JUMP = 0
POWERUP_SHOOT = 1
current_powerup_type = POWERUP_JUMP
bullets = []  # List to store active bullets

# bullet vars
bullet_speed = 0.03
bullet_size = 0.05
shoot_powers = 0
max_shoot_powers = 3  
shots_per_powerup = 3 

# freeze power-up vars
POWERUP_FREEZE = 2  
car_frozen = False
freeze_start_time = 0.0
freeze_duration = 3.0  

# day/night cycle vars
game_start_time = time.time()
DAY_NIGHT_CYCLE_DURATION = 80.0  
current_time_factor = 0.0  # 0 = day, 1 = night

# cheat mode vars
cheat_mode = False
cheat_duration = 7.0  
cheat_start_time = 0.0
cheat_cooldown = 10.0  
last_cheat_use = 0.0

# difficulty ++ vars
base_obstacle_count = 3
current_obstacle_count = 3
max_obstacles = 6
obstacle4_x = 0.0
obstacle4_z = -30.0
obstacle5_x = 0.0
obstacle5_z = -40.0
obstacle6_x = 0.0
obstacle6_z = -50.0

# blackout vars
screen_dark_mode = False
screen_dark_start_time = 0.0
screen_dark_duration = 1.25  
last_dark_event = 0.0
dark_event_interval = 8.0  

# negative power-up vars
POWERUP_OBSTACLE_BOOST = 3
POWERUP_SCORE_DRAIN = 4
obstacle_boost_active = False
obstacle_boost_start_time = 0.0
obstacle_boost_duration = 8.0  
normal_obstacle_spawn_rate = 30.0  
boosted_obstacle_spawn_rate = 15.0  

trees = []
grass_patches = []

last_update_time = 0
UPDATE_INTERVAL = 1 / 60  



def init_environment():
    global trees, grass_patches
    
    # generate trees
    trees = []
    for i in range(20):
        side = random.choice([-1, 1])  # Left? right?
        tree = {
            'x': side * random.uniform(4.5, 8),  
            'z': random.uniform(-50, 10),
            'height': random.uniform(1, 3),
            'trunk_height': random.uniform(0.5, 1.0)
        }
        trees.append(tree)
    
    # generate grass
    grass_patches = []
    for i in range(30):
        side = random.choice([-1, 1])
        patch = {
            'x': side * random.uniform(4.0, 10),  
            'z': random.uniform(-50, 10),
            'size': random.uniform(0.3, 0.8)
        }
        grass_patches.append(patch)

def update_day_night_cycle():
    global current_time_factor, game_start_time
    
    elapsed_time = time.time() - game_start_time
    cycle_progress = (elapsed_time % DAY_NIGHT_CYCLE_DURATION) / DAY_NIGHT_CYCLE_DURATION
    
    
    current_time_factor = (math.sin(cycle_progress * 2 * math.pi) + 1) / 2

def get_sky_color():
    
    day_color = (0.53, 0.81, 0.98)
    night_color = (0.1, 0.1, 0.2)
    
    r = day_color[0] + (night_color[0] - day_color[0]) * current_time_factor
    g = day_color[1] + (night_color[1] - day_color[1]) * current_time_factor
    b = day_color[2] + (night_color[2] - day_color[2]) * current_time_factor
    
    return (r, g, b)

def get_speed_multiplier():
    global score
    # speed ++
    return min(max_speed_multiplier, min_speed_multiplier + (score / 15) * 0.2)


def init():
    sky_color = get_sky_color()
    glClearColor(sky_color[0], sky_color[1], sky_color[2], 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    init_environment()


def draw_trees():
    """Draw trees using cylinders and spheres"""
    for tree in trees:
        glPushMatrix()
        glTranslatef(tree['x'], 0, tree['z'])
        
        # tree_trunk
        glPushMatrix()
        glColor3f(0.4, 0.2, 0.1)  # brown
        glTranslatef(0, tree['trunk_height']/2, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 0.1, 0.1, tree['trunk_height'], 8, 8)
        glPopMatrix()
        
        # leaves(sphere)
        glPushMatrix()
        if current_time_factor < 0.5:  # day
            glColor3f(0.2, 0.8, 0.2)  # green
        else:  # night
            glColor3f(0.1, 0.4, 0.1)  # dark green
            
        glTranslatef(0, tree['trunk_height'] + tree['height']/2, 0)
        glutSolidSphere(tree['height']/2, 8, 8)
        glPopMatrix()
        
        glPopMatrix()

def draw_grass():
    """Draw grass patches using small cubes"""
    for patch in grass_patches:
        glPushMatrix()
        glTranslatef(patch['x'], -0.4, patch['z'])
        
        if current_time_factor < 0.5:  # day
            glColor3f(0.1, 0.6, 0.1)  # bright green
        else:  # night
            glColor3f(0.05, 0.3, 0.05)  # darker 
            
        glScalef(patch['size'], 0.1, patch['size'])
        glutSolidCube(1.0)
        glPopMatrix()

def draw_ground():
    global track_position
    
    
    if current_time_factor < 0.5:  # day
        glColor3f(0.6, 0.4, 0.2)  # brown
    else:  # night
        glColor3f(0.3, 0.2, 0.1)  # dark brown
   
    # left side
    glPushMatrix()
    glTranslatef(-8.0, -0.55, -10.0)  
    glScalef(80.0, 0.1, 200.0)  
    glutSolidCube(1.0)
    glPopMatrix()
   
    # right side
    glPushMatrix()
    glTranslatef(8.0, -0.55, -10.0)  
    glScalef(80.0, 0.1, 200.0)  
    glutSolidCube(1.0)
    glPopMatrix()
    
    if current_time_factor < 0.5:  # day
        glColor3f(0.5, 0.3, 0.1)  # brown markers
    else:  # night
        glColor3f(0.25, 0.15, 0.05)  # dark brown markers
    
    start_pos = int(track_position * 2) % 4  
    
    for i in range(-30, 10, 4):
        z_pos = (i - start_pos - 10.0) % 60 - 30
        glPushMatrix()
        glTranslatef(-4.0, -0.50, -z_pos)  
        glScalef(0.5, 0.05, 0.5)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(4.0, -0.50, -z_pos)  
        glScalef(0.5, 0.05, 0.5)
        glutSolidCube(1.0)
        glPopMatrix()

def draw_track():
    global track_position
    
    if current_time_factor < 0.5:  # day
        glColor3f(0.5, 0.5, 0.5)  # gray
    else:  # night
        glColor3f(0.3, 0.3, 0.3)  # dark gray
   
    glPushMatrix()
    glTranslatef(0.0, -0.5, -100.0)  
    glScalef(6.0, 0.10, 200.0)  
    glutSolidCube(1.0)  
    glPopMatrix()
   
    glColor3f(1.0, 1.0, 1.0)  # white lanes
   
    start_pos = int(track_position) % 2 
    
    
    for lane in range(-2, 3): # 5 dividers, 6 internal lanes, 2 edge lanes
        for i in range(-30, 10, 2):
            z_pos = (i - start_pos - 10.0) % 60 - 30
            glPushMatrix()
            glTranslatef(lane * 1.0, -0.45, z_pos)  # 1.0 unit spacing between lanes
            glScalef(0.05, 0.02, 1.0)  
            glutSolidCube(1.0)
            glPopMatrix()


def draw_stars():
    """Draw stars during night time"""
    if current_time_factor > 0.3:  # show stars if getting dark
        star_brightness = (current_time_factor - 0.3) / 0.7
        glColor3f(star_brightness, star_brightness, star_brightness)
        
        
        star_positions = [
            (-15, 8, -20), (10, 9, -25), (-8, 7, -30), (12, 8, -15),
            (-20, 6, -35), (5, 10, -40), (-12, 9, -18), (18, 7, -28),
            (-5, 8, -45), (8, 6, -22), (-18, 10, -32), (15, 9, -38)
        ]
        
        glPointSize(3)
        glBegin(GL_POINTS)
        for x, y, z in star_positions:
            glVertex3f(x, y, z)
        glEnd()

def check_game_over():
    global car_position_x, game_over
    if abs(car_position_x) > (track_width/2 - 0.25): 
        game_over = True

def draw_game_over():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 0.0, 0.0)  
    glRasterPos2f(350, 300)
    for c in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(300, 250)
    for c in "Press R to Restart":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def update_car_physics():
    global car_position_y, car_velocity_y, is_jumping, jump_start_time
    
    if is_jumping:
        current_time = time.time()
        time_in_air = current_time - jump_start_time
        
        if time_in_air < JUMP_DURATION:
            progress = time_in_air / JUMP_DURATION
            height_progress = 4 * progress * (1 - progress)
            car_position_y = ground_level + (max_jump_height * height_progress)
        else:
            car_position_y = ground_level
            car_velocity_y = 0.0
            is_jumping = False

def perform_jump():
    global jump_powers, is_jumping, jump_start_time
    
    if jump_powers > 0 and not is_jumping:
        jump_powers -= 1
        is_jumping = True
        jump_start_time = time.time()

def update_player2_physics():
    global player2_position_y, player2_velocity_y, player2_is_jumping, player2_jump_start_time
    
    if player2_is_jumping:
        current_time = time.time()
        time_in_air = current_time - player2_jump_start_time
        
        if time_in_air < JUMP_DURATION:
            progress = time_in_air / JUMP_DURATION
            height_progress = 4 * progress * (1 - progress)
            player2_position_y = ground_level + (max_jump_height * height_progress)
        else:
            player2_position_y = ground_level
            player2_velocity_y = 0.0
            player2_is_jumping = False

def perform_player2_jump():
    global player2_jump_powers, player2_is_jumping, player2_jump_start_time
    
    if player2_jump_powers > 0 and not player2_is_jumping:
        player2_jump_powers -= 1
        player2_is_jumping = True
        player2_jump_start_time = time.time()

def draw_car():
    global car_position_x, car_position_z, car_position_y, jump_powers, cheat_mode, car_frozen
    
    quadric = gluNewQuadric()
    
    glPushMatrix()
    glTranslatef(car_position_x, car_position_y, car_position_z)
    glScalef(0.3, 0.3, 0.3)  
    
    # car clr
    if car_frozen:
        glColor3f(0.7, 0.7, 1.0)  # light blue->frozen
    elif cheat_mode:
        glColor4f(0.5, 0.5, 1.0, 0.7)  # transparent blue->cheat
    elif jump_powers > 0:
        glColor3f(1.0, 0.5, 0.0)  # orange->jump
    else:
        glColor3f(1.0, 0.0, 0.0)  # red->normal
        
    glPushMatrix()
    glScalef(1.0, 0.5, 2.0)  
    glutSolidCube(1.0)
    glPopMatrix()
    
    # car cab
    glColor3f(0.8, 0.8, 1.0)  
    glPushMatrix()
    glTranslatef(0.0, 0.4, 0.0)  
    glScalef(0.8, 0.4, 1.0)  
    glutSolidCube(1.0)
    glPopMatrix()
    
    # wheels
    glColor3f(0.2, 0.2, 0.2)  
    
    positions = [(-0.6, -0.3, 0.7), (0.6, -0.3, 0.7), 
                (-0.6, -0.3, -0.7), (0.6, -0.3, -0.7)]
    
    for x, y, z in positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.2, 12, 12)
        glPopMatrix()
    
    # tailights
    glColor3f(1.0, 1.0, 0.0)
    for x in [-0.3, 0.3]:
        glPushMatrix()
        glTranslatef(x, 0.0, 1.05)
        gluSphere(quadric, 0.1, 8, 8)
        glPopMatrix()
    
    glPopMatrix()

def draw_player2_car():
    global player2_position_x, player2_position_z, player2_position_y, player2_jump_powers, player2_cheat_mode, player2_frozen
    
    if not multiplayer_mode:
        return
        
    quadric = gluNewQuadric()
    
    glPushMatrix()
    glTranslatef(player2_position_x, player2_position_y, player2_position_z)
    glScalef(0.3, 0.3, 0.3)  
    
    # player2 clr
    if player2_frozen:
        glColor3f(0.7, 0.7, 1.0)  # light blue->frozen
    elif player2_cheat_mode:
        glColor4f(0.5, 1.0, 0.5, 0.7)  # transparent green->cheat
    elif player2_jump_powers > 0:
        glColor3f(1.0, 1.0, 0.0)  # yellow->jump
    else:
        glColor3f(0.0, 0.0, 1.0)  # blue->normal
        
    glPushMatrix()
    glScalef(1.0, 0.5, 2.0)  
    glutSolidCube(1.0)
    glPopMatrix()
    
    # player2 cab
    glColor3f(0.8, 1.0, 0.8)  
    glPushMatrix()
    glTranslatef(0.0, 0.4, 0.0)  
    glScalef(0.8, 0.4, 1.0)  
    glutSolidCube(1.0)
    glPopMatrix()
    
    # player2 wheels
    glColor3f(0.2, 0.2, 0.2)  
    
    positions = [(-0.6, -0.3, 0.7), (0.6, -0.3, 0.7), 
                (-0.6, -0.3, -0.7), (0.6, -0.3, -0.7)]
    
    for x, y, z in positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.2, 12, 12)
        glPopMatrix()
    
    # player2 tailights
    glColor3f(1.0, 1.0, 0.0)
    for x in [-0.3, 0.3]:
        glPushMatrix()
        glTranslatef(x, 0.0, 1.05)
        gluSphere(quadric, 0.1, 8, 8)
        glPopMatrix()
    
    glPopMatrix()

def draw_obstacles():
    global obstacle1_x, obstacle1_z, obstacle2_x, obstacle2_z, obstacle3_x, obstacle3_z
    global obstacle4_x, obstacle4_z, obstacle5_x, obstacle5_z, obstacle6_x, obstacle6_z
    global current_obstacle_count
    
    glColor3f(1.0, 0.0, 0.0)  
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    # obstacles ++ if difficulty ++
    if current_obstacle_count >= 4:
        obstacles.append((obstacle4_x, obstacle4_z))
    if current_obstacle_count >= 5:
        obstacles.append((obstacle5_x, obstacle5_z))
    if current_obstacle_count >= 6:
        obstacles.append((obstacle6_x, obstacle6_z))
    
    for x, z in obstacles:
        glPushMatrix()
        glTranslatef(x, -0.3, z)
        glScalef(obstacle_width, obstacle_height, obstacle_depth)
        glutSolidCube(1.0)
        glPopMatrix()


def update_bullets():
    global bullets
    
    # bullet move
    bullets = [bullet for bullet in bullets if bullet['active']]
    
    for bullet in bullets:
        bullet['z'] -= bullet_speed
        # bullets hit horizon /// remove
        if bullet['z'] < -50:
            bullet['active'] = False

def update_player2_bullets():
    global player2_bullets
    
    # bullet move
    player2_bullets = [bullet for bullet in player2_bullets if bullet['active']]
    
    for bullet in player2_bullets:
        bullet['z'] -= bullet_speed
        # bullets hit horizon /// remove
        if bullet['z'] < -50:
            bullet['active'] = False

def draw_bullets():
    global bullets
    
    glColor3f(1.0, 1.0, 0.0)  # yellow bullets
    quadric = gluNewQuadric()
    
    for bullet in bullets:
        if bullet['active']:
            glPushMatrix()
            glTranslatef(bullet['x'], bullet['y'], bullet['z'])
            gluSphere(quadric, bullet_size, 8, 8)
            glPopMatrix()

def draw_player2_bullets():
    global player2_bullets
    
    if not multiplayer_mode:
        return
        
    glColor3f(0.0, 1.0, 1.0)  # cyan bullets(player 2)
    quadric = gluNewQuadric()
    
    for bullet in player2_bullets:
        if bullet['active']:
            glPushMatrix()
            glTranslatef(bullet['x'], bullet['y'], bullet['z'])
            gluSphere(quadric, bullet_size, 8, 8)
            glPopMatrix()

def check_bullet_collision():
    global bullets, obstacle1_x, obstacle1_z, obstacle2_x, obstacle2_z, obstacle3_x, obstacle3_z, score
    global obstacle4_x, obstacle4_z, obstacle5_x, obstacle5_z, obstacle6_x, obstacle6_z
    global current_obstacle_count
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    # obstacles ++ if difficulty ++
    if current_obstacle_count >= 4:
        obstacles.append((obstacle4_x, obstacle4_z))
    if current_obstacle_count >= 5:
        obstacles.append((obstacle5_x, obstacle5_z))
    if current_obstacle_count >= 6:
        obstacles.append((obstacle6_x, obstacle6_z))
    
    for bullet in bullets:
        if bullet['active']:
            for i, (obs_x, obs_z) in enumerate(obstacles):
                if (abs(bullet['x'] - obs_x) < 0.3 and abs(bullet['z'] - obs_z) < 0.3):
                    bullet['active'] = False
                    score += 2  # +2 score if hit
                    
                    # despawn + respawn hit obstacle
                    if i == 0:
                        obstacle1_z = -50.0
                        obstacle1_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 1:
                        obstacle2_z = -50.0
                        obstacle2_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 2:
                        obstacle3_z = -50.0
                        obstacle3_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 3 and current_obstacle_count >= 4:
                        obstacle4_z = -50.0
                        obstacle4_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 4 and current_obstacle_count >= 5:
                        obstacle5_z = -50.0
                        obstacle5_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 5 and current_obstacle_count >= 6:
                        obstacle6_z = -50.0
                        obstacle6_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)

def check_player2_bullet_collision():
    global player2_bullets, obstacle1_x, obstacle1_z, obstacle2_x, obstacle2_z, obstacle3_x, obstacle3_z, player2_score
    global obstacle4_x, obstacle4_z, obstacle5_x, obstacle5_z, obstacle6_x, obstacle6_z
    global current_obstacle_count
    
    if not multiplayer_mode:
        return
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    # obstacles ++ if difficulty ++
    if current_obstacle_count >= 4:
        obstacles.append((obstacle4_x, obstacle4_z))
    if current_obstacle_count >= 5:
        obstacles.append((obstacle5_x, obstacle5_z))
    if current_obstacle_count >= 6:
        obstacles.append((obstacle6_x, obstacle6_z))
    
    for bullet in player2_bullets:
        if bullet['active']:
            for i, (obs_x, obs_z) in enumerate(obstacles):
                if (abs(bullet['x'] - obs_x) < 0.3 and abs(bullet['z'] - obs_z) < 0.3):
                    bullet['active'] = False
                    player2_score += 2  # +2 score if hit
                    
                    # despawn + respawn hit obstacle
                    if i == 0:
                        obstacle1_z = -50.0
                        obstacle1_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 1:
                        obstacle2_z = -50.0
                        obstacle2_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 2:
                        obstacle3_z = -50.0
                        obstacle3_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 3 and current_obstacle_count >= 4:
                        obstacle4_z = -50.0
                        obstacle4_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 4 and current_obstacle_count >= 5:
                        obstacle5_z = -50.0
                        obstacle5_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
                    elif i == 5 and current_obstacle_count >= 6:
                        obstacle6_z = -50.0
                        obstacle6_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)

def update_screen_effects():
    global screen_dark_mode, screen_dark_start_time, last_dark_event, score
    
    current_time = time.time()
    
    # start dark event?
    if (score >= 150 and current_time_factor > 0.5 and  # score >= 150 needed
        not screen_dark_mode and 
        current_time - last_dark_event > dark_event_interval + random.uniform(0, 4)):  # rand(8-12) seconds
        
        screen_dark_mode = True
        screen_dark_start_time = current_time
        last_dark_event = current_time
    
    # end dark event?
    if screen_dark_mode and current_time - screen_dark_start_time > screen_dark_duration:
        screen_dark_mode = False



def check_collision():
    global car_position_x, car_position_z, car_position_y, game_over, cheat_mode, cheat_start_time
    global current_obstacle_count

    if cheat_mode:
        current_time = time.time()
        if current_time - cheat_start_time > cheat_duration:
            cheat_mode = False
        else:
            return  
    
    if car_position_y > ground_level + obstacle_height:
        return
        
    car_width = 0.2
    car_length = 0.6
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    # obstacles ++ if difficulty ++
    if current_obstacle_count >= 4:
        obstacles.append((obstacle4_x, obstacle4_z))
    if current_obstacle_count >= 5:
        obstacles.append((obstacle5_x, obstacle5_z))
    if current_obstacle_count >= 6:
        obstacles.append((obstacle6_x, obstacle6_z))
    
    for obs_x, obs_z in obstacles:
        if (abs(car_position_x - obs_x) < (car_width + obstacle_width/2) and 
            abs(car_position_z - obs_z) < (car_length + obstacle_depth/2)):
            game_over = True

def check_player2_collision():
    global player2_position_x, player2_position_z, player2_position_y, game_over, player2_cheat_mode, player2_cheat_start_time
    global current_obstacle_count
 
    if not multiplayer_mode:
        return
        
    if player2_cheat_mode:
        current_time = time.time()
        if current_time - player2_cheat_start_time > cheat_duration:
            player2_cheat_mode = False
        else:
            return 
    
    if player2_position_y > ground_level + obstacle_height:
        return
        
    car_width = 0.2
    car_length = 0.6
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    # obstacles ++ if difficulty ++
    if current_obstacle_count >= 4:
        obstacles.append((obstacle4_x, obstacle4_z))
    if current_obstacle_count >= 5:
        obstacles.append((obstacle5_x, obstacle5_z))
    if current_obstacle_count >= 6:
        obstacles.append((obstacle6_x, obstacle6_z))
    
    for obs_x, obs_z in obstacles:
        if (abs(player2_position_x - obs_x) < (car_width + obstacle_width/2) and 
            abs(player2_position_z - obs_z) < (car_length + obstacle_depth/2)):
            game_over = True

def specialKeyListener(key, x, y):
    global target_x, target_z, game_over
    
    if not game_over:
        if key == GLUT_KEY_LEFT:
            target_x -= 0.06  
        elif key == GLUT_KEY_RIGHT:
            target_x += 0.06  
        elif key == GLUT_KEY_UP:
            if target_z > -6.5:
                target_z -= 0.06  
        elif key == GLUT_KEY_DOWN:
            if target_z < -3.0:
                target_z += 0.06  
        
        glutPostRedisplay()


def mouseListener(button, state, x, y):

    return


def keyboardListener(key, x, y):
    global powerup_x, powerup_z
    global game_over, car_position_x, target_x, car_position_z, target_z, track_position
    global obstacle1_x, obstacle1_z, obstacle2_x, obstacle2_z, obstacle3_x, obstacle3_z
    global score, track_speed, jump_powers, last_powerup_score, car_position_y, car_velocity_y, is_jumping
    global jump_start_time, game_start_time
    global bullets, current_powerup_type, shoot_powers  
    global cheat_mode, cheat_start_time, last_cheat_use
    global multiplayer_mode, player2_target_x, player2_target_z, player2_bullets, player2_shoot_powers
    global player2_position_x, player2_position_z, player2_position_y, player2_velocity_y, player2_is_jumping
    global player2_jump_start_time, player2_score, player2_jump_powers, player2_last_powerup_score
    global player2_cheat_mode, player2_cheat_start_time, player2_last_cheat_use, player2_frozen, player2_freeze_start_time

    if key == b' ':  # action
        if not game_over:
            # priority = shoot > jump
            if shoot_powers > 0:
                # fire bullet
                new_bullet = {
                    'x': car_position_x,
                    'y': car_position_y,
                    'z': car_position_z - 0.5,
                    'active': True
                }
                bullets.append(new_bullet)
                shoot_powers -= 1
            elif jump_powers > 0:
                perform_jump()
        glutPostRedisplay()

    elif key == b'f' or key == b'F':  # player2 action
        if not game_over and multiplayer_mode:
            # priority = shoot > jump
            if player2_shoot_powers > 0:
                # fire bullet
                new_bullet = {
                    'x': player2_position_x,
                    'y': player2_position_y,
                    'z': player2_position_z - 0.5,
                    'active': True
                }
                player2_bullets.append(new_bullet)
                player2_shoot_powers -= 1
            elif player2_jump_powers > 0:
                perform_player2_jump()
        glutPostRedisplay()

    elif key == b'm' or key == b'M':  # toggle multiplayer 
        multiplayer_mode = not multiplayer_mode
        if multiplayer_mode:
            # initialize player2 pos
            player2_position_x = 1.0  # slightly offset from player1
            player2_target_x = 1.0
            player2_position_z = -5.0
            player2_target_z = -5.0
            player2_position_y = ground_level
            player2_velocity_y = 0.0
            player2_is_jumping = False
            player2_jump_start_time = 0.0
            player2_jump_powers = 2  # initial jumps (for testing)
            player2_shoot_powers = 3  # initial shoot (for testing)
            player2_score = 0
            player2_last_powerup_score = 0
            player2_frozen = False
            player2_freeze_start_time = 0.0
            player2_cheat_mode = False
            player2_cheat_start_time = 0.0
            player2_last_cheat_use = 0.0
            player2_bullets.clear()
            
            # player1 as well
            if jump_powers == 0:
                jump_powers = 2
            if shoot_powers == 0:
                shoot_powers = 3
        glutPostRedisplay()

    # WASD player2
    elif key == b'w' or key == b'W':  
        if not game_over and multiplayer_mode:
            if player2_target_z > -6.5:
                player2_target_z -= 0.06
        glutPostRedisplay()

    elif key == b's' or key == b'S':  
        if not game_over and multiplayer_mode:
            if player2_target_z < -3.0:
                player2_target_z += 0.06
        glutPostRedisplay()

    elif key == b'a' or key == b'A':  
        if not game_over and multiplayer_mode:
            player2_target_x -= 0.06
        glutPostRedisplay()

    elif key == b'd' or key == b'D':  
        if not game_over and multiplayer_mode:
            player2_target_x += 0.06
        glutPostRedisplay()

    elif key == b'r' or key == b'R':
        # reset game
        game_over = False
        car_position_x = 0.0
        target_x = 0.0
        car_position_z = -5.0
        target_z = -5.0
        car_position_y = ground_level
        car_velocity_y = 0.0
        is_jumping = False
        jump_start_time = 0.0
        track_position = 0.0
        score = 0  
        track_speed = initial_track_speed  
        jump_powers = 0
        last_powerup_score = 0
        game_start_time = time.time()  
        cheat_mode = False
        last_cheat_use = 0.0
        obstacle_boost_active = False
        obstacle_boost_start_time = 0.0
        
        # also reset Player 2 if multiplayer 
        if multiplayer_mode:
            player2_position_x = 1.0
            player2_target_x = 1.0
            player2_position_z = -5.0
            player2_target_z = -5.0
            player2_position_y = ground_level
            player2_velocity_y = 0.0
            player2_is_jumping = False
            player2_jump_start_time = 0.0
            player2_jump_powers = 0
            player2_shoot_powers = 0
            player2_score = 0
            player2_last_powerup_score = 0
            player2_frozen = False
            player2_freeze_start_time = 0.0
            player2_cheat_mode = False
            player2_cheat_start_time = 0.0
            player2_last_cheat_use = 0.0
            player2_bullets.clear()
        
        # reset obstacles
        obstacle1_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
        obstacle1_z = -15.0
        obstacle2_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
        obstacle2_z = -25.0
        obstacle3_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
        obstacle3_z = -20.0
        
        # reset powerup
        powerup_x = (random.random() * 2 - 1) * (track_width/2 - powerup_radius)
        powerup_z = -35.0
        
        shoot_powers = 0
        current_powerup_type = POWERUP_JUMP
        bullets.clear()
        
        # reinit environment
        init_environment()
        
        glutPostRedisplay()

    elif key == b'c' or key == b'C':
        if not game_over and not cheat_mode:  
            current_time = time.time()
            if current_time - last_cheat_use >= cheat_cooldown:
                cheat_mode = True
                cheat_start_time = current_time
                last_cheat_use = current_time
                
                # cheat player2 if multiplayer
                if multiplayer_mode:
                    player2_cheat_mode = True
                    player2_cheat_start_time = current_time
                    player2_last_cheat_use = current_time
                
        glutPostRedisplay()

def showScreen():
    update_day_night_cycle()
    sky_color = get_sky_color()
    glClearColor(sky_color[0], sky_color[1], sky_color[2], 1.0)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    gluLookAt(0.0, 2.0, 2.0,   
              0.0, 0.0, -15.0, 
              0.0, 1.0, 0.0)    
   
    draw_stars()
    draw_trees()
    draw_grass()
    draw_ground()
    draw_track()
    draw_obstacles()
    draw_coins()  
    draw_powerup() 
    draw_car()
    draw_player2_car()
    draw_bullets()
    draw_player2_bullets()
    
    # darkening 
    if screen_dark_mode:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.98)  # opaque black
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(800, 0)
        glVertex2f(800, 600)
        glVertex2f(0, 600)
        glEnd()
        glDisable(GL_BLEND)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    if game_over:
        draw_game_over()
    
    draw_score()  
    
    glutSwapBuffers()   

def check_collision():
    global car_position_x, car_position_z, car_position_y, game_over, cheat_mode, cheat_start_time
 
    if cheat_mode:
        current_time = time.time()
        if current_time - cheat_start_time > cheat_duration:
            cheat_mode = False
        else:
            return 
    
    if car_position_y > ground_level + obstacle_height:
        return
        
    car_width = 0.2
    car_length = 0.6
    
    obstacles = [(obstacle1_x, obstacle1_z), (obstacle2_x, obstacle2_z), (obstacle3_x, obstacle3_z)]
    
    for obs_x, obs_z in obstacles:
        if (abs(car_position_x - obs_x) < (car_width + obstacle_width/2) and 
            abs(car_position_z - obs_z) < (car_length + obstacle_depth/2)):
            game_over = True


def update():
    global car_position_x, target_x, car_position_z, target_z, game_over, track_position
    global obstacle1_z, obstacle2_z, obstacle3_z, obstacle1_x, obstacle2_x, obstacle3_x
    global obstacle4_z, obstacle5_z, obstacle6_z, obstacle4_x, obstacle5_x, obstacle6_x
    global coin1_z, coin2_z, coin1_x, coin2_x, track_speed
    global jump_powers, powerup_z, powerup_x, last_powerup_score
    global trees, grass_patches
    global shoot_powers, bullets, current_powerup_type 
    global current_obstacle_count, score
    global car_frozen, freeze_start_time 
    global obstacle_boost_active, obstacle_boost_start_time 
    global multiplayer_mode, player2_position_x, player2_target_x, player2_position_z, player2_target_z
    global player2_frozen, player2_freeze_start_time, player2_bullets
    global player2_jump_powers, player2_shoot_powers, player2_score, player2_last_powerup_score

    if not game_over:
        update_car_physics()
        update_player2_physics()
        update_screen_effects()  

        
        if car_frozen:
            current_time = time.time()
            if current_time - freeze_start_time > freeze_duration:
                car_frozen = False

        if player2_frozen:
            current_time = time.time()
            if current_time - player2_freeze_start_time > freeze_duration:
                player2_frozen = False

        if not car_frozen:
            
            if abs(car_position_x - target_x) > 0.001:
                car_position_x += (target_x - car_position_x) * movement_speed * 10
            
            if abs(car_position_z - target_z) > 0.001:
                car_position_z += (target_z - car_position_z) * movement_speed * 8

        # player2 movement
        if multiplayer_mode and not player2_frozen:
            if abs(player2_position_x - player2_target_x) > 0.001:
                player2_position_x += (player2_target_x - player2_position_x) * movement_speed * 10
            
            if abs(player2_position_z - player2_target_z) > 0.001:
                player2_position_z += (player2_target_z - player2_position_z) * movement_speed * 8


        
        # difficulty ++ if score ++
        if score >= 100:
            current_obstacle_count = min(max_obstacles, 4 + (score - 100) // 50)
        
        speed_multiplier = get_speed_multiplier()
        track_speed = initial_track_speed * speed_multiplier
        
        speed_multiplier = get_speed_multiplier()
        track_speed = initial_track_speed * speed_multiplier
        
        
        track_position += track_speed
        
        obstacle1_z += track_speed
        obstacle2_z += track_speed
        obstacle3_z += track_speed
        
        if current_obstacle_count >= 4:
            obstacle4_z += track_speed
        if current_obstacle_count >= 5:
            obstacle5_z += track_speed
        if current_obstacle_count >= 6:
            obstacle6_z += track_speed
        
        # add the new obstacles
        current_spawn_rate = boosted_obstacle_spawn_rate if obstacle_boost_active else normal_obstacle_spawn_rate


        if obstacle1_z > 5.0:
            obstacle1_z = -current_spawn_rate
            obstacle1_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
        
        if obstacle2_z > 5.0:
            obstacle2_z = -current_spawn_rate
            obstacle2_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
            
        if obstacle3_z > 5.0:
            obstacle3_z = -current_spawn_rate
            obstacle3_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
            
        if current_obstacle_count >= 4 and obstacle4_z > 5.0:
            obstacle4_z = -current_spawn_rate
            obstacle4_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
            
        if current_obstacle_count >= 5 and obstacle5_z > 5.0:
            obstacle5_z = -current_spawn_rate
            obstacle5_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
            
        if current_obstacle_count >= 6 and obstacle6_z > 5.0:
            obstacle6_z = -current_spawn_rate
            obstacle6_x = (random.random() * 2 - 1) * (track_width/2 - obstacle_width/2)
        
        if obstacle_boost_active:
            current_time = time.time()
            if current_time - obstacle_boost_start_time > obstacle_boost_duration:
                obstacle_boost_active = False       

        # move coins
        coin1_z += track_speed
        coin2_z += track_speed
        
        if coin1_z > 5.0:
            coin1_z = -30.0
            coin1_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)
        
        if coin2_z > 5.0:
            coin2_z = -30.0
            coin2_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)
        
        # move environment objects
        for tree in trees:
            tree['z'] += track_speed
            if tree['z'] > 10:
                tree['z'] = -50
                tree['x'] = random.choice([-1, 1]) * random.uniform(3, 8)
        
        for patch in grass_patches:
            patch['z'] += track_speed
            if patch['z'] > 10:
                patch['z'] = -50
                patch['x'] = random.choice([-1, 1]) * random.uniform(4.0, 10)    

        check_coin_collection()
        check_player2_coin_collection()
        
        # update powerup 
        powerup_z += track_speed
        if powerup_z > 5.0:
            should_spawn_powerup = False
            
            if multiplayer_mode:
                # if multiplayer, if need powerup AND score lim, spawn 
                player1_needs_powerup = (score >= last_powerup_score + powerup_spawn_interval and 
                                       (jump_powers < max_jump_powers or shoot_powers < max_shoot_powers))
                player2_needs_powerup = (player2_score >= player2_last_powerup_score + powerup_spawn_interval and 
                                       (player2_jump_powers < max_jump_powers or player2_shoot_powers < max_shoot_powers))
                should_spawn_powerup = player1_needs_powerup or player2_needs_powerup
            else:
                # single player 
                should_spawn_powerup = (score >= last_powerup_score + powerup_spawn_interval and 
                                      (jump_powers < max_jump_powers or shoot_powers < max_shoot_powers))
            
            if should_spawn_powerup:
                powerup_z = -35.0
                powerup_x = (random.random() * 2 - 1) * (track_width/2 - powerup_radius)
                
                available_types = [POWERUP_FREEZE, POWERUP_OBSTACLE_BOOST, POWERUP_SCORE_DRAIN]
                
                # fairness 
                if multiplayer_mode:
                    if jump_powers < max_jump_powers or player2_jump_powers < max_jump_powers:
                        available_types.append(POWERUP_JUMP)
                    if shoot_powers < max_shoot_powers or player2_shoot_powers < max_shoot_powers:
                        available_types.append(POWERUP_SHOOT)
                else:
                    if jump_powers < max_jump_powers:
                        available_types.append(POWERUP_JUMP)
                    if shoot_powers < max_shoot_powers:
                        available_types.append(POWERUP_SHOOT)

                if available_types:
                    current_powerup_type = random.choice(available_types)
            else:
                powerup_z = -50.0
        
        
        check_powerup_collection()
        check_player2_powerup_collection()
        check_collision()
        check_player2_collision()
        check_game_over()
    
    
    update_bullets()
    update_player2_bullets()
    check_bullet_collision()
    check_player2_bullet_collision()
    
    glutPostRedisplay()

def draw_coins():
    global coin1_x, coin1_z, coin2_x, coin2_z
    
    quadric = gluNewQuadric()
    glColor3f(1.0, 0.84, 0.0)  
    
    glPushMatrix()
    glTranslatef(coin1_x, -0.3, coin1_z)
    gluSphere(quadric, coin_radius, 12, 12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(coin2_x, -0.3, coin2_z)
    gluSphere(quadric, coin_radius, 12, 12)
    glPopMatrix()

def check_coin_collection():
    global car_position_x, car_position_z, coin1_x, coin1_z, coin2_x, coin2_z, score
    
    collection_distance = 0.3
    
    if (abs(car_position_x - coin1_x) < collection_distance and 
        abs(car_position_z - coin1_z) < collection_distance):
        score += 10
        coin1_z = -30.0  
        coin1_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)
    
    if (abs(car_position_x - coin2_x) < collection_distance and 
        abs(car_position_z - coin2_z) < collection_distance):
        score += 10
        coin2_z = -30.0
        coin2_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)

def check_player2_coin_collection():
    global player2_position_x, player2_position_z, coin1_x, coin1_z, coin2_x, coin2_z, player2_score
    
    if not multiplayer_mode:
        return
        
    collection_distance = 0.3
    
    if (abs(player2_position_x - coin1_x) < collection_distance and 
        abs(player2_position_z - coin1_z) < collection_distance):
        player2_score += 10
        coin1_z = -30.0  
        coin1_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)
    
    if (abs(player2_position_x - coin2_x) < collection_distance and 
        abs(player2_position_z - coin2_z) < collection_distance):
        player2_score += 10
        coin2_z = -30.0
        coin2_x = (random.random() * 2 - 1) * (track_width/2 - coin_radius)

def check_powerup_collection():
    global car_position_x, car_position_z, powerup_x, powerup_z, jump_powers
    global last_powerup_score, score, current_powerup_type, shoot_powers
    global car_frozen, freeze_start_time
    global obstacle_boost_active, obstacle_boost_start_time  
    
    collection_distance = 0.3
    if (abs(car_position_x - powerup_x) < collection_distance and 
        abs(car_position_z - powerup_z) < collection_distance and
        powerup_z > -40.0 and powerup_z < 10.0):  
        
        if current_powerup_type == POWERUP_JUMP:
            jump_powers = min(jump_powers + 1, max_jump_powers)
        elif current_powerup_type == POWERUP_SHOOT:
            shoot_powers = min(shoot_powers + shots_per_powerup, max_shoot_powers)
        elif current_powerup_type == POWERUP_FREEZE:
            car_frozen = True
            freeze_start_time = time.time()
        elif current_powerup_type == POWERUP_OBSTACLE_BOOST:
            obstacle_boost_active = True
            obstacle_boost_start_time = time.time()
        elif current_powerup_type == POWERUP_SCORE_DRAIN:
            score = max(0, score - 30)  # -30 score, min = 0

        last_powerup_score = score
        powerup_z = -50.0

def check_player2_powerup_collection():
    global player2_position_x, player2_position_z, powerup_x, powerup_z, player2_jump_powers
    global player2_last_powerup_score, player2_score, current_powerup_type, player2_shoot_powers
    global player2_frozen, player2_freeze_start_time
    global obstacle_boost_active, obstacle_boost_start_time  
    
    if not multiplayer_mode:
        return

    collection_distance = 0.3
    if (abs(player2_position_x - powerup_x) < collection_distance and 
        abs(player2_position_z - powerup_z) < collection_distance and
        powerup_z > -40.0 and powerup_z < 10.0):  
        
        if current_powerup_type == POWERUP_JUMP:
            player2_jump_powers = min(player2_jump_powers + 1, max_jump_powers)
        elif current_powerup_type == POWERUP_SHOOT:
            player2_shoot_powers = min(player2_shoot_powers + shots_per_powerup, max_shoot_powers)
        elif current_powerup_type == POWERUP_FREEZE:
            player2_frozen = True
            player2_freeze_start_time = time.time()
        elif current_powerup_type == POWERUP_OBSTACLE_BOOST:
            obstacle_boost_active = True
            obstacle_boost_start_time = time.time()
        elif current_powerup_type == POWERUP_SCORE_DRAIN:
            player2_score = max(0, player2_score - 30)  # -30 score, min = 0

        player2_last_powerup_score = player2_score
        powerup_z = -50.0

def draw_powerup():
    global powerup_x, powerup_z, score, last_powerup_score, current_powerup_type
    global player2_score, player2_last_powerup_score
    
    # powerup visible?
    should_show_powerup = False
    
    if multiplayer_mode:
        # if multiplayer, if at least one > score lim, show 
        player1_eligible = score >= last_powerup_score + powerup_spawn_interval
        player2_eligible = player2_score >= player2_last_powerup_score + powerup_spawn_interval
        should_show_powerup = (player1_eligible or player2_eligible) and powerup_z > -40.0 and powerup_z < 10.0
    else:
        # single player
        should_show_powerup = score >= last_powerup_score + powerup_spawn_interval and powerup_z > -40.0 and powerup_z < 10.0
    
    if should_show_powerup:
        quadric = gluNewQuadric()
        bounce_offset = math.sin(time.time() * 5) * 0.1
        
        # powerup clr
        if current_powerup_type == POWERUP_JUMP:
            glColor3f(0.0, 0.5, 1.0)  # blue->jump
        
        elif current_powerup_type == POWERUP_FREEZE:
            glColor3f(0.5, 0.0, 0.5)  # purple->freeze (negative)
        
        elif current_powerup_type == POWERUP_OBSTACLE_BOOST:
            glColor3f(1.0, 0.0, 0.0)  # red->obstacle boost (negative)
        elif current_powerup_type == POWERUP_SCORE_DRAIN:
            glColor3f(0.8, 0.0, 0.8)  # magenta->score drain (negative)

        else:
            glColor3f(1.0, 0.5, 0.0)  # orange->shoot
        
        glPushMatrix()
        glTranslatef(powerup_x, -0.3 + bounce_offset, powerup_z)
        glRotatef(time.time() * 50, 0, 1, 0)
        gluSphere(quadric, powerup_radius, 12, 12)
        glPopMatrix()


def draw_score():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    if multiplayer_mode:
        # player1 info on right
        glColor3f(1.0, 0.0, 0.0)  # red for Player 1 header
        glRasterPos2f(600, 570)
        player1_header = "PLAYER-1"
        for c in player1_header:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        # player1 score
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(600, 550)
        score_text = f"Score: {score}"
        for c in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        # player1 jump powers
        glColor3f(0.0, 0.5, 1.0)
        glRasterPos2f(600, 530)
        jump_text = f"Jump Powers: {jump_powers}"
        for c in jump_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # player1 shoot 
        glColor3f(1.0, 0.5, 0.0)
        glRasterPos2f(600, 510)
        shoot_text = f"Shoot Powers: {shoot_powers}"
        for c in shoot_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        if car_frozen:
            glColor3f(0.5, 0.0, 0.5)
            glRasterPos2f(600, 490)
            remaining_freeze = max(0, freeze_duration - (time.time() - freeze_start_time))
            freeze_text = f"FROZEN: {remaining_freeze:.1f}s"
            for c in freeze_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if obstacle_boost_active:
            glColor3f(1.0, 0.0, 0.0)
            glRasterPos2f(600, 470)
            remaining_boost = max(0, obstacle_boost_duration - (time.time() - obstacle_boost_start_time))
            boost_text = f"OBSTACLE BOOST: {remaining_boost:.1f}s"
            for c in boost_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if cheat_mode:
            glColor3f(0.5, 0.5, 1.0)
            glRasterPos2f(600, 450)
            remaining_time = max(0, cheat_duration - (time.time() - cheat_start_time))
            cheat_text = f"CHEAT: {remaining_time:.1f}s"
            for c in cheat_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        else:
            current_time = time.time()
            if current_time - last_cheat_use < cheat_cooldown:
                glColor3f(0.7, 0.7, 0.7)
                glRasterPos2f(600, 450)
                cooldown_remaining = cheat_cooldown - (current_time - last_cheat_use)
                cooldown_text = f"Cheat CD: {cooldown_remaining:.1f}s"
                for c in cooldown_text:
                    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # player2 info on left
        glColor3f(0.0, 0.0, 1.0)  # blue for Player 2 header
        glRasterPos2f(10, 570)
        player2_header = "PLAYER-2"
        for c in player2_header:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        # player2 score
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(10, 550)
        score_text = f"Score: {player2_score}"
        for c in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        # player2 jump powers
        glColor3f(0.0, 0.5, 1.0)
        glRasterPos2f(10, 530)
        jump_text = f"Jump Powers: {player2_jump_powers}"
        for c in jump_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # player2 shoot 
        glColor3f(1.0, 0.5, 0.0)
        glRasterPos2f(10, 510)
        shoot_text = f"Shoot Powers: {player2_shoot_powers}"
        for c in shoot_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        if player2_frozen:
            glColor3f(0.5, 0.0, 0.5)
            glRasterPos2f(10, 490)
            remaining_freeze = max(0, freeze_duration - (time.time() - player2_freeze_start_time))
            freeze_text = f"FROZEN: {remaining_freeze:.1f}s"
            for c in freeze_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if player2_cheat_mode:
            glColor3f(0.5, 0.5, 1.0)
            glRasterPos2f(10, 470)
            remaining_time = max(0, cheat_duration - (time.time() - player2_cheat_start_time))
            cheat_text = f"CHEAT: {remaining_time:.1f}s"
            for c in cheat_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        else:
            current_time = time.time()
            if current_time - player2_last_cheat_use < cheat_cooldown:
                glColor3f(0.7, 0.7, 0.7)
                glRasterPos2f(10, 470)
                cooldown_remaining = cheat_cooldown - (current_time - player2_last_cheat_use)
                cooldown_text = f"Cheat CD: {cooldown_remaining:.1f}s"
                for c in cooldown_text:
                    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # multiplayer indicator
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(350, 570)
        mode_text = "MULTIPLAYER MODE"
        for c in mode_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    else:
        # single player -> display on left
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(10, 570)
        score_text = f"Score: {score}"
        for c in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        # jump powers
        glColor3f(0.0, 0.5, 1.0)
        glRasterPos2f(10, 550)
        jump_text = f"Jump Powers: {jump_powers}"
        for c in jump_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # shoot powers
        glColor3f(1.0, 0.5, 0.0)
        glRasterPos2f(10, 530)
        shoot_text = f"Shoot Powers: {shoot_powers}"
        for c in shoot_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        if car_frozen:
            glColor3f(0.5, 0.0, 0.5)
            glRasterPos2f(10, 490)
            remaining_freeze = max(0, freeze_duration - (time.time() - freeze_start_time))
            freeze_text = f"FROZEN: {remaining_freeze:.1f}s"
            for c in freeze_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if obstacle_boost_active:
            glColor3f(1.0, 0.0, 0.0)
            glRasterPos2f(10, 470)
            remaining_boost = max(0, obstacle_boost_duration - (time.time() - obstacle_boost_start_time))
            boost_text = f"OBSTACLE BOOST: {remaining_boost:.1f}s"
            for c in boost_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if cheat_mode:
            glColor3f(0.5, 0.5, 1.0)
            glRasterPos2f(10, 510)
            remaining_time = max(0, cheat_duration - (time.time() - cheat_start_time))
            cheat_text = f"CHEAT ACTIVE: {remaining_time:.1f}s"
            for c in cheat_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        else:
            current_time = time.time()
            if current_time - last_cheat_use < cheat_cooldown:
                glColor3f(0.7, 0.7, 0.7)
                glRasterPos2f(10, 510)
                cooldown_remaining = cheat_cooldown - (current_time - last_cheat_use)
                cooldown_text = f"Cheat Cooldown: {cooldown_remaining:.1f}s"
                for c in cooldown_text:
                    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))   

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def idle():
    global last_update_time
    current_time = time.time()
    
    if current_time - last_update_time >= UPDATE_INTERVAL:
        update()
        last_update_time = current_time



def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b" 3D Car Racing ")
   
    init()
    glutDisplayFunc(showScreen)        
    glutKeyboardFunc(keyboardListener) 
    glutSpecialFunc(specialKeyListener) 
    glutMouseFunc(mouseListener)       
    glutIdleFunc(idle)  
   
    glutMainLoop()

if __name__ == "__main__":
    main()