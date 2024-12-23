import pygame
import random
import sys
import os
script_dir = os.path.dirname(__file__)

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Christmas Game")

# Load images
background_img = pygame.image.load(r"C:\Users\sanja\OneDrive\Desktop\code\VSWhere\background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

tree_img = pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\christmastree.png")
tree_img = pygame.transform.scale(tree_img, (300, 450))

basket_img = pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\basket.png")
basket_img = pygame.transform.scale(basket_img, (100, 50))

ornament_images = [
    pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\ornament1.png"),
    pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\ornament2.png"),
    pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\ornament3.png")
]
ornament_images = [pygame.transform.scale(img, (40, 40)) for img in ornament_images]

bomb_img = pygame.image.load(r"C:\Users\sanja\My project\Library\PackageCache\com.unity.ide.visualstudio@2.0.22\Editor\VSWhere\bomb.png")
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
# Add an ornament
def add_ornament():
    while True:
        x = random.randint(50, WIDTH - 50)
        if not (tree_x <= x <= tree_x + 300):  # Avoid spawning ornaments in the tree area
            break
    image = random.choice(ornament_images)
    ornaments.append({'x': x, 'y': 0, 'image': image})
    



# Add the bomb, we bring the booooom
def add_bomb():
    x = random.randint(50, WIDTH - 50)
    bombs.append({'x': x, 'y': 0})

# Add to tree decorations
def add_to_tree_decoration():
    x = random.randint(TREE_DECORATION_AREA['x_min'], TREE_DECORATION_AREA['x_max'])
    y = random.randint(TREE_DECORATION_AREA['y_min'], TREE_DECORATION_AREA['y_max'])
    tree_decorations.append((x, y))

# Draw snowflakes
def draw_snowflakes():
    for snowflake in snowflakes:
        pygame.draw.circle(screen, WHITE, (snowflake['x'], snowflake['y']), 2)

# Update snowflakes
def update_snowflakes():
    for snowflake in snowflakes:
        snowflake['y'] = (snowflake['y'] + 1) % HEIGHT
        if snowflake['y'] == 0:
            snowflake['x'] = random.randint(0, WIDTH)

# Draw tree decorations
def draw_tree_decorations():
    for decoration in tree_decorations:
        screen.blit(random.choice(ornament_images), decoration)

# Main game loop
clock = pygame.time.Clock()
running = True
add_ornament()

while running:
    # Clear screen and draw background
    screen.blit(background_img, (0, 0))

    # Draw snowflakes
    draw_snowflakes()
    update_snowflakes()

    # Draw Christmas tree
    screen.blit(tree_img, (tree_x, tree_y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - 100:
        basket_x += basket_speed

    # Update ornaments
    for ornament in ornaments[:]:
        ornament['y'] += ornament_speed
        if ornament['y'] > HEIGHT:
            ornaments.remove(ornament)
            score -= 1
        elif basket_x < ornament['x'] < basket_x + 100 and basket_y < ornament['y'] < basket_y + 50:
            ornaments.remove(ornament)
            score += 1
            add_to_tree_decoration()

    # Update da bombs
    for bomb in bombs[:]:
        bomb['y'] += bomb_speed
        if bomb['y'] > HEIGHT:
            bombs.remove(bomb)
        elif basket_x < bomb['x'] < basket_x + 100 and basket_y < bomb['y'] < basket_y + 50:
            bombs.remove(bomb)
            score -= 100000
            running = False

    # Add more ornaments and bombs
    if random.randint(1, 50 - level) == 1:
        add_ornament()
    if random.randint(1, 100 - level) == 1:
        add_bomb()

    # Draw basket
    screen.blit(basket_img, (basket_x, basket_y))

    # Draw ornaments
    for ornament in ornaments:
        screen.blit(ornament['image'], (ornament['x'], ornament['y']))

    # Draw bombs
    for bomb in bombs:
        screen.blit(bomb_img, (bomb['x'], bomb['y']))

    # Draw decorations on the tree
    draw_tree_decorations()

    # Update level based on score
    if score // 10 + 1 > level:
        level += 1
        ornament_speed += 1
        bomb_speed += 1

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    # Check if you win 
    if score >= 10:
        win_text = font.render("You Win! Press Q to quit.", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update el display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
