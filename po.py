import pygame
import sys
import pickle
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fun")

# Player attributes
player_x = GRID_WIDTH // 2
player_y = GRID_HEIGHT // 2
player_color = RED

# World grid
world = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Mapping number keys to colors
color_mapping = {
    pygame.K_1: RED,
    pygame.K_2: GREEN,
    pygame.K_3: BLUE,
    pygame.K_4: YELLOW,
    pygame.K_5: CYAN,
    pygame.K_6: MAGENTA,
    pygame.K_7: ORANGE,
    pygame.K_8: PURPLE,
    pygame.K_9: BLACK,
}

# Color history stack for undo feature
color_history = []

# Color legend
color_legend = {
    RED: "Red",
    GREEN: "Green",
    BLUE: "Blue",
    YELLOW: "Yellow",
    CYAN: "Cyan",
    MAGENTA: "Magenta",
    ORANGE: "Orange",
    PURPLE: "Purple",
    BLACK: "Black"
}

# Font
font = pygame.font.Font(None, 36)

# Function to display popup message
def display_popup():
    popup_text = font.render("Press ESC to see color options", True, BLACK)
    popup_rect = popup_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(popup_text, popup_rect)

# Function to display controls page
def display_controls_page():
    screen.fill(WHITE)
    controls_text = font.render("Controls:", True, BLACK)
    screen.blit(controls_text, (20, 20))
    instructions = [
        "Arrow Keys: Move player",
        "1-9: Select color",
        "Space: Place block",
        "Backspace: Remove block",
        "Ctrl + Z: Undo last action",
        "Ctrl + S: Save game",
        "Ctrl + L: Load game"
    ]
    y_offset = 60
    for instruction in instructions:
        instruction_text = font.render(instruction, True, BLACK)
        screen.blit(instruction_text, (20, y_offset))
        y_offset += 40

# Function to restart the game
def restart_game():
    global world, color_history
    world = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    color_history = []

# Function to display start menu
def display_start_menu():
    screen.fill(WHITE)
    title_text = font.render("Color Fun", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))

    start_text = font.render("Press Space to Start", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

# Function to save the game state
def save_game(file_name):
    try:
        with open(file_name, 'wb') as file:
            game_state = {
                'world': world,
                'color_history': color_history
            }
            pickle.dump(game_state, file)
    except Exception as e:
        print("Error saving game:", e)

# Function to load the game state
def load_game(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                game_state = pickle.load(file)
                global world, color_history
                world = game_state['world']
                color_history = game_state['color_history']
    except Exception as e:
        print("Error loading game:", e)

# Game loop
running = True
show_legend = False
show_popup = True  # Show the popup message at the beginning
show_controls = False  # Whether to show the controls page
show_start_menu = True  # Show start menu initially

# Button rects
controls_button = pygame.Rect(20, 20, 160, 40)
restart_button = pygame.Rect(20, 70, 160, 40)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if show_start_menu:
                if event.key == pygame.K_SPACE:
                    show_start_menu = False
            elif event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < GRID_HEIGHT - 1:
                player_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < GRID_WIDTH - 1:
                player_x += 1
            elif event.key == pygame.K_SPACE:
                world[player_y][player_x] = player_color
                color_history.append((player_x, player_y, player_color))
            elif event.key == pygame.K_BACKSPACE:
                world[player_y][player_x] = 0
            elif event.key in color_mapping:
                player_color = color_mapping[event.key]
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if color_history:
                    last_change = color_history.pop()
                    x, y, prev_color = last_change
                    world[y][x] = 0  # Remove the block
                    player_x, player_y, player_color = x, y, prev_color
            elif event.key == pygame.K_ESCAPE:
                if not show_controls:
                    show_legend = not show_legend
                else:
                    show_controls = False
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_game("saved_game.dat")
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_game("saved_game.dat")
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_controls:
            if controls_button.collidepoint(event.pos):
                show_controls = True
            elif restart_button.collidepoint(event.pos):
                restart_game()

    # Holding down space to continuously place blocks
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        world[player_y][player_x] = player_color
        color_history.append((player_x, player_y, player_color))

    # Display the start menu
    if show_start_menu:
        display_start_menu()
        pygame.display.flip()
        continue

    # Display the popup message at the beginning
    if show_popup:
        screen.fill(WHITE)
        display_popup()
        pygame.display.flip()
        show_popup = False  # Don't show the popup again
        continue

    # Draw the world
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if world[y][x] != 0:
                pygame.draw.rect(screen, world[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    pygame.draw.rect(screen, player_color, (player_x * BLOCK_SIZE, player_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Display color legend if requested
    if show_legend:
        legend_text = font.render("Color Legend (Press Esc to close):", True, BLACK)
        screen.blit(legend_text, (20, 20))
        y_offset = 60
        for idx, (color, name) in enumerate(color_legend.items(), start=1):
            color_text = font.render(f"{name} - Press {idx}", True, color)
            screen.blit(color_text, (20, y_offset))
            y_offset += 40

    # Draw controls button if legend is not shown and controls page is not open
    if not show_legend and not show_controls:
        pygame.draw.rect(screen, BLACK, controls_button, 2)
        controls_text = font.render("Controls", True, BLACK)
        screen.blit(controls_text, (40, 30))

    # Draw restart button if legend is not shown and controls page is not open
    if not show_legend and not show_controls:
        pygame.draw.rect(screen, BLACK, restart_button, 2)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (45, 80))

    # Display controls page if requested
    if show_controls:
        display_controls_page()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

