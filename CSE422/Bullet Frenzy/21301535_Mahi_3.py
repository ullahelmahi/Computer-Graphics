from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math 
import random

camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 600
GRID_CELLS = 13 
CELL_SIZE = GRID_LENGTH * 2 / GRID_CELLS
rand_var = 423

player_pos = [0, 0, 0]
player_angle = 0
bullets = []
enemies = []
ENEMY_COUNT = 5
game_over = False
score = 0
animation_phase = 0
player_life = 5
bullets_missed = 0
MAX_BULLETS_MISSED = 10
player_is_down = False
is_first_person = False
cheat_mode = False
cheat_rotation_speed = .5
time_since_last_auto_fire = 0
auto_fire_interval = 30 

auto_follow = False


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text_end(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if is_first_person:
        if auto_follow:
            # Freeze camera a little behind and above the head
            head_height = 80
            behind_offset = -60   
            above_offset = 120     
            eye_x = player_pos[0]
            eye_y = player_pos[1] + behind_offset
            eye_z = player_pos[2] + head_height + above_offset
            gluLookAt(eye_x, eye_y, eye_z,
                      player_pos[0], player_pos[1] + 200, player_pos[2] + head_height,
                      0, 0, 1)
        else:
            # Normal first-person (follows body/gun)
            angle_rad = math.radians(player_angle)
            offset_behind = 20
            offset_up = 70
            eye_x = player_pos[0] - math.sin(angle_rad) * offset_behind
            eye_y = player_pos[1] - math.cos(angle_rad) * offset_behind
            eye_z = player_pos[2] + offset_up
            look_distance = 200
            look_x = player_pos[0] + math.sin(angle_rad) * look_distance
            look_y = player_pos[1] + math.cos(angle_rad) * look_distance
            look_z = eye_z - 5
            gluLookAt(eye_x, eye_y, eye_z,
                      look_x, look_y, look_z,
                      0, 0, 1)
    else:
        # Third-person
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)


def spawn_enemy():
    while True:
        x = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        y = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        dist = math.sqrt((x - player_pos[0])**2 + (y - player_pos[1])**2)
        if dist > 200:
            break
    return [x, y, 30, 1.0]

def draw_player():
    global player_angle
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)
    
    if player_is_down:
        glRotatef(90, 1, 0, 0)
    
    if is_first_person:
        # In first person mode, show the gun
        glColor3f(0.8, 0.8, 0.0)
        glPushMatrix()
        glTranslatef(0, 0, -40)
        gluCylinder(gluNewQuadric(), 5, 5, 90, 10, 5)
        glPopMatrix()
        
        # If auto_follow (V mode) is on, also show the rotating body
        if auto_follow:
            
            glColor3f(0.2, 0.8, 0.2)
            glPushMatrix()
            glTranslatef(0, 0, 0)
            glScalef(40, 30, 110)
            glutSolidCube(1)
            glPopMatrix()
            
            glColor3f(0.7, 0.7, 0.7)
            glTranslatef(0, 0, 70)
            gluSphere(gluNewQuadric(), 20, 20, 20)
            
            glColor3f(0.0, 0.0, 0.8)
            glPushMatrix()
            glTranslatef(-30, 60, -20)
            glRotatef(90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(30, 60, -20)
            glRotatef(90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(-15, 20, -55)
            glRotatef(180, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 5)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(15, 20, -55)
            glRotatef(180, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 5)
            glPopMatrix()
    else:
        glColor3f(0.2, 0.8, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glScalef(40, 30, 110)
        glutSolidCube(1)
        glPopMatrix()
        
        glColor3f(0.7, 0.7, 0.7)
        glTranslatef(0, 0, 70)
        gluSphere(gluNewQuadric(), 20, 20, 20)
        
        glColor3f(0.0, 0.0, 0.8)
        glPushMatrix()
        glTranslatef(-30, 60, -20)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 5)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(30, 60, -20)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 5)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-15, 20, -55)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 5)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(15, 20, -55)
        glRotatef(180, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 5)
        glPopMatrix()
        
        glColor3f(0.8, 0.8, 0.0)
        glPushMatrix()
        glTranslatef(0, 30, -40)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 5)
        glPopMatrix()
    
    glPopMatrix()

def draw_bullet(x, y, z):
    global bullets_missed
    if cheat_mode == True:
        bullets_missed = 0
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0.8, 0.0)
    glutSolidCube(15)
    glPopMatrix()

def update_bullets():
    global bullets, bullets_missed, game_over
    new_bullets = []
    
    for bullet in bullets:
        x, y, z, dx, dy = bullet
        x += dx
        y += dy
        if abs(x) < GRID_LENGTH and abs(y) < GRID_LENGTH:
            new_bullets.append((x, y, z, dx, dy))
        else:
            bullets_missed += 1
            if bullets_missed >= MAX_BULLETS_MISSED:
                game_over = True
    bullets = new_bullets

def fire_bullet():
    angle_rad = math.radians(player_angle)
    dx = math.sin(-angle_rad) * 15
    dy = math.cos(-angle_rad) * 15
    weapon_length = 50
    weapon_tip_x = player_pos[0] + math.sin(angle_rad) * weapon_length
    weapon_tip_y = player_pos[1] + math.cos(angle_rad) * weapon_length
    weapon_tip_z = player_pos[2] + 20
    bullets.append((weapon_tip_x, weapon_tip_y, weapon_tip_z, dx, dy))

def draw_enemy(x, y, z, size_factor):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0.0, 0.0)
    base_size = 40 * size_factor
    gluSphere(gluNewQuadric(), base_size, 20, 20)
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 50 * size_factor)
    gluSphere(gluNewQuadric(), 15 * size_factor, 20, 20)
    glPopMatrix()

def update_enemies():
    global enemies, animation_phase, score, game_over, player_life, player_is_down
    animation_phase += 0.1
    if animation_phase > 8.28:
        animation_phase = 0
    while len(enemies) < ENEMY_COUNT:
        enemies.append(spawn_enemy())
    for i, enemy in enumerate(enemies):
        x, y, z, _ = enemy
        dx = player_pos[0] - x
        dy = player_pos[1] - y
        dist = math.sqrt(dx*dx + dy*dy)
        speed = 0.051
        if dist > 0:
            dx = dx / dist * speed
            dy = dy / dist * speed
        new_x = x + dx
        new_y = y + dy
        size_factor = 0.8 + 0.2 * math.sin(animation_phase)
        enemies[i] = [new_x, new_y, z, size_factor]
        if dist < 60:
            enemies.pop(i)
            player_life -= 1
            if player_life <= 0:
                game_over = True
                player_is_down = True
            break

def check_bullet_enemy_collisions():
    global bullets, enemies, score
    bullets_to_remove = []
    enemies_to_remove = []
    for i, bullet in enumerate(bullets):
        bx, by, bz, _, _ = bullet
        for j, enemy in enumerate(enemies):
            ex, ey, ez, _ = enemy
            dist = math.sqrt((bx - ex)**2 + (by - ey)**2 + (bz - ez)**2)
            if dist < 50:
                bullets_to_remove.append(i)
                enemies_to_remove.append(j)
                score += 10
                break
    for i in sorted(bullets_to_remove, reverse=True):
        if i < len(bullets):
            bullets.pop(i)
    for i in sorted(enemies_to_remove, reverse=True):
        if i < len(enemies):
            enemies.pop(i)

def draw_grid():
    # Vertical lines
    for i in range(GRID_CELLS + 1):
        x = -GRID_LENGTH + i * CELL_SIZE
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_QUADS)
        glVertex3f(x - 1, -GRID_LENGTH, 0.1)
        glVertex3f(x + 1, -GRID_LENGTH, 0.1)
        glVertex3f(x + 1, GRID_LENGTH, 0.1)
        glVertex3f(x - 1, GRID_LENGTH, 0.1)
        glEnd()
    
    # Horizontal lines
    for i in range(GRID_CELLS + 1):
        y = -GRID_LENGTH + i * CELL_SIZE
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_QUADS)
        glVertex3f(-GRID_LENGTH, y - 1, 0.1)
        glVertex3f(GRID_LENGTH, y - 1, 0.1)
        glVertex3f(GRID_LENGTH, y + 1, 0.1)
        glVertex3f(-GRID_LENGTH, y + 1, 0.1)
        glEnd()
    
    # Draw checkered pattern
    for i in range(GRID_CELLS):
        for j in range(GRID_CELLS):
            if (i + j) % 2 == 0:
                glColor3f(0.9, 0.9, 0.9)
            else:
                glColor3f(0.5, 0.5, 0.9)
            x1 = -GRID_LENGTH + i * CELL_SIZE
            y1 = -GRID_LENGTH + j * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            glBegin(GL_QUADS)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
            glEnd()

def draw_boundaries():
    wall_height = 200
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    
    glColor3f(0, 0, 1)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    
    glColor3f(0, 1, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    
    glColor3f(0, 1, 1)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_LEFT and cx > -330:
        cx -= 10
    if key == GLUT_KEY_RIGHT and cx < 330:
        cx += 10
    if key == GLUT_KEY_UP and cz < 1000:
        cz += 10
    if key == GLUT_KEY_DOWN and cz > 150:
        cz -= 10
    camera_pos = (cx, cy, cz)
    glutPostRedisplay()

def is_enemy_in_line_of_sight(enemy_pos):
    angle_rad = math.radians(player_angle)
    dx = enemy_pos[0] - player_pos[0]
    dy = enemy_pos[1] - player_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 400:
        return False
    player_dir_x = math.sin(-angle_rad)
    player_dir_y = math.cos(-angle_rad)
    if dist > 0:
        dx /= dist
        dy /= dist
    dot_product = player_dir_x * dx + player_dir_y * dy
    return dot_product > 0.966

def keyboardListener(key, x, y):
    global player_pos, player_angle, game_over, player_life, score, bullets_missed, player_is_down, enemies, bullets, cheat_mode, auto_follow
    if game_over and key == b'r':
        player_life = 5
        score = 0
        bullets_missed = 0
        game_over = False
        player_is_down = False
        enemies = []
        bullets = []
        player_pos = [0, 0, 0]
        player_angle = 0
        for _ in range(ENEMY_COUNT):
            enemies.append(spawn_enemy())
        glutPostRedisplay()
        return
    if game_over:
        glutPostRedisplay()
        return
    if key == b'w':
        angle_rad = math.radians(player_angle)
        player_pos[0] += math.sin(-angle_rad) * 10
        player_pos[1] += math.cos(-angle_rad) * 10
    if key == b's':
        angle_rad = math.radians(player_angle)
        player_pos[0] -= math.sin(-angle_rad) * 10
        player_pos[1] -= math.cos(-angle_rad) * 10
    if key == b'a':
        player_angle += 5
    if key == b'd':
        player_angle -= 5
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        auto_follow = not auto_follow   # toggle V mode

    player_pos[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[0]))
    player_pos[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[1]))
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global is_first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
        glutPostRedisplay()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        is_first_person = not is_first_person
        glutPostRedisplay()

def idle():
    global player_angle, time_since_last_auto_fire
    if not game_over:
        update_bullets()
        update_enemies()
        check_bullet_enemy_collisions()
        if cheat_mode:
            player_angle += cheat_rotation_speed
            if player_angle > 360:
                player_angle -= 360
            time_since_last_auto_fire += 1
            if time_since_last_auto_fire >= auto_fire_interval:
                for enemy in enemies:
                    if is_enemy_in_line_of_sight(enemy):
                        fire_bullet()
                        time_since_last_auto_fire = 0
                        break
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    draw_grid()
    draw_boundaries()
    
    for bullet in bullets:
        x, y, z, _, _ = bullet
        draw_bullet(x, y, z)
        
    for enemy in enemies:
        x, y, z, size_factor = enemy
        draw_enemy(x, y, z, size_factor)

    # Display game info text
    draw_text(10, 740, f"Score: {score}")
    draw_text(10, 710, f"Life: {player_life}")
    draw_text(10, 680, f"Bullets Missed: {bullets_missed}/{MAX_BULLETS_MISSED}")

    if game_over:
        draw_text_end(400, 400, "G A M E   O V E R")
        draw_text_end(400, 370, "  Press R to restart  ")
        
    draw_player()
    glutSwapBuffers()

def main():
    global player_life, score, bullets_missed, game_over, player_is_down
    player_life = 5
    score = 0
    bullets_missed = 0
    game_over = False
    player_is_down = False
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D Bullet Frenzy")
    
    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    for _ in range(ENEMY_COUNT):
        enemies.append(spawn_enemy())
    main()