import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600  # Width and height of the game window
GREEN = (0, 255, 0)  # RGB color for green
WHITE = (255, 255, 255)  # RGB color for white
BLUE = (0, 0, 255)  # RGB color for blue
RED = (255, 0, 0)  # RGB color for red
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the game window
pygame.display.set_caption("Christmas Game")  # Set the window title

# Load images
script_dir = os.path.dirname(__file__)  # Get the directory of the script
background_img = pygame.image.load(f"{script_dir}/pictures/background.png")  # Load the background image
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Scale the background to fit the screen

tree_img = pygame.image.load(f"{script_dir}/pictures/christmastree.png")  # Load the Christmas tree image
# Scale the tree to make it taller and wider
tree_img = pygame.transform.scale(tree_img, (410, 900))  # Adjust dimensions for width and height

# Position the tree so the top half is off-screen
tree_rect = tree_img.get_rect(midbottom=(WIDTH // 2, HEIGHT + 200))  # Adjust the vertical position

basket_img = pygame.image.load(f"{script_dir}/pictures/basket.png")  # Load the basket image
basket_img = pygame.transform.scale(basket_img, (100, 50))  # Scale the basket image

# Load and resize ornament images
ornament_images = [
    pygame.image.load(f"{script_dir}/pictures/ornament1.png"),  # Load first ornament image
    pygame.image.load(f"{script_dir}/pictures/ornament2.png"),  # Load second ornament image
    pygame.image.load(f"{script_dir}/pictures/ornament3.png")   # Load third ornament image
]
ornament_images = [pygame.transform.scale(img, (40, 40)) for img in ornament_images]  # Scale all ornaments

bomb_img = pygame.image.load(f"{script_dir}/pictures/bomb.png")  # Load the bomb image
bomb_img = pygame.transform.scale(bomb_img, (40, 40))  # Scale the bomb image

# Load power-up image
power_up_img = pygame.image.load(f"{script_dir}/pictures/powerup.png")  # Load the power-up image
power_up_img = pygame.transform.scale(power_up_img, (40, 40))  # Scale the power-up image


# Game variables
basket_x = WIDTH // 2  # Initial horizontal position of the basket
basket_y = HEIGHT - 100  # Vertical position of the basket
basket_speed = 8  # Speed of the basket
ornaments = []  # List to store ornaments
bombs = []  # List to store bombs
power_ups = []  # List to store power-ups
ornament_speed = 5  # Speed of falling ornaments
bomb_speed = 6  # Speed of falling bombs
score = 0  # Initial score
tree_decorations = []  # List to store ornaments on the tree
level = 1  # Initial level
tree_x, tree_y = 100, HEIGHT - 500  # Position of the Christmas tree
snowflakes = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT)} for _ in range(100)]  # Generate snowflakes

# Power-up effect variables
power_up_active = False  # Whether a power-up is active
power_up_timer = 0  # Timer for power-up duration

# Font setup
font = pygame.font.Font(None, 36)  # Font for displaying text

# Define tree decoration area
TREE_DECORATION_AREA = {
    'x_min': tree_x + 100,  # Minimum x-coordinate for tree decorations
    'x_max': tree_x + 310,  # Maximum x-coordinate for tree decorations
    'y_min': tree_y + 50,  # Minimum y-coordinate for tree decorations
    'y_max': tree_y + 500  # Maximum y-coordinate for tree decorations
}

def is_within_tree(x, y):
    """
    Check if the (x, y) position is within the triangular area of the tree.
    """
    tree_center_x = tree_x + 205  # Approximate center of the tree
    tree_width = 410             # Scaled width of the tree
    tree_height = 900            # Scaled height of the tree

    # Calculate triangle boundaries at this y-coordinate
    left_boundary = tree_center_x - ((tree_width / 2) * ((y - tree_y) / tree_height))
    right_boundary = tree_center_x + ((tree_width / 2) * ((y - tree_y) / tree_height))

    return left_boundary <= x <= right_boundary

# Function to add a new ornament
def add_ornament():
    while True:
        x = random.randint(50, WIDTH - 50)  # Generate a random x-coordinate
        if not (tree_x <= x <= tree_x + 300):  # Avoid spawning ornaments near the tree
            break


# Function to add a bomb
def add_bomb():
    while True:
        x = random.randint(50, WIDTH - 50)
        if not (TREE_DECORATION_AREA['x_min'] <= x <= TREE_DECORATION_AREA['x_max']):
            bombs.append({'x': x, 'y': 0})
            break

# Function to add a power-up
def add_power_up():
    x = random.randint(50, WIDTH - 50)  # Generate a random x-coordinate
    power_ups.append({'x': x, 'y': 0})  # Add the power-up to the list

# Function to add an ornament to the tree decorations
def add_to_tree_decoration():
    while True:
        x = random.randint(TREE_DECORATION_AREA['x_min'], TREE_DECORATION_AREA['x_max'])
        y = random.randint(TREE_DECORATION_AREA['y_min'], TREE_DECORATION_AREA['y_max'])
        if is_within_tree(x, y):
            tree_decorations.append((x, y))
            break

# Function to draw snowflakes
def draw_snowflakes():
    for snowflake in snowflakes:
        pygame.draw.circle(screen, WHITE, (snowflake['x'], snowflake['y']), 2)  # Draw a snowflake as a small white circle

# Function to update snowflake positions
def update_snowflakes():
    for snowflake in snowflakes:
        snowflake['y'] = (snowflake['y'] + 1) % HEIGHT  # Move snowflakes down and reset them to the top
        if snowflake['y'] == 0:
            snowflake['x'] = random.randint(0, WIDTH)  # Randomize x-coordinate when resetting

# Function to draw tree decorations
def draw_tree_decorations():
    for decoration in tree_decorations:
        screen.blit(random.choice(ornament_images), decoration)  # Draw decorations on the tree

# Function to display the intro screen
def show_intro():
    intro_running = True  # Flag to keep the intro running
    while intro_running:
        screen.blit(background_img, (0, 0))  # Draw the background image
        # Display instructions
        intro_text1 = font.render("Welcome to the Christmas Game!", True, BLUE)
        intro_text2 = font.render("Catch ornaments in the basket to decorate the tree.", True, BLUE)
        intro_text3 = font.render("Avoid bombs or you lose the game.", True, RED)
        intro_text4 = font.render("If you fail to catch an ornament, you lose a point.", True, RED)
        intro_text5 = font.render("Press LEFT and RIGHT to move.", True, BLUE)
        intro_text6 = font.render("Press SPACE to start.", True, BLUE)

        # Position the text on the screen
        screen.blit(intro_text1, (WIDTH // 2 - intro_text1.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(intro_text2, (WIDTH // 2 - intro_text2.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(intro_text3, (WIDTH // 2 - intro_text3.get_width() // 2, HEIGHT // 2))
        screen.blit(intro_text4, (WIDTH // 2 - intro_text4.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(intro_text5, (WIDTH // 2 - intro_text5.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(intro_text6, (WIDTH // 2 - intro_text6.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()  # Update the display

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Start the game
                if event.key == pygame.K_SPACE:
                    intro_running = False

# Main game logic starts here
clock = pygame.time.Clock()  # Create a clock to manage the frame rate
running = True  # Flag to keep the game running

show_intro()  # Show the intro screen
add_ornament()  # Add the first ornament

# Modify the game loop for power-up logic
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            running = False

    # Movement logic for the basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - 100:
        basket_x += basket_speed

    # Update positions of ornaments and check collisions
    for ornament in ornaments[:]:
        ornament['y'] += ornament_speed
        if ornament['y'] > HEIGHT:  # Missed ornament
            ornaments.remove(ornament)
            score -= 1
        elif basket_x < ornament['x'] < basket_x + 100 and basket_y < ornament['y'] < basket_y + 50:  # Caught ornament
            ornaments.remove(ornament)
            score += 1
            add_to_tree_decoration()

    # Update positions of bombs and check collisions
    for bomb in bombs[:]:
        bomb['y'] += bomb_speed
        if bomb['y'] > HEIGHT:  # Missed bomb
            bombs.remove(bomb)
        elif basket_x < bomb['x'] < basket_x + 100 and basket_y < bomb['y'] < basket_y + 50:  # Hit by bomb
            running = False

    # Update positions of power-ups and check collisions
    for power_up in power_ups[:]:
        power_up['y'] += ornament_speed
        if power_up['y'] > HEIGHT:  # Missed power-up
            power_ups.remove(power_up)
        elif basket_x < power_up['x'] < basket_x + 100 and basket_y < power_up['y'] < basket_y + 50:  # Caught power-up
            power_ups.remove(power_up)
            power_up_active = True
            power_up_timer = pygame.time.get_ticks()  # Start the power-up timer

    # Handle power-up effects
    if power_up_active:
        current_time = pygame.time.get_ticks()
        if current_time - power_up_timer < 5000:  # Power-up lasts for 5 seconds
            basket_speed = 12  # Increase basket speed
            ornament_speed = 3  # Slow down ornaments
        else:
            power_up_active = False
            basket_speed = 8  # Reset basket speed
            ornament_speed = 5  # Reset ornament speed

    # Randomly add ornaments, bombs, and power-ups
    if random.randint(1, 50 - level) == 1:
        add_ornament()
    if random.randint(1, 100 - level) == 1:
        add_bomb()
    if random.randint(1, 200 - level) == 1:
        add_power_up()

    # Draw game elements
    screen.blit(background_img, (0, 0))  # Draw the background
    draw_snowflakes()  # Draw snowflakes
    update_snowflakes()  # Update snowflake positions
    screen.blit(tree_img, (tree_x, tree_y))  # Draw the tree
    screen.blit(basket_img, (basket_x, basket_y))  # Draw the basket

    for ornament in ornaments:
        screen.blit(ornament['image'], (ornament['x'], ornament['y']))  # Draw ornaments

    for bomb in bombs:
        screen.blit(bomb_img, (bomb['x'], bomb['y']))  # Draw bombs

    for power_up in power_ups:
        screen.blit(power_up_img, (power_up['x'], power_up['y']))  # Draw power-ups

    draw_tree_decorations()  # Draw decorations on the tree

    # Display score
    score_text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    # Check for win condition
    if score >= 10:
        win_text = font.render("You Win! Press Q to quit.", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    elif score <= -3:
        win_text = font.render("Your score was too small you lose.", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()  # Update the display
    clock.tick(30)  # Limit the frame rate

pygame.quit()  # Quit pygame
sys.exit()  # Exit the program

# as a note to whoever is reading this, i loved this challenge. I had never used pygame before this and now I love it.
# This was really fun and i hope you enjoy my game. It is not perfect but i loved making it and I hope you like it too. 