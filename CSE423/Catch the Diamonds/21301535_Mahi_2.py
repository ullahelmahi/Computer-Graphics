from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game variables
game_running = True
game_paused = False
game_over = False
score = 0

# Catcher variables
catcher_x = WINDOW_WIDTH // 2
catcher_y = 50
catcher_width = 120
catcher_height = 20

# Diamond variables
diamond_x = 0
diamond_y = 0
diamond_size = 25
diamond_speed = 2
diamond_colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), 
                  (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0),
                  (1.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 1.0)]
current_diamond_color = (1.0, 1.0, 1.0)

# Button positions
restart_button_x = 100
restart_button_y = WINDOW_HEIGHT - 50
pause_button_x = WINDOW_WIDTH // 2
pause_button_y = WINDOW_HEIGHT - 50
exit_button_x = WINDOW_WIDTH - 100
exit_button_y = WINDOW_HEIGHT - 50
button_size = 30

left_key_pressed = False
right_key_pressed = False

# Time tracking for smooth animation
last_time = 0
diamond_fall_timer = 0

def init():
    """Initialize OpenGL settings"""
    global last_time
    glClearColor(0.0, 0.0, 0.2, 1.0)  # Dark blue background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glPointSize(2.0)  
    create_new_diamond()
    last_time = time.time()

def create_new_diamond():
    """Create a new diamond at random position"""
    global diamond_x, diamond_y, current_diamond_color
    diamond_x = random.randint(diamond_size + 50, WINDOW_WIDTH - diamond_size - 50)
    diamond_y = WINDOW_HEIGHT + diamond_size
    current_diamond_color = random.choice(diamond_colors)


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):  # |dx| >= |dy|
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx >= 0 and dy < 0
            return 7
    else:  # |dx| < |dy|
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  # dx >= 0 and dy < 0
            return 6

def convert_to_zone0(x, y, zone):
    
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(int(x), int(y))
    glEnd()

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    
    x = x1_z0
    y = y1_z0
    
    orig_x, orig_y = convert_from_zone0(x, y, zone)
    draw_point(orig_x, orig_y)
    
    while x < x2_z0:
        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE
        x = x + 1
        
        orig_x, orig_y = convert_from_zone0(x, y, zone)
        draw_point(orig_x, orig_y)


def draw_diamond(center_x, center_y, size):
    
    
    draw_line(center_x, center_y + size, center_x + size, center_y)
    
    draw_line(center_x + size, center_y, center_x, center_y - size)
    
    draw_line(center_x, center_y - size, center_x - size, center_y)
    
    draw_line(center_x - size, center_y, center_x, center_y + size)

def draw_catcher(center_x, center_y, width, height):
    
    half_width = width // 2
    
    draw_line(center_x - half_width, center_y, center_x - half_width//2, center_y - height)
    
    draw_line(center_x - half_width//2, center_y - height, center_x + half_width//2, center_y - height)
    
    draw_line(center_x + half_width//2, center_y - height, center_x + half_width, center_y)
    
    draw_line(center_x - half_width, center_y, center_x + half_width, center_y)

def draw_restart_button():
   
    glColor3f(0.0, 0.8, 0.8)  # Bright teal
    
    draw_line(restart_button_x + 15, restart_button_y, restart_button_x - 15, restart_button_y)
    draw_line(restart_button_x - 15, restart_button_y, restart_button_x - 5, restart_button_y + 10)
    draw_line(restart_button_x - 15, restart_button_y, restart_button_x - 5, restart_button_y - 10)

def draw_pause_button():
    
    glColor3f(1.0, 0.6, 0.0)  # Amber
    if game_paused:
        
        draw_line(pause_button_x - 10, pause_button_y - 15, pause_button_x - 10, pause_button_y + 15)
        draw_line(pause_button_x - 10, pause_button_y - 15, pause_button_x + 15, pause_button_y)
        draw_line(pause_button_x + 15, pause_button_y, pause_button_x - 10, pause_button_y + 15)
    else:
       
        draw_line(pause_button_x - 8, pause_button_y - 15, pause_button_x - 8, pause_button_y + 15)
        draw_line(pause_button_x + 8, pause_button_y - 15, pause_button_x + 8, pause_button_y + 15)

def draw_exit_button():
    
    glColor3f(1.0, 0.0, 0.0)  # Red
    
    draw_line(exit_button_x - 15, exit_button_y - 15, exit_button_x + 15, exit_button_y + 15)
    draw_line(exit_button_x - 15, exit_button_y + 15, exit_button_x + 15, exit_button_y - 15)



def check_collision():
    
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top = diamond_y + diamond_size
    diamond_bottom = diamond_y - diamond_size
    
    
    catcher_left = catcher_x - catcher_width // 2
    catcher_right = catcher_x + catcher_width // 2
    catcher_top = catcher_y
    catcher_bottom = catcher_y - catcher_height
   
    return (diamond_left < catcher_right and 
            diamond_right > catcher_left and 
            diamond_bottom < catcher_top and 
            diamond_top > catcher_bottom)

def update_game():
    
    global diamond_y, diamond_speed, score, game_over, last_time, diamond_fall_timer
    
    if game_over or game_paused:
        return
    
    
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    
    diamond_fall_timer += delta_time
    
    
    if diamond_fall_timer > 0.02:  # Update every 20ms for smooth movement
        diamond_y -= diamond_speed
        diamond_fall_timer = 0
    
    
    if check_collision():
        score += 1
        print(f"Score: {score}")
        create_new_diamond()
        
        diamond_speed += 0.2
    
    
    elif diamond_y + diamond_size < 0:
        game_over = True
        print(f"Game Over! Final Score: {score}")

def update_catcher():
    
    global catcher_x
    
    if game_over or game_paused:
        return
    
    
    if left_key_pressed:
        catcher_x -= 0.3
    if right_key_pressed:
        catcher_x += 0.3
    
    
    if catcher_x - catcher_width // 2 < 0:
        catcher_x = catcher_width // 2
    if catcher_x + catcher_width // 2 > WINDOW_WIDTH:
        catcher_x = WINDOW_WIDTH - catcher_width // 2

def restart_game():
    
    global game_over, game_paused, score, diamond_speed, last_time
    game_over = False
    game_paused = False
    score = 0
    diamond_speed = 2
    last_time = time.time()
    create_new_diamond()
    print("Starting Over!")

def toggle_pause():
    
    global game_paused
    if not game_over:
        game_paused = not game_paused
        if game_paused:
            print("Game Paused")
        else:
            print("Game Resumed")

def is_point_in_button(x, y, button_x, button_y):
    
    return (abs(x - button_x) < button_size and 
            abs(y - button_y) < button_size)



def display():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT)
    

    draw_restart_button()
    draw_pause_button()
    draw_exit_button()
    

    if not game_over:
        glColor3f(current_diamond_color[0], current_diamond_color[1], current_diamond_color[2])
        draw_diamond(diamond_x, diamond_y, diamond_size)

    if game_over:
        glColor3f(1.0, 0.0, 0.0)  # Red when game over
    else:
        glColor3f(1.0, 1.0, 1.0)  # White normally
    draw_catcher(catcher_x, catcher_y, catcher_width, catcher_height)
    
    glutSwapBuffers()

def idle():
    update_game()
    update_catcher()
    glutPostRedisplay()

def special_key_down(key, x, y):

    global left_key_pressed, right_key_pressed
    
    if key == GLUT_KEY_LEFT:
        left_key_pressed = True
    elif key == GLUT_KEY_RIGHT:
        right_key_pressed = True

def special_key_up(key, x, y):

    global left_key_pressed, right_key_pressed
    
    if key == GLUT_KEY_LEFT:
        left_key_pressed = False
    elif key == GLUT_KEY_RIGHT:
        right_key_pressed = False

def mouse_click(button, state, x, y):

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       
        opengl_y = WINDOW_HEIGHT - y
        
       
        if is_point_in_button(x, opengl_y, restart_button_x, restart_button_y):
            restart_game()
        elif is_point_in_button(x, opengl_y, pause_button_x, pause_button_y):
            toggle_pause()
        elif is_point_in_button(x, opengl_y, exit_button_x, exit_button_y):
            print(f"Goodbye! Final score: {score}")
            glutLeaveMainLoop()

def main():
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Catch the Diamonds!")
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(special_key_down)
    glutSpecialUpFunc(special_key_up)
    glutMouseFunc(mouse_click)
    
    init()
    
    glutMainLoop()

if __name__ == "__main__":
    main()