import pygame
import random
import json
import os
import asyncio
import websockets

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
BLOCK_SIZE = 20

# Grid size
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

COLORS = [
    (0, 240, 240),   # I
    (0, 0, 240),      # J
    (240, 160, 0),    # L
    (240, 240, 0),    # O
    (0, 240, 0),      # S
    (160, 0, 240),    # T
    (240, 0, 0)       # Z
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

# Piece class with hold mechanic support
class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.locked = False

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

# Grid initialization
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# Valid space checking
def valid_space(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and grid[y][x] != BLACK):
                    return False
    return True

def check_game_over(locked_positions):
    for pos in locked_positions:
        if pos[1] < 1:
            return True
    return False

def clear_lines(grid, locked):
    cleared = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            cleared += 1
            del_row(i, locked)
    return cleared

def del_row(row, locked):
    for j in range(GRID_WIDTH):
        try:
            del locked[(j, row)]
        except:
            continue
    for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
        x, y = key
        if y < row:
            new_key = (x, y + 1)
            locked[new_key] = locked.pop(key)

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(surface, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Draw ghost piece
def draw_ghost_piece(surface, piece, grid):
    ghost = Piece(piece.x, piece.y, piece.shape, GRAY)
    while valid_space(ghost, grid):
        ghost.y += 1
    ghost.y -= 1
    for i, row in enumerate(ghost.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, ghost.color, ( (ghost.x + j) * BLOCK_SIZE, (ghost.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_next_piece(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next:', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH + 20, 50))
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, (SCREEN_WIDTH + 20 + j * 20, 80 + i * 20, 20, 20), 0)

def draw_hold_piece(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Hold:', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH + 20, 200))
    if piece:
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, piece.color, (SCREEN_WIDTH + 20 + j * 20, 230 + i * 20, 20, 20), 0)

# New piece generator
def get_new_piece():
    i = random.randint(0, len(SHAPES) - 1)
    return Piece(GRID_WIDTH // 2 - 2, 0, SHAPES[i], COLORS[i])

def save_high_score(score):
    if not os.path.exists('highscore.json'):
        with open('highscore.json', 'w') as f:
            json.dump({'highscore': score}, f)
    else:
        with open('highscore.json', 'r+') as f:
            data = json.load(f)
            if score > data.get('highscore', 0):
                data['highscore'] = score
                f.seek(0)
                json.dump(data, f)
                f.truncate()

def get_high_score():
    if not os.path.exists('highscore.json'):
        return 0
    with open('highscore.json', 'r') as f:
        data = json.load(f)
        return data.get('highscore', 0)

# Pause functionality
def pause_game(win):
    paused = True
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('Paused', 1, WHITE)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        win.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - label.get_height() // 2))
        pygame.display.update()

# Level system
def get_level(score):
    return score // 1000

def get_drop_speed(level):
    return max(0.1, 0.4 - (level * 0.05))

# Sound effects
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

# Save and load game state
def save_game_state(locked_positions, current_piece, next_piece, hold_piece, score):
    state = {
        'locked_positions': locked_positions,
        'current_piece': (current_piece.x, current_piece.y, current_piece.shape, current_piece.color),
        'next_piece': (next_piece.x, next_piece.y, next_piece.shape, next_piece.color),
        'hold_piece': (hold_piece.x, hold_piece.y, hold_piece.shape, hold_piece.color) if hold_piece else None,
        'score': score
    }
    with open('savegame.json', 'w') as f:
        json.dump(state, f)

def load_game_state():
    if not os.path.exists('savegame.json'):
        return None
    with open('savegame.json', 'r') as f:
        state = json.load(f)
    locked_positions = state['locked_positions']
    current_piece = Piece(*state['current_piece'])
    next_piece = Piece(*state['next_piece'])
    hold_piece = Piece(*state['hold_piece']) if state['hold_piece'] else None
    score = state['score']
    return locked_positions, current_piece, next_piece, hold_piece, score

async def game_loop(websocket, _path):
    # your game loop logic

    win = pygame.display.set_mode((SCREEN_WIDTH + 200, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris Deluxe')

    locked_positions = {}
    current_piece = get_new_piece()
    next_piece = get_new_piece()
    hold_piece = None
    hold_used = False

    clock = pygame.time.Clock()
    fall_time = 0
    score = 0
    drop_speed = 0.4

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        level = get_level(score)
        drop_speed = get_drop_speed(level)

        if fall_time / 1000 > drop_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for i, row in enumerate(current_piece.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
                current_piece = next_piece
                next_piece = get_new_piece()
                cleared_lines = clear_lines(grid, locked_positions)
                score += cleared_lines * 150
                hold_used = False

                if check_game_over(locked_positions):
                    save_high_score(score)
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):
                            current_piece.rotate()
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                elif event.key == pygame.K_c and not hold_used:
                    if hold_piece is None:
                        hold_piece = current_piece
                        current_piece = next_piece
                        next_piece = get_new_piece()
                    else:
                        hold_piece, current_piece = current_piece, hold_piece
                        hold_piece.x, hold_piece.y = GRID_WIDTH // 2 - 2, 0
                    hold_used = True
                elif event.key == pygame.K_p:
                    pause_game(win)
                elif event.key == pygame.K_s:
                    save_game_state(locked_positions, current_piece, next_piece, hold_piece, score)
                elif event.key == pygame.K_l:
                    loaded_state = load_game_state()
                    if loaded_state:
                        locked_positions, current_piece, next_piece, hold_piece, score = loaded_state

        win.fill(BLACK)
        draw_grid(win, grid)
        draw_ghost_piece(win, current_piece, grid)

        for i, row in enumerate(current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(win, current_piece.color, ( (current_piece.x + j) * BLOCK_SIZE, (current_piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        draw_next_piece(next_piece, win)
        draw_hold_piece(hold_piece, win)

        font = pygame.font.SysFont('comicsans', 30)
        score_text = font.render(f'Score: {score}', 1, WHITE)
        high_score_text = font.render(f'High Score: {get_high_score()}', 1, WHITE)
        level_text = font.render(f'Level: {level}', 1, WHITE)
        win.blit(score_text, (SCREEN_WIDTH + 20, 350))
        win.blit(high_score_text, (SCREEN_WIDTH + 20, 400))
        win.blit(level_text, (SCREEN_WIDTH + 20, 450))

        pygame.display.update()

        # Send game state to the frontend
        game_state = {
            'grid': grid,
            'current_piece': {
                'x': current_piece.x,
                'y': current_piece.y,
                'shape': current_piece.shape,
                'color': current_piece.color
            },
            'next_piece': {
                'shape': next_piece.shape,
                'color': next_piece.color
            },
            'hold_piece': {
                'shape': hold_piece.shape,
                'color': hold_piece.color
            } if hold_piece else None,
            'score': score,
            'level': level,
            'high_score': get_high_score()
        }
        await websocket.send(json.dumps(game_state))

    pygame.time.wait(3000)

async def main():
    async with websockets.serve(game_loop, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
