from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import time
import random


small_c = {'x': 0, 'y': 0, 'r': 5, 'active': False}
small_l = {'x0': 0, 'y0': 0, 'x1': 0, 'y1': 0, 'active': False}
start_t = time.time()
game_duration = 1 * 20
width, height = 800, 600
pause = False
game_over = False
winner = None
puck = {'x': 0, 'y': 0, 'dx': 6, 'dy': 6, 'r': 10}
puck_flag = 0
mallet1 = {'x': -360, 'y': 0, 'r': 20}
mallet2 = {'x': 360, 'y': 0, 'r': 20}
scores = {'player1': 0, 'player2': 0}
circle_thickness = 1


def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def convert_to_zero(zone, x0, y0):
    if zone == 0:
        return x0, y0
    elif zone == 1:
        return y0, x0
    elif zone == 2:
        return y0, -x0
    elif zone == 3:
        return -x0, y0
    elif zone == 4:
        return -x0, -y0
    elif zone == 5:
        return -y0, -x0
    elif zone == 6:
        return -y0, x0
    elif zone == 7:
        return x0, -y0


def convert_to_origin(zone, x0, y0):
    x, y = 0, 0
    if zone == 1:
        x, y = y0, x0
    elif zone == 2:
        x, y = -y0, x0
    elif zone == 3:
        x, y = -x0, y0
    elif zone == 4:
        x, y = -x0, -y0
    elif zone == 5:
        x, y = -y0, -x0
    elif zone == 6:
        x, y = y0, -x0
    elif zone == 7:
        x, y = x0, -y0
    return int(x), int(y)


def zone_find(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy > 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    return zone


def mpl(x0, y0, x1, y1):
    zone = zone_find(x0, y0, x1, y1)
    x0, y0 = convert_to_zero(zone, x0, y0)
    x1, y1 = convert_to_zero(zone, x1, y1)

    dx = x1 - x0
    dy = y1 - y0
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    di_nit = 2 * dy - dx

    while x0 <= x1:
        if di_nit >= 0:
            di_nit += dne
            x0 += 1
            y0 += 1
        else:
            di_nit += de
            x0 += 1

        a, b = convert_to_origin(zone, x0, y0)
        draw_point(a, b)


def draw_circle(cx, cy, r, thickness=1):
    x = 0
    y = r
    d = 1 - r
    for r in range(r, r - thickness, -1):
        mcl(cx, cy, r)


def mcl(x0, y0, r):
    x, y = r, 0
    d = 1 - r
    draw_point(x + x0, y + y0)
    while y <= x:
        dn = ((2 * y) + 3)
        dnw = ((2 * y) - (2 * x) + 5)
        if d < 0:
            d += dn
            y += 1
        else:
            d += dnw
            y += 1
            x -= 1

        draw_point(x + x0, y + y0)
        draw_point(-x + x0, y + y0)
        draw_point(-x + x0, -y + y0)
        draw_point(x + x0, -y + y0)
        draw_point(y + x0, x + y0)
        draw_point(-y + x0, x + y0)
        draw_point(-y + x0, -x + y0)
        draw_point(y + x0, -x + y0)


def button_pause():
    glColor3f(1.0, 1.0, 0.0)
    mpl(-10, -290, -10, -270)
    mpl(10, -290, 10, -270)


def button_play():
    glColor3f(0.0, 1.0, 0.0)
    mpl(-11, -290, -11, -265)
    mpl(10, -277, -10, -290)
    mpl(10, -277, -10, -265)


def button_cancel():
    glColor3f(1.0, 0.0, 0.0)
    mpl(370, -290, 390, -270)
    mpl(390, -290, 370, -270)


def button_restart():
    glColor3f(0.0, 0.0, 1.0)
    mpl(-370, -285, -390, -285)
    mpl(-383, -295, -390, -285)
    mpl(-392, -285, -383, -275)


def draw_field():
    glColor3f(1, 1, 1)
    glPointSize(3)

    # top and bottom borders
    mpl(400, -260, -400, -260)
    mpl(400, 260, -400, 260)

    # left and right borders
    mpl(-400, 260, -400, 40)
    mpl(-400, -260, -400, -40)
    mpl(400, -260, 400, -40)
    mpl(400, 260, 400, 40)

    # mid line
    mpl(00, 259, 00, -259)

    mcl(0, 0, 75)  # mid field circle
    mcl(-400, 0, 95)  # goal d box left
    mcl(400, 0, 95)  # goal d box right

    if small_c['active']:
        glColor3f(1, 0, 0)
        draw_circle(small_c['x'], small_c['y'], small_c['r'])
    if small_l['active']:
        glColor3f(0, 1, 0)
        mpl(small_l['x0'], small_l['y0'], small_l['x1'], small_l['y1'])


key_states = {}


def keyboard(key, x, y):
    global key_states
    key_states[key] = True


def keyboard_up(key, x, y):
    global key_states
    if key in key_states:
        key_states[key] = False


def update(value):
    global puck, puck_flag, game_over, winner, start_t, small_c,  mallet1, mallet2

    if pause:
        glutTimerFunc(32, update, 0)
        return

    mallet_speed = 10
    # player 1
    if b'w' in key_states and key_states[b'w']:
        mallet1['y'] = min(mallet1['y'] + mallet_speed, 260 - mallet1['r'])
    if b's' in key_states and key_states[b's']:
        mallet1['y'] = max(mallet1['y'] - mallet_speed, -260 + mallet1['r'])
    if b'a' in key_states and key_states[b'a']:
        mallet1['x'] = max(mallet1['x'] - mallet_speed, -400 + mallet1['r'])
    if b'd' in key_states and key_states[b'd']:
        mallet1['x'] = min(mallet1['x'] + mallet_speed, 0 - mallet1['r'])

    # Player 2 movements
    if b'i' in key_states and key_states[b'i']:
        mallet2['y'] = min(mallet2['y'] + mallet_speed, 260 - mallet2['r'])
    if b'k' in key_states and key_states[b'k']:
        mallet2['y'] = max(mallet2['y'] - mallet_speed, -260 + mallet2['r'])
    if b'j' in key_states and key_states[b'j']:
        mallet2['x'] = max(mallet2['x'] - mallet_speed, 0 + mallet2['r'])
    if b'l' in key_states and key_states[b'l']:
        mallet2['x'] = min(mallet2['x'] + mallet_speed, 400 - mallet2['r'])

    elapsed_time = time.time() - start_t
    if elapsed_time >= game_duration and not game_over:
        game_over = True
        if scores['player1'] > scores['player2']:
            winner = 'Player 1'
        elif scores['player1'] < scores['player2']:
            winner = 'Player 2'
        else:
            winner = 'Draw'
        return

    if not small_c['active'] and elapsed_time >= game_duration / 2:
        small_c['x'] = random.randint(-200, 200)
        small_c['y'] = random.randint(-100, 100)
        small_c['r'] = random.randint(5, 15)
        small_c['active'] = True

    if not small_l['active'] and elapsed_time >= game_duration / 2:

        small_l['x0'] = random.randint(-200, 200)
        small_l['y0'] = random.randint(-100, 100)
        small_l['x1'] = random.randint(5, 15)
        small_l['y1'] = random.randint(5, 15)
        small_l['active'] = True

    if small_c['active']:
        dx = puck['x'] - small_c['x']
        dy = puck['y'] - small_c['y']
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < puck['r'] + small_c['r']:
            small_c['active'] = False
            random_ability()

    if not small_l['active'] and elapsed_time >= game_duration / 2:
        small_l['x0'] = random.randint(-200, 200)
        small_l['y0'] = random.randint(-100, 100)
        small_l['x1'] = small_l['x0'] + random.randint(-50, 50)
        small_l['y1'] = small_l['y0'] + random.randint(-50, 50)
        small_l['active'] = True

    if small_l['active']:
        x0, y0 = small_l['x0'], small_l['y0']
        x1, y1 = small_l['x1'], small_l['y1']

        px, py = puck['x'], puck['y']
        dx, dy = puck['dx'], puck['dy']

        line_length = (x1 - x0) ** 2 + (y1 - y0) ** 2
        if line_length == 0:
            line_length = 1

        t = max(0, min(1, ((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / line_length))
        c_x = x0 + t * (x1 - x0)
        c_y = y0 + t * (y1 - y0)

        dist = (px - c_x) ** 2 + (py - c_y) ** 2

        if dist < puck['r'] ** 2:
            norm_x = px - c_x
            norm_y = py - c_y
            norm_length = (norm_x ** 2 + norm_y ** 2) ** 0.5
            if norm_length != 0:
                norm_x /= norm_length
                norm_y /= norm_length

            dot = dx * norm_x + dy * norm_y
            puck['dx'] -= 2 * dot * norm_x
            puck['dy'] -= 2 * dot * norm_y

    puck['x'] += puck['dx']
    puck['y'] += puck['dy']

    if puck['y'] + puck['r'] > 260 or puck['y'] - puck['r'] < -260:
        puck['dy'] *= -1
    if puck['x'] + puck['r'] > 400 or puck['x'] - puck['r'] < -400:
        puck['dx'] *= -1

    for mallet in [mallet1, mallet2]:
        dx = puck['x'] - mallet['x']
        dy = puck['y'] - mallet['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        total_r = puck['r'] + mallet['r']

        if distance < total_r:
            col_norm_x = dx / distance
            col_norm_y = dy / distance
            rel_vel_x = puck['dx']
            rel_vel_y = puck['dy']

            velocity_along_normal = (rel_vel_x * col_norm_x + rel_vel_y * col_norm_y)
            puck['dx'] -= 2 * velocity_along_normal * col_norm_x
            puck['dy'] -= 2 * velocity_along_normal * col_norm_y

            overlap = total_r - distance
            puck['x'] += col_norm_x * overlap
            puck['y'] += col_norm_y * overlap

    if puck['x'] - puck['r'] < -400 and -35 < puck['y'] < 35:
        scores['player2'] += 1
        puck_flag += 1
        reset_puck()

    elif puck['x'] + puck['r'] > 400 and -35 < puck['y'] < 35:
        scores['player1'] += 1
        puck_flag += 1
        reset_puck()
    glutPostRedisplay()
    glutTimerFunc(32, update, 0)


def random_ability():
    global puck
    effects = ["increase_speed", "decrease_speed", "increase_size", "decrease_size"]
    selected_effect = random.choice(effects)

    if selected_effect == "increase_speed":
        puck['dx'] *= 1.3
        puck['dy'] *= 1.3
    elif selected_effect == "decrease_speed":
        puck['dx'] *= 0.3
        puck['dy'] *= 0.3
    elif selected_effect == "increase_size":
        puck['r'] = min(puck['r'] + 5, 30)
    elif selected_effect == "decrease_size":
        puck['r'] = max(puck['r'] - 5, 5)


def reset_puck():
    global puck_flag, puck
    puck['x'], puck['y'] = 0, 0
    if puck_flag == 0:
        puck['dx'], puck['dy'] = 6, 6
    elif puck_flag == 1:
        puck['dx'], puck['dy'] = -6, 6
    elif puck_flag == 2:
        puck['dx'], puck['dy'] = 6, -6
    elif puck_flag == 3:
        puck['dx'], puck['dy'] = -6, -6
    if puck_flag == 3:
        puck_flag = 0


def mouseListener(button, state, x, y):
    global pause, game_over, puck, puck_flag, mallet1, mallet2, scores, circle_thickness, start_t, small_c

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 370 <= x <= 430 and 550 <= y <= 590:
            if game_over == False and pause == False:
                pause = True
            else:
                pause = False

        elif 0 <= x <= 50 and 550 <= y <= 590:
            if game_over == True:
                game_over = False
            pause = False
            puck = {'x': 0, 'y': 0, 'dx': 6, 'dy': 6, 'r': 10}
            puck_flag = 0
            mallet1 = {'x': -360, 'y': 0, 'r': 20}
            mallet2 = {'x': 360, 'y': 0, 'r': 20}
            scores = {'player1': 0, 'player2': 0}
            small_c = {'x': 0, 'y': 0, 'r': 5, 'active': False}
            circle_thickness = 1
            start_t = time.time()

        elif 740 <= x <= 800 and 550 <= y <= 590:
            game_over = True
            glutLeaveMainLoop()
    glutPostRedisplay()


def display_scores():
    glColor3f(1, 1, 1)
    glRasterPos2f(-20, 270)
    for char in f"{scores['player1']} - {scores['player2']}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def display_time():
    elapsed_time = time.time() - start_t
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    glColor3f(1, 1, 1)
    glRasterPos2f(-400, 270)

    time_text = f"{minutes:02}:{seconds:02}"
    for char in time_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    if elapsed_time >= game_duration:
        glColor3f(1, 0, 0)
        glRasterPos2f(100, 0)
        for char in "Game Over":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glColor3f(1, 1, 1)
        glRasterPos2f(100, -30)
        score_text = f"Player 1: {scores['player1']} | Player 2: {scores['player2']}"
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glRasterPos2f(100, -60)
        if winner == 'Draw':
            winner_text = "It's a Draw!"
        else:
            winner_text = f"Winner: {winner}"
        for char in winner_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glutPostRedisplay()


def initialize():
    global width, height
    glViewport(0, 0, width, height)
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -300, 300, 0, 1)


def display():
    global pause
    glClear(GL_COLOR_BUFFER_BIT)
    initialize()
    draw_field()
    glColor3f(1, 0, 0)
    draw_circle(mallet1['x'], mallet1['y'], mallet1['r'], thickness=circle_thickness)
    glColor3f(0, 0, 1)
    draw_circle(mallet2['x'], mallet2['y'], mallet2['r'], thickness=circle_thickness)
    glColor3f(1, 1, 0)
    draw_circle(puck['x'], puck['y'], puck['r'], thickness=circle_thickness)
    display_scores()
    display_time()
    if pause == True:
        button_play()
    else:
        button_pause()
    button_cancel()
    button_restart()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Air Hockey Game")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_up)
glutMouseFunc(mouseListener)
glutTimerFunc(32, update, 0)
glutMainLoop()
