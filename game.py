import sys

import json
import pygame
import random
import os

global current_song

pygame.init()
pygame.mixer.init()

# Stałe w grze
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 5 # 5=Easy
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = (0, 200   , 0)  # Zielony
FOOD_COLOR = (255, 0, 0)  # Czerwony
BACKGROUND_COLOR = (0, 100, 0)  # Ciemny zielony
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
BLUE = (100, 100, 255)
EYE_COLOR = (255, 255, 255)  # Biały
PUPIL_COLOR = (0, 0, 0)  # czarny
TONGUE_COLOR = (255, 0, 0)

#muzyka
music_folder = "resources/music"
point_sound = pygame.mixer.Sound("resources/score/f6-102819.mp3")

#Konfiguracja wyswietlacza
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Snake Game")

#czcionka
font = pygame.font.SysFont("Georgia", 40)

# zmienne gry
grass_positions = []
flowers_positions = []
difficulty = "Easy"
score = 0
direction = 'down'

#plik do zapisu najlepszego wyniku
SCORE_FILE = "resources/data/highscore.json"

clock = pygame.time.Clock()

def settings():
    global SPEED, SNAKE_COLOR, difficulty, start_screen_flag, grass_positions, flowers_positions,score, direction, snake, food, highest_score
    running = True
    while running:
        screen.fill((50, 50, 50))
        settings_text = font.render("Settings", True, WHITE)
        screen.blit(settings_text, (GAME_WIDTH / 2 - settings_text.get_width() / 2, 100))

        # Wyświetlanie aktualnej prędkości
        difficulty_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        screen.blit(difficulty_text, (GAME_WIDTH / 2 - difficulty_text.get_width() / 2, 200))

        # Wyświetlanie koloru węża
        color_text = font.render(f"Snake Color: {SNAKE_COLOR}(press c)", True, WHITE)
        screen.blit(color_text, (GAME_WIDTH / 2 - color_text.get_width() / 2, 250))

        # Zmiana utworu
        music_text = font.render("click 'M' to change song", True, WHITE)
        screen.blit(music_text, (GAME_WIDTH / 2 - music_text.get_width() / 2, 300))

        # Opcja powrotu do gry
        back_text = font.render("Press 'space' to resume", True, WHITE)
        screen.blit(back_text, (GAME_WIDTH / 2 - back_text.get_width() / 2, GAME_HEIGHT - 100))

        # Opcja restartu
        back_text = font.render("Press 'R' to restart", True, WHITE)
        screen.blit(back_text, (GAME_WIDTH / 2 - back_text.get_width() / 2, GAME_HEIGHT - 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
                elif event.key == pygame.K_c:  # Zmiana koloru węża na losowy
                    SNAKE_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif event.key == pygame.K_r: #restart gry
                    grass_positions = []
                    flowers_positions = []
                    difficulty = "Easy"
                    score = 0
                    direction = 'down'
                    return True
                elif event.key == pygame.K_m:
                    play_random_music()

        pygame.time.delay(100)

def initialize_grass():
    global grass_positions
    grass_positions = []
    for _ in range(100): # Ilosc trawy
        x = random.randint(0, GAME_WIDTH - SPACE_SIZE)
        y = random.randint(0, GAME_HEIGHT - SPACE_SIZE)
        width = random.randint(5, 10)  # Szerokość prostokąta trawy
        height = random.randint(10, 30)  # Wysokość prostokąta trawy
        color = (random.randint(0, 50), random.randint(150, 200), random.randint(0, 50)) #losowy odcien zielonego
        grass_positions.append((x, y, width, height, color))  # dodanie trawy

def initialize_flowers():
    global flowers_positions
    flowers_positions = []
    for _ in range(33):  # Liczba kwiatkow
        x = random.randint(0, GAME_WIDTH - SPACE_SIZE)
        y = random.randint(0, GAME_HEIGHT - SPACE_SIZE)
        size = random.randint(5, 10)
        color = (random.randint(150, 255), random.randint(0, 100), random.randint(150, 255))
        flowers_positions.append((x, y, size, color))

def draw_grass():
    for (x, y, width, height, color) in grass_positions:
        pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

def draw_flowers():
    for (x, y, size, color) in flowers_positions:
        pygame.draw.circle(screen, color, (x, y), size)

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[100, 100], [90, 100], [80, 100]]
        self.squares = []

    def move(self):
        x, y = self.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        #Dodanie nowej głowy węża na początek listy współrzędnych
        self.coordinates.insert(0, [x, y])

    def draw(self):
        #ciało
        for x, y in self.coordinates:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(x, y, SPACE_SIZE, SPACE_SIZE))

        #oczy
        self.draw_eyes(self.coordinates[0][0], self.coordinates[0][1], direction)

        #język
        self.draw_tongue(self.coordinates[0][0], self.coordinates[0][1])

    def draw_eyes(self, x, y, direction):
        eye_radius = 8  # promien oka
        eye_offset = 10  # dystans od srodka glowy
        if direction == "up" or direction == "down": #gdzie patrzy
            # lewe oko
            pygame.draw.circle(screen, EYE_COLOR, (x + SPACE_SIZE // 2 - eye_offset, y + SPACE_SIZE // 2), eye_radius)
            # prawe oko
            pygame.draw.circle(screen, EYE_COLOR, (x + SPACE_SIZE // 2 + eye_offset, y + SPACE_SIZE // 2), eye_radius)

            pupil_radius = 3
            pygame.draw.circle(screen, PUPIL_COLOR, (x + SPACE_SIZE // 2 - eye_offset, y + SPACE_SIZE // 2), pupil_radius)
            pygame.draw.circle(screen, PUPIL_COLOR, (x + SPACE_SIZE // 2 + eye_offset, y + SPACE_SIZE // 2), pupil_radius)
        else:
            pygame.draw.circle(screen, EYE_COLOR, (x + SPACE_SIZE // 2, y + SPACE_SIZE // 2 - eye_offset), eye_radius)
            pygame.draw.circle(screen, EYE_COLOR, (x + SPACE_SIZE // 2, y + SPACE_SIZE // 2 + eye_offset), eye_radius)

            pupil_radius = 3
            pygame.draw.circle(screen, PUPIL_COLOR, (x + SPACE_SIZE // 2, y + SPACE_SIZE // 2 - eye_offset), pupil_radius)
            pygame.draw.circle(screen, PUPIL_COLOR, (x + SPACE_SIZE // 2, y + SPACE_SIZE // 2 + eye_offset), pupil_radius)

    def draw_tongue(self, x, y):
        tongue_length = 20
        tongue_width = 5
        tongue_offset = 10

        if direction == 'up':
            pygame.draw.rect(screen, TONGUE_COLOR,
                             pygame.Rect(x + SPACE_SIZE // 2 - tongue_width // 2, y - tongue_offset, tongue_width,
                                         tongue_length))
        elif direction == 'down':
            pygame.draw.rect(screen, TONGUE_COLOR,
                             pygame.Rect(x + SPACE_SIZE // 2 - tongue_width // 2, y + SPACE_SIZE - tongue_offset,
                                         tongue_width, tongue_length))
        elif direction == 'left':
            pygame.draw.rect(screen, TONGUE_COLOR,
                             pygame.Rect(x - tongue_offset, y + SPACE_SIZE // 2 - tongue_width // 2, tongue_length,
                                         tongue_width))
        elif direction == 'right':
            pygame.draw.rect(screen, TONGUE_COLOR,
                             pygame.Rect(x + SPACE_SIZE - tongue_offset, y + SPACE_SIZE // 2 - tongue_width // 2,
                                         tongue_length, tongue_width))

    def check_collision(self):
        x, y = self.coordinates[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        for body_part in self.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    def grow(self):
        self.body_size += 1

    def remove_tail(self):
        del self.coordinates[-1]


class Food:
    def __init__(self):
        #losowanie koordynatów jablka
        self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

    def draw(self):
        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(self.x, self.y, SPACE_SIZE, SPACE_SIZE))

def game_over():
    font = pygame.font.SysFont("Impact", 40)
    running = True
    while running:
        screen.fill((50, 50, 50))

        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (GAME_WIDTH / 2 - game_over_text.get_width() / 2,
                                     GAME_HEIGHT / 2 - game_over_text.get_height() / 2))

        restart_text = font.render("click 'SPACE' to start again", True, (255, 0, 0))
        screen.blit(restart_text, (GAME_WIDTH / 2 - restart_text.get_width() / 2,
                                   GAME_HEIGHT / 2 - restart_text.get_height() / 2 + 40))

        exit_text = font.render("click 'ESCAPE' to exit", True, (255, 0, 0))
        screen.blit(exit_text, (GAME_WIDTH / 2 - exit_text.get_width() / 2,
                                   GAME_HEIGHT / 2 - exit_text.get_height() / 2 + 120))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_m:
                    play_random_music()



def get_music_files(folder):
    music_files = []
    for filename in os.listdir(folder):
        if filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".ogg"):
            music_files.append(os.path.join(folder, filename))
    return music_files

def play_random_music():
    global current_song
    music_files = get_music_files(music_folder)
    if music_files:
        random_music = random.choice(music_files)
        current_song = str(random_music)
        pygame.mixer.music.load(random_music)
        pygame.mixer.music.play(loops=-1)

def load_highest_score(SPEED):
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as file:
            scores = json.load(file)
            return scores.get(str(SPEED), 0)
    return 0


def save_highest_score(SPEED, score):
    scores = {}

    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as file:
            try:
                scores = json.load(file)
            except json.JSONDecodeError:
                scores = {}

    current_best = scores.get(str(SPEED), 0)
    if score > current_best:
        scores[str(SPEED)] = score
        with open(SCORE_FILE, 'w') as file:
            json.dump(scores, file)

def start_screen(screen):
    global difficulty, SPEED, SNAKE_COLOR
    LEVEL_COLOR = BLUE
    image = pygame.image.load("resources/screen/snake - menu screen.jpg")
    scaled_image = pygame.transform.scale(image, (800, 800))
    running = True
    while running:
        screen.fill((0, 10, 0))
        screen.blit(scaled_image, (0, -100))

        font = pygame.font.SysFont("Cosmos", 40)
        settings_text = font.render("Snake game by kamikaj", True, BLUE)
        screen.blit(settings_text, (GAME_WIDTH / 2 - settings_text.get_width() / 2, 100))

        font = pygame.font.SysFont("Cosmos", 33)
        # Wyświetlanie aktualnej prędkości
        difficulty_text = font.render(f"Difficulty Level: {difficulty} (use arrows to change it)", True, LEVEL_COLOR)
        screen.blit(difficulty_text, (GAME_WIDTH / 2 - difficulty_text.get_width() / 2, 200))

        # Wyświetlanie koloru węża
        color_text = font.render(f"Snake Color: {SNAKE_COLOR} (press c to change color randomly)", True, BLUE)
        screen.blit(color_text, (GAME_WIDTH / 2 - color_text.get_width() / 2, 250))

        # dodatkowe info
        info_text1 = font.render("Additional keys: ", True, BLUE)
        info_text = font.render("Press 'm' to change soundtrack ; Press 's' to go to settings", True, BLUE)
        screen.blit(info_text1, (GAME_WIDTH / 2 - info_text1.get_width() / 2, 300))
        screen.blit(info_text, (GAME_WIDTH / 2 - info_text.get_width() / 2, 350))

        # Opcja powrotu do gry
        back_text = font.render("Press 'SPACE' to start", True, YELLOW)
        screen.blit(back_text, (GAME_WIDTH / 2 - back_text.get_width() / 2, GAME_HEIGHT - 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_UP:
                    if difficulty == "Beginner":
                        difficulty = "Easy"
                        LEVEL_COLOR = BLUE
                        SPEED = 5
                    elif difficulty == "Easy":
                        difficulty = "Medium"
                        LEVEL_COLOR = YELLOW
                        SPEED = 7
                    elif difficulty == "Medium":
                        difficulty = "Hard"
                        LEVEL_COLOR = (255, 0, 0)
                        SPEED = 10
                    elif difficulty == "Hard":
                        difficulty = "Hardcore"
                        LEVEL_COLOR = (150, 0, 0)
                        SPEED = 13
                elif event.key == pygame.K_DOWN:
                    if difficulty == "Easy":
                        difficulty = "Beginner"
                        LEVEL_COLOR = SNAKE_COLOR
                        SPEED = 3
                    elif difficulty == "Medium":
                        difficulty = "Easy"
                        LEVEL_COLOR = BLUE
                        SPEED = 5
                    elif difficulty == "Hard":
                        difficulty = "Medium"
                        LEVEL_COLOR = YELLOW
                        SPEED = 7
                    elif difficulty == "Hardcore":
                        difficulty = "Hard"
                        LEVEL_COLOR = (255, 0, 0)
                        SPEED = 10
                elif event.key == pygame.K_c:  # Zmiana koloru węża na losowy
                        SNAKE_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif event.key == pygame.K_m:
                    play_random_music()
                elif event.key == pygame.K_s:
                    font = pygame.font.SysFont("Cosmos", 38)
                    settings_text = font.render("You can go to settings only when you are in the game", True, (255, 0, 0))
                    screen.blit(settings_text, (GAME_WIDTH / 2 - settings_text.get_width() / 2, 400))
                    pygame.display.update()
                    pygame.time.delay(1000)

        pygame.time.delay(100)


#Główna pętla
def main():
    global score, highest_score, direction

    start_screen_flag = True
    running = True
    while running:
        if start_screen_flag:
            start_screen(screen)
            snake = Snake()
            food = Food()
            initialize_grass()
            initialize_flowers()
            play_random_music()
            highest_score = load_highest_score(SPEED)
            start_screen_flag = False

        screen.fill(BACKGROUND_COLOR)
        draw_grass()
        draw_flowers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'
                elif event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                elif event.key == pygame.K_s:
                    start_screen_flag = settings()
                elif event.key == pygame.K_m:
                    play_random_music()

        snake.move()

        # kolizja z jablkie,
        if snake.coordinates[0][0] == food.x and snake.coordinates[0][1] == food.y:
            score += 1
            if score == 50:
                great_text = font.render("Amazing", True, (0, 0, 0))
                screen.blit(great_text, (GAME_WIDTH / 2, GAME_HEIGHT / 2))
                pygame.time.delay(1000)
            point_sound.play()
            food = Food()
            snake.grow()
        else:
            snake.remove_tail()

        # sprawdzanie czy nie ma kolizji
        if snake.check_collision() and not start_screen_flag:
            if score > highest_score:
                highest_score = score
                save_highest_score(SPEED, highest_score)
            game_over()
            score = 0
            direction = 'down'
            snake = Snake()
            food = Food()
            highest_score = load_highest_score(SPEED)
            continue


        # Rysowanie weza i jedzenia
        snake.draw()
        food.draw()

        # wyswietlenie wyniku
        score_text = font.render(f"Score: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        #Wyswietlanie poziomu
        difficulty_text = font.render(f'Difficulty: {difficulty}', True, YELLOW)
        screen.blit(difficulty_text, (10, 50))

        # wyswietlenie najlepszego wyniku
        highest_score_text = font.render(f"Highscore: {highest_score}", True, YELLOW)
        screen.blit(highest_score_text, (GAME_WIDTH - highest_score_text.get_width() - 10, 10))

        # aktualizacja ekranu
        if not start_screen_flag:
            pygame.display.update()

        # kontrola predkosci gry
        clock.tick(SPEED)

if __name__ == "__main__":
    main()
