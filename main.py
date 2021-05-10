import pygame
import random

pygame.font.init()
 
# GLOBALS VARS
screen_width = 800
screen_height = 700
# The tetris game has a 'board' of 20x10 (blocks)
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

# Positions
top_left_x = (screen_width - play_width) // 2 # This is the X position (= 250)
top_left_y = screen_height - play_height # This is the Y position (= 100)
 
# SHAPE FORMATS
# The shapes are represented in a grid of 5x5 periods
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape and colors
 
 
class Piece(object):
    def __init__(self, x, y, shape):
        # (x, y) is the position where the shape is gonna show up
        self.x = x # Should be the middle of the screen
        self.y = y # Should be 0
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
 
def create_grid(locked_positions={}): # locked_positions = {(0,1): (255,0,0)} -> key-position and value-color
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] # The (0,0,0) means the color black
    # The line above creates a 10x20 array that contains the color of each block 

    for line in range(len(grid)):
        for column in range(len(grid[line])):
            if (column, line) in locked_positions:
                color = locked_positions[(column, line)]
                grid[line][column] = color # Make the locked positions appear on the screen
    return grid

# Take a better look at IT
def convert_shape_format(shape): 
    # shape.rotation % len(shape.shape) -> returns a number between 0 and the len(shape.shape)-1
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    
    for i, position in enumerate(positions):
        # This is necessary to 'take out' the offset to the right and down caused by the periods
        positions[i] = (position[0] - 2, position[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_position = [[(column, line) for column in range(10) if grid[line][column] == (0,0,0)] for line in range(20)]
    # The line above creates a 10x20 array that contains the position of each block
    accepted_position = [j for sub in accepted_position for j in sub]
    # Turns the previous accepted_position to a normal list (without sublists for the lines)

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_position and pos[1] > -1:
            return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape(): # Return a random shape from 'shapes' list
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - 50 - (label.get_height()/2)))

def draw_grid(surface, grid): # Draw the grid lines
    sx = top_left_x
    sy = top_left_y

    # pygame.draw.line(surface, color, start_position, end_position)
    for line in range(len(grid)):
        # Draw the horizontal lines
        pygame.draw.line(surface, (128,128,128), (sx, sy + line * block_size), (sx + play_width, sy + line * block_size))
        for column in range(len(grid[line])):
            # Draw the vertical lines
            pygame.draw.line(surface, (128,128,128), (sx + column * block_size, sy), (sx + column * block_size, sy + play_height))

def clear_rows(grid, locked):
    increment = 0
    for line in range(len(grid)-1, -1, -1):
        row = grid[line]
        if (0,0,0) not in row:
            increment += 1
            ind = line
            for column in range(len(row)): # Delete an entire row
                try:
                    del locked[(column, line)]
                except:
                    continue
    
    if increment > 0:
        # [::-1] -> this inverts the current order of the list
        # sorted(list(locked), key = lambda x : x[1])[::-1] -> first sorts ascending acording to the y axis and then inverts
        # the order of the list ([::-1]) to be descending
        for key in sorted(list(locked), key=lambda x : x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment


def draw_next_shape(shape, surface): # Draws the next shape to show the player what that is
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))

def update_score(nscore):
    score = max_score()
    
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0,0,0)) # Background is black

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    # surface.blit(label, (x,y))
    # The x position needs to be subtracted by half of the labels size so it'll be at the middle. 
    # Otherwise the Title will be a bit to the right because it'll start to write at the center
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30)) # middle of the screen coordinates

    # CURRENT SCORE
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 25, sy + 150))

    # LAST SCORE
    label = font.render('High score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 210
    sy = top_left_y + 100

    surface.blit(label, (sx + 25, sy + 150))

    for line in range(len(grid)): # This draws the little squares
        for column in range(len(grid[line])):
            # pygame.draw.rect(surface, color, (x_position, y_position, width, height), border_size)
            pygame.draw.rect(surface, grid[line][column], (top_left_x + column * block_size, top_left_y + line * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)

def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() # Get the amount of time since the last clock.tick
        clock.tick()

        # fall_time and level_time are divided by 1000 to turn them into seconds

        # MAKE THE PIECE MOVE
        if fall_time/1000 >= fall_speed:
            # The line above is important to make the game playable, otherwise, if it didn't exist thw game would
            # so fast that would become unplayable
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
                # If during the fall of the piece there's a position that isn't valid, that means the piece hit
                # the bottom of the screen or another piece. So it'll be time to change to another piece

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # Move block left
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT: # Move block right
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_UP: # Rotate shape
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_DOWN: # Move block down
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
        
        shape_pos = convert_shape_format(current_piece)

        # This makes the moving shape appear on the screen
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # Add the positions of the piece that is at the bottom to the locked_positions list
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions)
        
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle('YOU LOST!', 80, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press Any Key to Play', 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                main(win)
    
    pygame.display.quit()

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(win) # start game