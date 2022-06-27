import pygame as p
import sys
import random
import math
import time
from pygame import mixer

# initialise mixer
p.mixer.pre_init(44100, -16, 1, 512)
p.init()


# main screen
main_screen = p.display.set_mode((500, 500))
p.display.set_caption("X-GAMER!")
clock = p.time.Clock()
game_font = p.font.Font('04B_19.ttf', 30)


# flappy bird global variables
gravity = 0.25
bird_move = 0
game_active = True
score = 0
high_score = 0
score_sound_cd = 100
paused = False
game_over = False

main_surface = p.image.load('assets/D.png').convert()
main_surface = p.transform.scale2x(main_surface)
bg_surface = p.image.load('assets/background-day.png').convert()
bg_surface = p.transform.scale2x(bg_surface)
floor_surface = p.image.load('assets/base.png').convert()
floor_surface = p.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = p.transform.scale2x(p.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = p.transform.scale2x(p.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = p.transform.scale2x(p.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 265))

pipe_surface = p.image.load('assets/pipe-green.png').convert()
pipe_surface = p.transform.scale2x(pipe_surface)
pipe_list = []

game_over_screen = p.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_screen.get_rect(center=(238, 300))

flap_sound = p.mixer.Sound('sound/sfx_wing.wav')
death_sound = p.mixer.Sound('sound/sfx_hit.wav')
score_sound = p.mixer.Sound('sound/sfx_point.wav')


# flappy Bird functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 560))
    screen.blit(floor_surface, (floor_x_pos + 476, 560))


def create_pipe(pipe_height):
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe - 230))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 684:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = p.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -25 or bird_rect.bottom >= 560:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = p.transform.rotozoom(bird, -bird_move * 2, 1)
    return new_bird


def bird_ani():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_disp(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(238, 50))
        screen.blit(score_surface, score_rect)

    if game_state == 'end_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(238, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(238, 500))
        screen.blit(high_score_surface, high_score_rect)
        continue_surface = game_font.render(str('PRESS SPACE TO RE-PLAY'), True, (0, 0, 0))
        continue_surface_rect = continue_surface.get_rect(center=(230, 380))
        screen.blit(continue_surface, continue_surface_rect)
        main_return_surface = game_font.render(str('PRESS M FOR MAIN MENU'), True, (0, 0, 0))
        main_return_surface_rect = main_return_surface.get_rect(center=(230, 420))
        screen.blit(main_return_surface, main_return_surface_rect)


def update_score(score, high_score):
    if (score > high_score):
        high_score = score
    return high_score


# ---------------SPACE INVADER ------------------ #

# VARIABLES


# game active variable
i_game_active = True
in_game = True
over = False
i_enemies = True



# player spaceship
player_img = p.image.load('assets/space-ship1.png')
player_imgX = 318
player_imgY = 400
player_imgX_change = 0

# enemy spaceships
enemy_img = []
enemy_imgX = []
enemy_imgY = []
enemy_imgX_change = []
enemy_imgY_change = []
enemies = 4
for i in range(enemies):
    enemy_img.append(p.image.load('assets/ufo.png'))
    enemy_imgX.append(random.randint(0, 636))
    enemy_imgY.append(random.randint(40, 200))
    enemy_imgX_change.append(2.5)
    enemy_imgY_change.append(50)

# bullet
bullet_img = p.image.load('assets/bullet_1.png')
bullet_imgX = 318
bullet_imgY = 400
bullet_imgX_change = 0
bullet_imgY_change = -4
bullet_state = "ready"

# score
score_val = 0
font = p.font.Font("04B_19.ttf", 20)
scoreX = 10
scoreY = 10

# high score
high_score_val = 0
font_1 = p.font.Font("04B_19.ttf", 20)
high_scoreX = 545
high_scoreY = 10

# game over
game_over_font = p.font.Font("04B_19.ttf", 32)
game_overX = 250
game_overY = 200

# FUNCTIONS

def player(x, y):
    window.blit(player_img, (int(x), int(y)))


def enemy(x, y, i):
    window.blit(enemy_img[i], (int(x), int(y)))


def bullet(x, y):
    global bullet_imgX
    window.blit(bullet_img, (int(x + 16.5), int(y + 10)))


def collision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    if distance < 40:
        return True


def i_score(x, y):
    score = font.render("SCORE : " + str(score_val), True, (255, 255, 255))
    window.blit(score, (x, y))


def update_high_score(score_val, high_score_val):
    if score_val > high_score_val:  # a is current score
        high_score_val = score_val
    return high_score_val


def i_high_score():
    high_score = font_1.render("HIGH SCORE : " + str(high_score_val), True, (255, 255, 255))
    window.blit(high_score, (high_scoreX, high_scoreY))


def i_game_over():
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    window.blit(game_over, (game_overX, game_overY))


def i_main():
    main_menu = main_font.render("PRESS M FOR MAIN MENU", True, (255, 255, 255))
    window.blit(main_menu, (150, 280))


def i_replay():
    replay = replay_font.render("PRESS X TO REPLAY", True, (255, 255, 255))
    window.blit(replay, (150, 320))


# space invader function finished



# pause variables
pause_font = p.font.Font("04B_19.ttf", 32)
main_font = p.font.Font("04B_19.ttf", 32)
replay_font = p.font.Font("04B_19.ttf", 32)
# space invaders variables finished

#------------------MAMBA TRAIL --------------------


# cell variables
m_cell_size = 25
m_cell_num = 25
# game_active
m_game_active = True
m_game_over = False
g_over = False
m_font = p.font.Font('04B_19.ttf', 30)

# fruit
m_cell_x = random.randint(0, m_cell_num - 1)
m_cell_y = random.randint(0, m_cell_num - 1)
m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)

# snake
m_snake_position = [p.math.Vector2(6, 10), p.math.Vector2(5, 10), p.math.Vector2(4, 10)]
m_direction = (1, 0)

# high score
m_high_score_val = 0


# FUNCTIONS

def draw_fruit():
    m_fruit_rect = p.Rect(int(m_cell_x * m_cell_size), int(m_cell_y * m_cell_size), m_cell_size, m_cell_size)
    p.draw.rect(window, (238, 130, 238), m_fruit_rect) #(surface,color,rect to be placed)
    p.draw.rect(window, (0, 0, 0), m_fruit_rect, 2)


def draw_snake():
    for i in m_snake_position:
        m_snake_rect = p.Rect(int(i.x * m_cell_size), int(i.y * m_cell_size), m_cell_size, m_cell_size)
        p.draw.rect(window, (219, 112, 147), m_snake_rect)
        p.draw.rect(window, (0, 0, 0), m_snake_rect, 2)

m_wall_collision = mixer.Sound('sound/mixkit-falling-hit-on-gravel-756.wav')
def m_collision():
    if not 0 <= m_snake_position[0].y < m_cell_num or not 0 <= m_snake_position[0].x < m_cell_num:
        m_wall_collision.play(0)
        p.time.wait(int(m_wall_collision.get_length() * 1000))
        return False

    for i in m_snake_position[1:]:
        if i == m_snake_position[0]:
            m_wall_collision.play(0)
            p.time.wait(int(m_wall_collision.get_length() * 1000))
            return False

    return True


def m_score():
    global m_score_val
    m_score_val = len(m_snake_position) - 3
    m_score = str(m_score_val)
    m_score_surface = m_font.render(str('SCORE: ') + m_score, True, (0, 0, 0))
    window.blit(m_score_surface, (470, 30))


def update(m_score_val, m_high_score_val):
    if m_score_val > m_high_score_val:
        m_high_score_val = m_score_val

    return m_high_score_val


def m_high_score(m_high_score_val):
    m_high_score_surface = m_font.render(str('HIGH SCORE: ') + str(m_high_score_val), True, (0, 0, 0))
    window.blit(m_high_score_surface, (20, 30))


# COMMON FUNCTIONS

def pause(game_state, x):
    paused = True
    if x == 1:
        while paused:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    quit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_c:
                        paused = False
                    elif event.key == p.K_q:
                        p.quit()
                        quit()
            if game_state == 'paused':
                pause_surface = game_font.render(str('PAUSED!!'), True, (0, 0, 0))
                pause_rect = pause_surface.get_rect(center=(238, 200))
                screen.blit(pause_surface, pause_rect)
                pause_surface_1 = game_font.render(str('PRESS C TO CONTINUE'), True, (0, 0, 0))
                pause_rect_1 = pause_surface_1.get_rect(center=(238, 300))
                screen.blit(pause_surface_1, pause_rect_1)
                pause_surface_2 = game_font.render(str('PRESS Q TO QUIT'), True, (0, 0, 0))
                pause_rect_2 = pause_surface_2.get_rect(center=(238, 400))
                screen.blit(pause_surface_2, pause_rect_2)
                p.display.update()
                clock.tick(50)
    if x == 2:
        paused = True
        while paused:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    quit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_c:
                        paused = False
                    elif event.key == p.K_q:
                        p.quit()
                        quit()
            if game_state == 'paused':
                pause_surface = pause_font.render(str('PAUSED!!'), True, (255, 255, 255))

                window.blit(pause_surface, (280, 110))
                pause_surface_1 = pause_font.render(str('PRESS C TO CONTINUE'), True, (255, 255, 255))
                window.blit(pause_surface_1, (205, 210))
                pause_surface_2 = pause_font.render(str('PRESS Q TO QUIT'), True, (255, 255, 255))
                window.blit(pause_surface_2, (245, 310))
                p.display.update()

    if x == 3:
        paused = True
        while paused:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    quit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_c:
                        paused = False
                    elif event.key == p.K_q:
                        p.quit()
                        quit()
            if game_state == 'paused':
                pause_surface = pause_font.render(str('PAUSED!!'), True, (0, 0, 0))
                window.blit(pause_surface, (240, 130))
                pause_surface_1 = pause_font.render(str('PRESS C TO CONTINUE'), True, (0, 0, 0))
                window.blit(pause_surface_1, (155, 230))
                pause_surface_2 = pause_font.render(str('PRESS Q TO QUIT'), True, (0, 0, 0))
                window.blit(pause_surface_2, (185, 330))
                p.display.update()
                clock.tick(50)




def loading(screen, x, y, id):
    i_load_img = p.image.load('assets/load_bck.jpg')
    i_bg_imageX = 0
    i_bg_imageY = 0
    screen.blit(i_load_img, (i_bg_imageX, i_bg_imageY))
    p.display.update()


    m_load_pause = m_font.render(str('PRESS P TO PAUSE GAME!!'), True, (255, 110 , 110))
    m_load_pause_rect = m_load_pause.get_rect(center=(x/2, (3*y)/5))
    if id==1:
        m_load_dir = m_font.render(str('PRESS SPACE TO FLY BIRD!!'), True, (250, 250, 70))
        m_load_dir_rect = m_load_dir.get_rect(center=(x/2, (4*y)/5))
    if id==2:
        m_load_dir = m_font.render(str('PRESS SPACE TO SHOOT!!'), True, (250, 250, 70))
        m_load_dir_rect = m_load_dir.get_rect(center=(x / 2, (4*y) / 5))

    if id==3:
        m_load_dir = m_font.render(str('PRESS ARROW KEYS TO MOVE SNAKE!!'), True, (250, 250, 70))
        m_load_dir_rect = m_load_dir.get_rect(center=(x / 2, (4*y) / 5))

    m_load = m_font.render(str('3'), True, (35, 250, 200))
    m_load_rect = m_load.get_rect(center=(x/2,(y)/5))
    screen.blit(m_load, m_load_rect)
    screen.blit(m_load_pause, m_load_pause_rect)
    screen.blit(m_load_dir, m_load_dir_rect)
    p.display.update()
    time.sleep(1)


    screen = p.display.set_mode((x,y))
    i_load_img = p.image.load('assets/load_bck.jpg')
    screen.blit(i_load_img, (i_bg_imageX, i_bg_imageX))
    p.display.update()

    m_load = m_font.render(str('2'), True, (35, 250, 200))
    m_load_rect = m_load.get_rect(center=(x / 2, ( y) / 5))
    screen.blit(m_load, m_load_rect)
    screen.blit(m_load_pause, m_load_pause_rect)
    screen.blit(m_load_dir, m_load_dir_rect)
    p.display.update()
    time.sleep(1)

    screen = p.display.set_mode((x,y))
    screen.blit(i_load_img, (i_bg_imageX, i_bg_imageX))
    p.display.update()

    m_load = m_font.render(str('1'), True, (35, 250, 200))
    m_load_rect = m_load.get_rect(center=(x / 2, (y) / 5))
    screen.blit(m_load, m_load_rect)
    screen.blit(m_load_pause, m_load_pause_rect)
    screen.blit(m_load_dir, m_load_dir_rect)
    p.display.update()
    time.sleep(2)


#MAIN CODE

while True:
    for main_event in p.event.get():
        if main_event.type == p.QUIT:
            p.quit()
            sys.exit()
        if main_event.type == p.KEYDOWN:
            if main_event.key == p.K_f:  # flappy_bird
                screen = p.display.set_mode((476, 684))
                p.display.set_caption("Flappy Bird!")
                f_icon_img = p.image.load('assets/flappy-bird-icon.png')  # icon of the game window
                p.display.set_icon(f_icon_img)

                loading(screen, 476, 684,1)
                SPAWNPIPE = p.USEREVENT
                p.time.set_timer(SPAWNPIPE, 1100)
                BIRDFLAP = p.USEREVENT + 1
                p.time.set_timer(BIRDFLAP, 300)
                pipe_height = [280, 400, 350, 450]

                while not game_over:
                    for event in p.event.get():
                        if event.type == p.QUIT:
                            p.quit()
                            sys.exit()
                        if event.type == p.KEYDOWN:
                            if event.key == p.K_SPACE:
                                bird_move = 0
                                bird_move -= 7
                                flap_sound.play()
                            if event.key == p.K_SPACE and game_active == False:
                                game_active = True
                                pipe_list.clear()
                                bird_move = 0
                                bird_rect.center = (50, 265)
                                score = 0
                            if event.key == p.K_p:
                                pause('paused', 1)              #Z

                            if event.key == p.K_m and game_active == False:
                                game_over = True
                                pipe_list.clear()
                                bird_move = 0
                                bird_rect.center = (50, 265)
                                score = 0
                                break

                        if event.type == SPAWNPIPE:
                            pipe_list.extend(create_pipe(pipe_height))

                        if event.type == BIRDFLAP:
                            bird_index = (bird_index + 1) % 3
                            bird_surface, bird_rect = bird_ani()
                    # background
                    screen.blit(bg_surface, (0, -310))
                    if game_active:

                        # Bird movement
                        bird_move += gravity
                        rotated_bird = rotate_bird(bird_surface)
                        bird_rect.centery = int(bird_rect.centery+bird_move)
                        screen.blit(rotated_bird, bird_rect)
                        game_active = check_collisions(pipe_list)

                        # pipes
                        pipe_list = move_pipe(pipe_list)
                        draw_pipes(pipe_list)
                        score += 0.01
                        score_disp('main_game')
                        score_sound_cd -= 1  # defined a variable score_sound_cd and initialised as 100
                        if score_sound_cd == 0:
                            score_sound.play()
                            score_sound_cd = 100
                    else:
                        screen.blit(game_over_screen, game_over_rect)
                        high_score = update_score(score, high_score)
                        score_disp('end_game')
                    # floor
                    floor_x_pos -= 1
                    draw_floor()
                    if floor_x_pos <= -476:
                        floor_x_pos = 0
                    p.display.update()
                    clock.tick(120)

            if main_event.key == p.K_s:  # space invaders
                window = p.display.set_mode((700, 500))
                p.display.set_caption("Space Invaders!")
                icon_img = p.image.load('assets/icon.png')  # icon of the game window
                p.display.set_icon(icon_img)
                mixer.music.load('sound/background-audio.wav')
                mixer.music.play()

                p.mixer.music.set_volume(100)
                i_clock = p.time.Clock()

                loading(window,700, 500,2)

                run = True
                while run:
                    for event in p.event.get():
                        if event.type == p.QUIT:
                            run = False
                        if event.type == p.KEYDOWN:
                            if event.key == p.K_m and in_game == False:
                                i_game_active = False
                                in_game = True
                                over = False
                                i_enemies = True
                                score_val = 0
                                run = False
                                break

                            if event.key == p.K_x and in_game == False:
                                i_game_active = True
                                in_game = True
                                over = False
                                i_enemies = True
                                score_val = 0

                        if i_game_active:
                            if event.type == p.KEYDOWN:
                                if event.key == p.K_LEFT:
                                    player_imgX_change = -3.0
                                if event.key == p.K_RIGHT:
                                    player_imgX_change = +3.0
                                if event.key == p.K_SPACE:
                                    bullet_sound = mixer.Sound('sound/bullet-sound.wav')
                                    bullet_sound.play()
                                    bullet_state = "fire"
                                    bullet_imgX = player_imgX
                                if event.key == p.K_p:
                                    pause('paused', 2) #P

                            if event.type == p.KEYUP:
                                if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                                    player_imgX_change = 0

                    i_bg_image = p.image.load('assets/bg1.png')
                    i_bg_imageX = 0
                    i_bg_imageY = 0
                    window.blit(i_bg_image, (i_bg_imageX, i_bg_imageY))

                    if i_game_active:
                        # BULLET
                        if in_game:

                            if bullet_state == "fire":
                                bullet(bullet_imgX, bullet_imgY)
                                bullet_imgY += bullet_imgY_change

                            if bullet_imgY <= 0:
                                bullet_imgY = 400
                                bullet_imgX = player_imgX
                                bullet_state = "ready"

                            # PLAYER
                            player_imgX += player_imgX_change

                            if player_imgX <= 0:
                                player_imgX = 0
                            elif player_imgX >= 636:
                                player_imgX = 636

                            player(player_imgX, player_imgY)

                            # ENEMY

                            for i in range(enemies):

                                # game over
                                if enemy_imgY[i] > 318:
                                    for j in range(enemies):
                                        enemy_imgY[j] = 1600
                                        in_game = False
                                        over = True

                                enemy_imgX[i] += enemy_imgX_change[i]

                                if enemy_imgX[i] <= 0:
                                    enemy_imgX_change[i] = +2.5
                                    enemy_imgY[i] += enemy_imgY_change[i]
                                elif enemy_imgX[i] >= 636:
                                    enemy_imgX_change[i] = -2.5
                                    enemy_imgY[i] += enemy_imgY_change[i]

                                # collision
                                is_collision = collision(enemy_imgX[i], enemy_imgY[i], bullet_imgX, bullet_imgY)
                                if is_collision:
                                    bullet_imgY = 400
                                    bullet_state = "ready"
                                    enemy_imgX[i] = random.randint(0, 636)
                                    enemy_imgY[i] = random.randint(40, 200)
                                    score_val += 1
                                    collision_sound = mixer.Sound('sound/explosion-sound.wav')
                                    collision_sound.play()

                                enemy(enemy_imgX[i], enemy_imgY[i], i)
                                i_score(scoreX, scoreY)
                                high_score_val = update_high_score(score_val, high_score_val)

                        if over:
                            i_game_over()
                            i_score(scoreX, scoreY)
                            i_high_score()
                            i_main()  #
                            i_replay()
                            enemy_imgY.clear()
                            for i in range(enemies):
                                enemy_imgY.append(random.randint(40, 200))

                    p.display.update()
                    i_clock.tick(120)

            if main_event.key == p.K_a:
                window = p.display.set_mode((m_cell_num * m_cell_size, m_cell_num * m_cell_size))
                p.display.set_caption("Mamba Trail!")
                m_icon_img = p.image.load('assets/snake_icon.jpeg')  # icon of the game window
                p.display.set_icon(m_icon_img)
                m_snake_clock = p.time.Clock()
                loading(window,m_cell_num * m_cell_size,m_cell_num * m_cell_size,3)
                SCREEN_UPDATE =p.USEREVENT
                window.fill((85, 107, 47))
                p.time.set_timer(SCREEN_UPDATE, 100)
                m_game_over = False
                m_game_active = True
                running = True

                run = True
                while run:
                    for event in p.event.get():
                        if event.type == p.QUIT:
                            run = False

                        if event.type == p.USEREVENT and running:
                            window.fill((85, 107, 47))
                            m_snake_position_copy = m_snake_position[:-1]#slicing and eliminating last element
                            m_snake_position_copy.insert(0, m_snake_position_copy[0] + m_direction) #(index,value)
                            m_snake_position = m_snake_position_copy[:]
                        if event.type == p.KEYDOWN:
                            if event.key == p.K_UP:
                                if m_direction[1] != 1:
                                    m_direction = (0, -1)
                            if event.key == p.K_DOWN:
                                if m_direction[1] != -1:
                                    m_direction = (0, +1)
                            if event.key == p.K_LEFT:
                                if m_direction[0] != 1:
                                    m_direction = (-1, 0)
                            if event.key == p.K_RIGHT:
                                if m_direction[0] != -1:
                                    m_direction = (+1, 0)
                            if event.key == p.K_p:
                                pause('paused', 3) #P
                            if event.key == p.K_r and m_game_over == True:
                                print("xyz")
                                m_cell_x = random.randint(0, m_cell_num - 1)
                                m_cell_y = random.randint(0, m_cell_num - 1)
                                m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)
                                m_snake_position = [p.math.Vector2(6, 10), p.math.Vector2(5, 10),
                                                    p.math.Vector2(4, 10)]
                                m_direction = (1, 0)
                                if m_cell_position == m_snake_position[1:]:
                                    m_cell_x = random.randint(0, m_cell_num - 1)
                                    m_cell_y = random.randint(0, m_cell_num - 1)
                                    m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)
                                m_game_active = True
                                m_game_over = False
                                running = True
                                window.fill((85, 107, 47))
                            if event.key == p.K_q and m_game_over == True:
                                p.quit()
                                sys.exit()
                            if event.key == p.K_m and m_game_over == True:
                                run = False
                                running = False
                                m_game_active = False
                                m_cell_x = random.randint(0, m_cell_num - 1)
                                m_cell_y = random.randint(0, m_cell_num - 1)
                                m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)
                                m_snake_position = [p.math.Vector2(6, 10), p.math.Vector2(5, 10),
                                                    p.math.Vector2(4, 10)]
                                m_direction = (1, 0)
                                if m_cell_position == m_snake_position[1:]:
                                    m_cell_x = random.randint(0, m_cell_num - 1)
                                    m_cell_y = random.randint(0, m_cell_num - 1)
                                    m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)
                                break

                    if running :
                        if m_game_active:
                            draw_fruit()
                            draw_snake()
                            m_score()
                            m_high_score_val = update(m_score_val, m_high_score_val)
                            # m_high_score(m_high_score_val)
                            if m_cell_position == m_snake_position[0]:
                                # the fruit changes its position
                                m_cell_x = random.randint(0, m_cell_num - 1)
                                m_cell_y = random.randint(0, m_cell_num - 1)
                                m_cell_position = p.math.Vector2(m_cell_x, m_cell_y)
                                # the length of the snake increases.
                                m_snake_position_copy = m_snake_position[:]
                                m_snake_position_copy.insert(0, m_snake_position_copy[0] + m_direction)
                                m_snake_position = m_snake_position_copy[:]
                                # the sound
                                m_fruit_collision = mixer.Sound('sound/collision-sound.wav')
                                m_fruit_collision.play()
                            else:
                                m_game_active= m_collision()
                                m_game_over = not(m_game_active)

                        if m_game_over:
                            #fill window and display sound
                            window.fill((85, 107, 47))
                            print("Hi")
                            m_over_surface = m_font.render(str('GAME OVER!'), True, (0, 0, 0))
                            window.blit(m_over_surface, (240, 100))
                            m_over_surface_1 = m_font.render(str('PRESS \'R\' TO RESTART.'), True, (0, 0, 0))
                            window.blit(m_over_surface_1, (170, 250))
                            m_over_surface_2 = m_font.render(str('PRESS \'Q\' TO QUIT.'), True, (0, 0, 0))
                            window.blit(m_over_surface_2, (170, 350))
                            m_over_surface_3 = m_font.render(str('PRESS \'M\' FOR MAIN MENU.'), True, (0, 0, 0))
                            window.blit(m_over_surface_3, (170, 450))
                            update(m_score_val, m_high_score_val)
                            m_score()
                            m_high_score(m_high_score_val)
                            p.display.update()
                            running= False
                            m_game_over= True

                    p.display.update()
                    m_snake_clock.tick(70)

    main_screen = p.display.set_mode((500, 500))
    p.display.set_caption("X-GAMER!")
    x_icon_img = p.image.load('assets/X-GAMER-logos.jpeg')
    p.display.set_icon(x_icon_img)
    main_screen.blit(main_surface, (0, 0))
    m_game_active = True
    game_over = False
    game_active = True
    i_game_active = True
    in_game = True
    over = False
    p.mixer.music.set_volume(0)
    p.display.update()
    clock.tick(120)
