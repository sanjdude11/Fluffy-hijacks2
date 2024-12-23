import pygame
import random
import sys
import os
script_dir = os.path.dirname(__file__)

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Christmas Game")

# Load images
script_dir = os.path.dirname(__file__)
background_img = pygame.image.load(f"{script_dir}/pictures/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

tree_img = pygame.image.load(f"{script_dir}/pictures/christmastree.png")
tree_img = pygame.transform.scale(tree_img, (300, 450))

basket_img = pygame.image.load(f"{script_dir}/pictures/basket.png")
basket_img = pygame.transform.scale(basket_img, (100, 50))

ornament_images = [
    pygame.image.load(f"{script_dir}/pictures/ornament1.png"),
    pygame.image.load(f"{script_dir}/pictures/ornament2.png"),
    pygame.image.load(f"{script_dir}/pictures/ornament3.png")
]
ornament_images = [pygame.transform.scale(img, (40, 40)) for img in ornament_images]

bomb_img = pygame.image.load(f"{script_dir}/pictures/bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (40, 40))

# Game variables
basket_x = WIDTH // 2
basket_y = HEIGHT - 100
basket_speed = 8
ornaments = []
bombs = []
ornament_speed = 5
bomb_speed = 6
score = 0
tree_decorations = []
level = 1
tree_x, tree_y = 100, HEIGHT - 500
snowflakes = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT)} for _ in range(100)]

# Font
font = pygame.font.Font(None, 36)

# Tree decoration area
TREE_DECORATION_AREA = {
    'x_min': tree_x + 50,
    'x_max': tree_x + 250,
    'y_min': tree_y + 100,
    'y_max': tree_y + 400
}

# Functions
def add_ornament():
    while True:
        x = random.randint(50, WIDTH - 50)
        if not (tree_x <= x <= tree_x + 300):  # Avoid spawning ornaments in the tree area
            break
    image = random.choice(ornament_images)
    ornaments.append({'x': x, 'y': 0, 'image': image})

def add_bomb():
    x = random.randint(50, WIDTH - 50)
    bombs.append({'x': x, 'y': 0})

def add_to_tree_decoration():
    x = random.randint(TREE_DECORATION_AREA['x_min'], TREE_DECORATION_AREA['x_max'])
    y = random.randint(TREE_DECORATION_AREA['y_min'], TREE_DECORATION_AREA['y_max'])
    tree_decorations.append((x, y))

def draw_snowflakes():
    for snowflake in snowflakes:
        pygame.draw.circle(screen, WHITE, (snowflake['x'], snowflake['y']), 2)

def update_snowflakes():
    for snowflake in snowflakes:
        snowflake['y'] = (snowflake['y'] + 1) % HEIGHT
        if snowflake['y'] == 0:
            snowflake['x'] = random.randint(0, WIDTH)

def draw_tree_decorations():
    for decoration in tree_decorations:
        screen.blit(random.choice(ornament_images), decoration)

def show_intro():
    intro_running = True
    while intro_running:
        screen.blit(background_img, (0, 0))
        intro_text1 = font.render("Welcome to the Christmas Game!", True, BLUE)
        intro_text2 = font.render("Catch ornaments in the basket to decorate the tree.", True, BLUE)
        intro_text3 = font.render("Avoid bombs or you lose the game.", True, RED)
        intro_text4 = font.render("Press LEFT and RIGHT to move.", True, BLUE)
        intro_text5 = font.render("Press SPACE to start.", True, BLUE)

        screen.blit(intro_text1, (WIDTH // 2 - intro_text1.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(intro_text2, (WIDTH // 2 - intro_text2.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(intro_text3, (WIDTH // 2 - intro_text3.get_width() // 2, HEIGHT // 2))
        screen.blit(intro_text4, (WIDTH // 2 - intro_text4.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(intro_text5, (WIDTH // 2 - intro_text5.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro_running = False

# Main game logic
clock = pygame.time.Clock()
running = True

show_intro()
add_ornament()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - 100:
        basket_x += basket_speed

    for ornament in ornaments[:]:
        ornament['y'] += ornament_speed
        if ornament['y'] > HEIGHT:
            ornaments.remove(ornament)
            score -= 1
        elif basket_x < ornament['x'] < basket_x + 100 and basket_y < ornament['y'] < basket_y + 50:
            ornaments.remove(ornament)
            score += 1
            add_to_tree_decoration()

    for bomb in bombs[:]:
        bomb['y'] += bomb_speed
        if bomb['y'] > HEIGHT:
            bombs.remove(bomb)
        elif basket_x < bomb['x'] < basket_x + 100 and basket_y < bomb['y'] < basket_y + 50:
            running = False

    if random.randint(1, 50 - level) == 1:
        add_ornament()
    if random.randint(1, 100 - level) == 1:
        add_bomb()

    if score // 10 + 1 > level:
        level += 1
        ornament_speed += 1
        bomb_speed += 1

    screen.blit(background_img, (0, 0))
    draw_snowflakes()
    update_snowflakes()
    screen.blit(tree_img, (tree_x, tree_y))
    screen.blit(basket_img, (basket_x, basket_y))

    for ornament in ornaments:
        screen.blit(ornament['image'], (ornament['x'], ornament['y']))

    for bomb in bombs:
        screen.blit(bomb_img, (bomb['x'], bomb['y']))

    draw_tree_decorations()

    score_text = font.render(f"Score: {score}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    if score >= 10:
        win_text = font.render("You Win! Press Q to quit.", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()