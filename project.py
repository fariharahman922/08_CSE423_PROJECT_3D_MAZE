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
bullet_list = []
bullet_c = 1
missed_bullet = 0
game_over = False
maze_width = len(maze[0])
maze_height = len(maze)
cell_size = 100
free_space = []
offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)
player_pos_x = player_pos_x * cell_size - offset_x
player_pos_y = player_pos_y * cell_size - offset_y
player_life = 2

coin = []  # pink ball
bonus_coin = []  # yellow coin
count = 0
score = 0
time = 180
fpp = False

coin_big = False
coin_rotate = 0

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
enemies = []
enemy_count = 0
e_rad = 30
big_small = True
enemy_bullets = []

current_enemy_index = 0  # which enemy's turn
last_shot_time = 0  # track time since last shot
shot_delay = 200  # ms between shots (tune this)
shield = False
shield_count = 2

for m in range(len(maze)):
    for n in range(len(maze[0])):
        if maze[m][n] == 0:
            free_space.append([n, m])  # stores the free space co ordinate


center_x = maze_width // 2
center_y = maze_height // 2
free_space.remove([center_x, center_y])
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
game_win = False
# for coin squizing

life_list = []
if len(life_list) < 1 and free_space:
    x, y = random.choice(free_space)
    free_space.remove([x, y])
    life_list.append([x, y])


while enemy_count < 7:
    x_e = random.randint(0, maze_width - 1)
    y_e = random.randint(0, maze_height - 1)
    if [x_e,y_e] in free_space :
        enemies.append([x_e, y_e])
        free_space.remove([x_e,y_e])
        enemy_count += 1


def setupCamera():
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1700)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    if not fpp:
        x, y, z = camera_pos
        d, e, f = look_at_target

    else:
        rad = math.radians(player_angle + 90)
        x = player_pos_x - 10 * math.cos(rad)
        y = player_pos_y - 10 * math.sin(rad)
        z = 120
        d = player_pos_x - 50 * math.cos(rad)
        e = player_pos_y - 50 * math.sin(rad)
        f = 99

    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              d, e, f,  # Look-at target -600
              0, 0, 1)  # Up vector (z-axis)


def draw_enemy(x_e, y_e):
    global maze_height, maze_width, cell_size
    offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
    offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)
    x_p = offset_x + x_e * cell_size
    y_p = offset_y + y_e * cell_size

    glPushMatrix()
    glTranslatef(x_p, y_p, 20)
    glColor3f(1, 0, 0)
    glutSolidSphere(e_rad, 20, 20)
    glTranslatef(0, 0, 15)
    glColor3f(0, 0, 0)
    glutSolidSphere(e_rad - 20, 20, 20)
    glPopMatrix()


def enemy_size():
    global big_small, e_rad
    if e_rad > 40:
        big_small = False
    elif e_rad < 20:
        big_small = True

    if big_small == True:
        e_rad += 0.04
    else:
        e_rad -= 0.04


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
    gluCylinder(gluNewQuadric(), 7.5, 4, 30, 10,10)  # parameters are: quadric, base radius, top radius, height, slices, stacks

    # #GUN
    glColor3f(0.8, 0.1, 0.5)
    glTranslatef(-15, 0, 0)
    gluCylinder(gluNewQuadric(), 7.5, 4, 30, 10,10)  # parameters are: quadric, base radius, top radius, height, slices, stacks

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


def bullet():
    global bullet_list, bullet_c
    for bullet in bullet_list:
        glPushMatrix()
        glColor3f(bullet_c, 0, 0)
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidCube(10)
        glPopMatrix()


def life(x3,y3):
    global maze_height, maze_width, cell_size
    ofst_x = -(maze_width * cell_size) / 2 + cell_size / 2
    ofst_y = -((maze_height * cell_size) / 2 - cell_size / 2)
    x4 = ofst_x + x3 * cell_size
    y4 = ofst_y + y3 * cell_size
    glPushMatrix()
    glTranslatef(x4, y4, 0)
    glColor3f(0, 1, 0)
    glutSolidCube(60)
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


def grid_to_world(grid_x, grid_y):
    ofx = -(maze_width * cell_size) / 2 + cell_size / 2
    ofy = -((maze_height * cell_size) / 2 - cell_size / 2)
    return ofx + grid_x * cell_size, ofy + grid_y * cell_size


def shoot_at_player(enemy_world_x, enemy_world_y, player_x, player_y):
    # enemy_world_* are already world coords
    angle = math.atan2(player_y - enemy_world_y, player_x - enemy_world_x)
    bullet = [enemy_world_x, enemy_world_y, angle, 2]  # x, y, angle, speed
    enemy_bullets.append(bullet)


def enemy_shoot():
    global current_enemy_index, last_shot_time, shield
    if shield != True:
        now = glutGet(GLUT_ELAPSED_TIME)  # current time in ms

        # fire only if enough time has passed
        if now - last_shot_time > shot_delay and enemies:
            gx, gy = enemies[current_enemy_index]
            ex, ey = grid_to_world(gx, gy)

            if distance(ex, ey, player_pos_x, player_pos_y) < 400:
                shoot_at_player(ex, ey, player_pos_x, player_pos_y)
            # move to next enemy (circular)
            current_enemy_index = (current_enemy_index + 1) % len(enemies)
            last_shot_time = now


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def move_enemy_bullets():
    global enemy_bullets, game_over, player_life
    if game_over == False:
        for bullet in enemy_bullets[:]:
            # Update the bullet position (world coords)
            bullet[0] += math.cos(bullet[2]) * bullet[3]  # x
            bullet[1] += math.sin(bullet[2]) * bullet[3]  # y

            # Collision with walls (can_move_to expects world coords -> ok)
            if not can_move_to(bullet[0], bullet[1]):
                enemy_bullets.remove(bullet)
                continue

            # Collision with the player
            if distance(bullet[0], bullet[1], player_pos_x, player_pos_y) < 15:  # Player radius
                player_life -= 1
                enemy_bullets.remove(bullet)
                if player_life < 0:
                    game_over = True


def draw_enemy_bullets():
    for bullet in enemy_bullets:
        x, y, _, _ = bullet
        glPushMatrix()
        glTranslatef(x, y, 0)
        glColor3f(0, 1, 0)  # Green bullets
        glutSolidSphere(5, 10, 10)
        glPopMatrix()


def animation():
    global count,life_list,player_life,game_win,e_rad,game_over, time, score, coin, bonus_coin, maze_height, maze_width, cell_size, scale_x, scale_y, scale_z, coin_big, coin_rotate, bullet_list, offset_x, offset_y, cell_size, player_pos_x, player_pos_y
    if int(time) <= 0:
        game_over = True
        time = 0
    player_grid_x = int((player_pos_x - offset_x + cell_size / 2) / cell_size)
    player_grid_y = int((player_pos_y - offset_y + cell_size / 2) / cell_size)

    if center_x == player_grid_x and center_y == player_grid_y:
        game_win = True
        game_over = True

    if not game_over:
        time -= 1 / 60
        enemy_size()
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

        bullet_speed = 10
        offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
        offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)

        for bullet in bullet_list:
            # Move bullet
            bullet[0] -= bullet[3] * bullet_speed
            bullet[1] -= bullet[4] * bullet_speed

            # Convert bullet pos to grid index
            grid_x = int((bullet[0] - offset_x + cell_size / 2) / cell_size)
            grid_y = int((bullet[1] - offset_y + cell_size / 2) / cell_size)

            # Check bounds and wall collision
            if 0 <= grid_x < maze_width and 0 <= grid_y < maze_height:
                if maze[grid_y][grid_x] == 1:  # Free space → keep bullet
                    bullet_list.remove(bullet)
            for enemy in enemies:
                ex, ey = grid_to_world(enemy[0], enemy[1])
                if distance(bullet[0], bullet[1], ex, ey) < e_rad:
                    bullet_list.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        player_grid_x = int((player_pos_x - offset_x + cell_size / 2) / cell_size)
        player_grid_y = int((player_pos_y - offset_y + cell_size / 2) / cell_size)
        for l in life_list:
            if player_life < 2:
                if l[0] == player_grid_x and l[1] == player_grid_y:
                    life_list.remove(l)
                    player_life += 1
                    free_space.append([l[0], l[1]])
                    if len(life_list) < 1 and free_space:
                        x, y = random.choice(free_space)
                        free_space.remove([x, y])
                        life_list.append([x, y])



        for c in coin:  # iterate over a copy so we can remove safely
            if c[0] == player_grid_x and c[1] == player_grid_y:
                coin.remove(c)  # remove this coin
                score += 1  # optional
                free_space.append([c[0], c[1]])
                x1 = random.randint(0, 18)
                y1 = random.randint(0, 18)
                if [x1, y1] in free_space:
                    free_space.remove([x1, y1])
                    coin.append([x1, y1])

        # Check bonus coins
        for b in bonus_coin:
            if b[0] == player_grid_x and b[1] == player_grid_y:
                bonus_coin.remove(b)
                score += 5
                free_space.append([b[0], b[1]])
                x2 = random.randint(0, 18)
                y2 = random.randint(0, 18)
                if [x2, y2] in free_space:
                    free_space.remove([x2, y2])
                    bonus_coin.append([x2, y2])
        enemy_size()
        move_enemy_bullets()
        enemy_shoot()
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global fovY, player_pos_z, player_pos_x, player_pos_y, bullet_list, camera_pos, player_angle, fpp, game_over
    # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_over:
            bullet_x = player_pos_x
            bullet_y = player_pos_y
            bullet_z = player_pos_z
            bullet_r = math.radians(player_angle + 90)
            bullet_dx = math.cos(bullet_r)
            bullet_dy = math.sin(bullet_r)
            bullet_list.append([bullet_x, bullet_y, bullet_z, bullet_dx, bullet_dy])

            # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpp = not fpp

    glutPostRedisplay()


def keyboardListener(key, a, b):
    global player_pos_x, player_pos_y, player_angle, speed_r, game_over, shield, shield_count,fovY

    if not game_over:
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

        if key == b'q':
            game_over = not game_over

    if key==b'r':
            restart_game()

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

    if key == b'i':
        fovY -= 10
    if key == b'o':
        fovY += 10

    glutPostRedisplay()

def draw_treasure_box():
    global free_space, center_x, center_y
    cx, cy = grid_to_world(center_x, center_y)

    glPushMatrix()
    glTranslatef(cx, cy, 0)   # place in center cell
    glColor3f(0.8, 0.8, 0)  # brown/orange box
    glutSolidCube(cell_size)
    glTranslatef(0, 0, 80)
    glColor3f(0.6, 0.3, 0)
    glutSolidSphere(30, 30, 30)
    glPopMatrix()

def restart_game():
    global life_list,center_x,center_y,scale_x,scale_y,scale_z,x_e,y_e,shield_count,shield,shot_delay,last_shot_time,current_enemy_index,big_small,enemy_bullets,e_rad,enemy_count,GRID_LENGTH,enemies,offset_x,offset_y,player_pos_x,player_pos_y,player_life,coin,bonus_coin,count,score,time,fpp,coin_big,coin_rotate,fovY ,bullet_c,missed_bullet,game_over,maze_width,maze_height,cell_size,free_space,camera_pos, look_at_target,camera_angle,speed_r,player_pos_x, player_pos_y ,player_pos_z,player_angle, maze,bullet_list
    camera_pos = (0, 500, 900)
    look_at_target = (0, 0, 0)
    camera_angle = 0
    speed_r = 5
    player_pos_x = 0
    player_pos_y = 0
    player_pos_z = 0
    player_angle = 0
    bullet_list = []
    bullet_c = 1
    missed_bullet = 0
    game_over = False
    maze_width = len(maze[0])
    maze_height = len(maze)
    cell_size = 100
    free_space = []
    offset_x = -(maze_width * cell_size) / 2 + cell_size / 2
    offset_y = -((maze_height * cell_size) / 2 - cell_size / 2)
    player_pos_x = player_pos_x * cell_size - offset_x
    player_pos_y = player_pos_y * cell_size - offset_y
    player_life = 2

    coin = []  # pink ball
    bonus_coin = []  # yellow coin
    count = 0
    score = 0
    time = 180
    fpp = False

    coin_big = False
    coin_rotate = 0

    fovY = 120  # Field of view
    GRID_LENGTH = 600  # Length of grid lines
    enemies = []
    enemy_count = 0
    e_rad = 30
    big_small = True
    enemy_bullets = []

    current_enemy_index = 0  # which enemy's turn
    last_shot_time = 0  # track time since last shot
    shot_delay = 200  # ms between shots (tune this)
    shield = False
    shield_count = 2

    for m in range(len(maze)):
        for n in range(len(maze[0])):
            if maze[m][n] == 0:
                free_space.append([n, m])  # stores the free space co ordinate

    center_x = maze_width // 2
    center_y = maze_height // 2
    free_space.remove([center_x, center_y])
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
    life_list = []
    if len(life_list) < 1 and free_space:
        x, y = random.choice(free_space)
        free_space.remove([x, y])
        life_list.append([x, y])


    while enemy_count < 7:
        x_e = random.randint(0, maze_width - 1)
        y_e = random.randint(0, maze_height - 1)
        if [x_e, y_e] in free_space:
            enemies.append([x_e, y_e])
            free_space.remove([x_e, y_e])
            enemy_count += 1


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


def specialKeyListener(key, x, y):
    global camera_pos, camera_angle
    rad = math.radians(camera_angle)
    cam_x, cam_y, cam_z = camera_pos
    d = (cam_x ** 2 + cam_y ** 2) ** 0.5  # consider to center

    # # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        cam_z += 10

    # # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        cam_z -= 10

    # # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        camera_angle -= 5
        rad = math.radians(camera_angle)
        cam_x = d * math.sin(rad)
        cam_y = d * math.cos(rad)
        # Small angle decrement for smooth movement
    #
    # # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        camera_angle += 5
        rad = math.radians(camera_angle)
        cam_x = d * math.sin(rad)
        cam_y = d * math.cos(rad)
    # Small angle increment for smooth movement
    #
    camera_pos = (cam_x, cam_y, cam_z)


def showScreen():
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()

    draw_maze()
    draw_treasure_box()
    draw_player()

    if not game_over:
        bullet()
        for i in enemies:
            draw_enemy(i[0], i[1])

        draw_enemy_bullets()
        for e in coin:
            draw_coin(e[0], e[1])
        for b in bonus_coin:
            draw_bonus_coin(b[0], b[1])
        for l in life_list:
            if player_life <2:
                life(l[0], l[1])

        glColor3f(1, 1, 1)
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Remaining time: {int(time)}")
        draw_text(10, 680, f"Player Life: {player_life}")
        draw_text(10, 650, f"Remaining shield: {int(shield_count)}")
        if int(time) < 20:
            # make it blink every half-second
            if int(time * 2) % 2 == 0:
                glColor3f(1, 0, 0)  # Red
                draw_text(400, 760, " ALERT! TIME IS RUNNING OUT")

    elif game_over and game_win:
        glColor3f(0.13, 1, 0)
        draw_text(420, 400, "CONGRATULATIONS! YOU FOUND THE TREASURE!!!")
        draw_text(430, 380, f"Final Score: {score}")

        # Show Game Over
    elif game_over and not game_win:
        glColor3f(0.13, 1, 0)
        draw_text(430, 400, "GAME OVER!")
        draw_text(430, 380, f"Final Score: {score}")


    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Maze")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animation)  # Register the idle function to move the bullet automatically
    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
