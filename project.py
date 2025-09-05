from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


# Camera-related variables
camera_pos = (0, 500, 900)
look_at_target = (0, 0, 0)
camera_angle = 0
speed_r = 5
player_pos_x = 0
player_pos_y = 0
player_pos_z = 0
player_angle = 0
maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]]




maze_width = len(maze[0])
maze_height = len(maze)
cell_size = 100
free_space = []
offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)
player_pos_x = player_pos_x * cell_size - offset_x
player_pos_y = player_pos_y * cell_size - offset_y
player_life=2

coin = []  # pink ball
bonus_coin = []  # yellow coin
count=0
score=0
time=180

coin_big = False
coin_rotate = 0




fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines


shield= False
shield_count=2


for m in range(len(maze)):
    for n in range(len(maze[0])):
        if maze[m][n] == 0:
            free_space.append([n, m])  # stores the free space co ordinate







while count < 7:  # postion of coins
    x_e = random.randint(0, 18)
    y_e = random.randint(0, 18)
    if [x_e, y_e] in free_space:
        free_space.remove([x_e, y_e])
        coin.append([x_e, y_e])


        count += 1
count = 0
while count < 4:  # postion of bonus coins
    x_e = random.randint(0, 18)
    y_e = random.randint(0, 18)
    if [x_e, y_e] in free_space:
        free_space.remove([x_e, y_e])
        bonus_coin.append([x_e, y_e])
        count += 1
scale_x = 0.1
scale_y = 0.1
scale_z = 0.1

# for coin squizing







def setupCamera():
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1700)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix


    # Extract camera position and look-at target
    x, y, z = camera_pos
    d, e, f = look_at_target




    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              d, e, f,  # Look-at target -600
              0, 0, 1)  # Up vector (z-axis)


def draw_maze():
    global maze_height, maze_width, cell_size


    # Calculate offset to center the maze
    offset_x = -(maze_width * cell_size) / 2 + cell_size / 2  # calculating actual position in grid
    offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)  # calculating actual position in grid


    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j] == 1:  # Wall
                x_pos = offset_x + j * cell_size  # increamenting
                y_pos = offset_y + i * cell_size


                glPushMatrix()
                glTranslatef(x_pos, y_pos, 0)
                glColor3f(0.3, 0.5, 0.8)  # Blue walls
                glutSolidCube(100)  # Slightly smaller for gaps
                glPopMatrix()




def can_move_to(new_x, new_y):
    global maze_height, maze_width, cell_size
    # Convert player position to maze coordinates
    offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
    offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)


    # Calculate grid cell
    grid_x = int((new_x - offset_x + cell_size / 2) / cell_size)  # actual postion/100 to match with matrix index
    grid_y = int((new_y - offset_y + cell_size / 2) / cell_size)


    # Check if within bounds and not a wall
    if 0 < grid_x < maze_width and 0 < grid_y < maze_height:
        return maze[grid_y][grid_x] == 0
    return False




def draw_player():
    global player_pos_x, player_pos_y, player_pos_z, player_angle, shield_count, shield
    glPushMatrix()
    glTranslatef(player_pos_x, player_pos_y, player_pos_z)
    glRotatef(player_angle, 0, 0, 1)
    if shield == True and shield_count >= 0:
        glColor3f(1, 1, 1)
        glutSolidCube(60)
    # body
    glColor3f(1, 0, 0)
    glutSolidCube(30)


    # Right_Hand
    glColor3f(0.9, 0.8, 0.7)
    glTranslatef(-15, -15, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 30, 10, 10)


    # Left_Hand
    glColor3f(0.9, 0.8, 0.7)
    glTranslatef(30, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 30, 10,
                10)  # parameters are: quadric, base radius, top radius, height, slices, stacks


    # #GUN
    glColor3f(0.8, 0.1, 0.5)
    glTranslatef(-15, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 30, 10,
                10)  # parameters are: quadric, base radius, top radius, height, slices, stacks


    # right_leg


    glColor3f(0, 1, 0)
    glTranslatef(-15, -15, -15)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 45, 100, 100)


    # leftleg
    glTranslatef(30, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 45, 10,
                10)  # parameters are: quadric, base radius, top radius, height, slices, stacks


    # head
    glColor3f(0, 0, 0)
    glTranslatef(-15, 0, -40)
    glRotatef(player_angle, 0, 0, 1)
    gluSphere(gluNewQuadric(), 10, 100, 100)
    # parameters are: quadric, radius, slices, stacks
    glPopMatrix()




def draw_coin(x_e, y_e):
    global maze_height, maze_width, cell_size, scale_x, scale_y, scale_z
    ofst_x = -(maze_width * cell_size) / 2 + cell_size / 2
    ofst_y = -((maze_height * cell_size) / 2 - cell_size / 2)
    x_p = ofst_x + x_e * cell_size
    y_p = ofst_y + y_e * cell_size


    glPushMatrix()
    glTranslatef(x_p, y_p, 0)
    glColor3f(1, 0, 1)
    glScalef(scale_x, scale_y, scale_z)
    gluSphere(gluNewQuadric(), 10, 100, 100)
    glPopMatrix()


def draw_bonus_coin(x_b, y_b):
    global maze_height, maze_width, cell_size, coin_rotate
    ofst_x = -(maze_width * cell_size) / 2 + cell_size / 2
    ofst_y = -((maze_height * cell_size) / 2 - cell_size / 2)
    x_p = ofst_x + x_b * cell_size
    y_p = ofst_y + y_b * cell_size




    glPushMatrix()
    glTranslatef(x_p, y_p, 0)
    glColor3f(0.9, 0.9, 0)
    glRotatef(coin_rotate, 0, 0, 1)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 15, 3, 10, 10)
    glPopMatrix()


def animation():
    global score, coin, bonus_coin, maze_height, maze_width, cell_size, scale_x, scale_y, scale_z, coin_big, coin_rotate, offset_x, offset_y, player_pos_x, player_pos_y
    player_grid_x = int((player_pos_x - offset_x + cell_size / 2) / cell_size)
    player_grid_y = int((player_pos_y - offset_y + cell_size / 2) / cell_size)
        
    if scale_x > 2 and scale_y > 2 and scale_z > 2:
            coin_big = True
    if scale_x < 1 and scale_y < 1 and scale_z < 1:
            coin_big = False


    if coin_big == False:
            scale_x += 0.005
            scale_y += 0.005
            scale_z += 0.005
    if coin_big == True:
            scale_x -= 0.005
            scale_y -= 0.005
            scale_z -= 0.005
        ####################################coin small big########################################
    if coin_rotate < 360:
            coin_rotate += 0.5
    else:
            coin_rotate = 0
        ################################# bonus coin rotate###########################################   
    glutPostRedisplay()


def keyboardListener(key, a, b):
    global player_pos_x, player_pos_y, player_angle, speed_r, shield, shield_count,fovY


    
    if shield == False:
            # Player movement controls
            if key == b'a':  # Move left
                new_x = player_pos_x + math.cos(math.radians(player_angle)) * 30
                new_y = (player_pos_y) + math.sin(math.radians(player_angle)) * 30
                if can_move_to(new_x, new_y):
                    player_pos_x = new_x
                    player_pos_y = new_y

            elif key == b'd':  # Move right
                new_x = player_pos_x - math.cos(math.radians(player_angle)) * 30
                new_y = (player_pos_y) - math.sin(math.radians(player_angle)) * 30
                if can_move_to(new_x, new_y):
                    player_pos_x = new_x
                    player_pos_y = new_y


            elif key == b'w':  # move_forward
                new_x = player_pos_x + math.cos(math.radians(player_angle - 90)) * 30
                new_y = player_pos_y + math.sin(math.radians(player_angle - 90)) * 30
                if can_move_to(new_x, new_y):
                    player_pos_x = new_x
                    player_pos_y = new_y


            elif key == b's':  # move back
                new_x = player_pos_x + math.cos(math.radians(player_angle + 90)) * 30
                new_y = (player_pos_y) + math.sin(math.radians(player_angle + 90)) * 30
                if can_move_to(new_x, new_y):
                    player_pos_x = new_x
                    player_pos_y = new_y


    if key == b' ':
                if shield == True:
                   shield = False
                else:
                    if shield_count > 0 and shield == False:
                        shield = True
                        shield_count -= 1


    if key == b'z':  # rotate left


        if player_angle < 360:
            player_angle += speed_r
        else:
            player_angle = 0
    if key == b'x':  # rotate right


        if player_angle > 0:
            player_angle -= speed_r
        else:
            player_angle = 360
    glutPostRedisplay()
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    # glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def showScreen():
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size


    setupCamera()


    draw_maze()

    draw_player()


    
    for e in coin:
            draw_coin(e[0], e[1])
    for b in bonus_coin:
            draw_bonus_coin(b[0], b[1])
            glColor3f(1, 1, 1)
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Remaining time: {int(time)}")
    draw_text(10, 680, f"Player Life: {player_life}")
    draw_text(10, 650, f"Remaining shield: {int(shield_count)}")
        
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Maze")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    #glutSpecialFunc(specialKeyListener)
    # glutMouseFunc(mouseListener)
    glutIdleFunc(animation)  # Register the idle function to move the bullet automatically
    glutMainLoop()  # Enter the GLUT main loop




if __name__ == "__main__":
    main()




