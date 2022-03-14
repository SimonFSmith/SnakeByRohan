author = 'Rohan Das'
collaborater = 'Simon Fournier-Smith'

# importing modules
import pygame
import random
import os
from tkinter import messagebox

# pygame initialization
pygame.mixer.init()
pygame.init()

# colors
red_color = (255, 0, 0)
black_color = (0, 0, 0)
snakegreen_color = (35, 45, 40)

# game backgrounds
main_background = pygame.image.load("screen_backgrounds/main_background.jpg")
intro_background = pygame.image.load("screen_backgrounds/intro_background.png")
outro_background = pygame.image.load("screen_backgrounds/outro_background.png")

# creating game window
screen_width = 900
screen_height = 600
game_window = pygame.display.set_mode((screen_width, screen_height))

# game title
pygame.display.set_caption("Snake By Rohan")
pygame.display.update()

# music initialization
pygame.mixer.music.load('music/intro_music.mp3')
pygame.mixer.music.play(100)
pygame.mixer.music.set_volume(.6)

# game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)
name_input_font = pygame.font.SysFont('Harrington', 20)


# display text on screen
def display_text(text, color, x, y):
   screen_text = font.render(text, True, color)
   game_window.blit(screen_text, [x, y])


# display the snake on screen
def plot_snake(game_window, color, snake_list, snake_size):
   for x,y in snake_list:
       pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


# show welcome screen
def show_welcome():
    exit_game = False

    # name box initialization
    input_box = pygame.Rect(300, 303, 300, 32)
    active = False
    name_input = ''

    while not exit_game:
        game_window.blit(intro_background, (0,0))

        # let player enter its name and put it in name_imput variable
        display_text("Enter your name in the box below", black_color, 200, 260)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
            if event.type == pygame.KEYDOWN:
                if active and event.key != pygame.K_RETURN:
                        if event.key == pygame.K_BACKSPACE:
                            name_input = name_input[:-1]
                        else:
                            name_input += event.unicode

            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if player entered its name
                    if name_input == '':
                        messagebox.showinfo('No name entered', "You must enter a name to keep track of your highscore.\nClick inside the rectangle on the welcome page and enter your name if you want to play.")
                        show_welcome()
                        quit()
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('music/main_music.mp3')
                    pygame.mixer.music.play(100)
                    pygame.mixer.music.set_volume(.6)
                    game_loop(name_input)
        color = pygame.Color('lightskyblue3') if active else black_color
        txt_surface = name_input_font.render(name_input, True, black_color)
        game_window.blit(txt_surface, (input_box.x+10, input_box.y+3))
        pygame.draw.rect(game_window, color, input_box, 2)
        pygame.display.update()
        clock.tick(60)


# show game loop
def game_loop(name_input):
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1

    # highscore build
    file_name = "highscores/highscore_" + name_input + ".txt"
    if(not os.path.exists(file_name)):
        with open(file_name, "w") as f:
            f.write("0")
    with open(file_name, "r") as f:
            highscore = f.read()

    # food
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    # game variables
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open(file_name, "w") as f:
                f.write(str(highscore))
            # game over screen
            game_window.blit(outro_background, (0, 0))

            display_text(name_input, snakegreen_color, 135, 360)
            display_text("Your final score: " + str(score), snakegreen_color, 135, 410)
            display_text("Your highest score is: " + str(highscore), snakegreen_color, 135, 460)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        show_welcome()
        else:
            # game screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score +=10
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<12 and abs(snake_y - food_y)<12:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length +=5
                if score>int(highscore):
                    highscore = score
            game_window.blit(main_background, (0, 0))

            display_text("Player: " + name_input + "  Score: " + str(score) + "  Highscore: " + str(highscore), snakegreen_color, 5, 5)
            pygame.draw.rect(game_window, red_color, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('music/bgm1.mp3')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.6)
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('music/bgm2.mp3')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.6)
            plot_snake(game_window, black_color, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


show_welcome()
