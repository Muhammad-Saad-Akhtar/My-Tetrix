<!-- # Tetris Deluxe - Python (Pygame)

Tetris Deluxe is an enhanced version of the classic Tetris game built with Python and Pygame. It includes advanced features like a **ghost piece**, **hold piece**, **scoring system**, **save/load game state**, and **level progression**.

## Features
- 🎮 **Classic Tetris Gameplay** - Move, rotate, and drop tetrominoes to clear lines.
- 👻 **Ghost Piece** - Displays where the current piece will land.
- 🔄 **Hold Piece Mechanic** - Swap a piece to use later (once per drop).
- 📈 **Scoring & Levels** - Tracks scores, levels, and high scores.
- 💾 **Save & Load Game State** - Resume from where you left off.
- ⏸ **Pause Functionality** - Pause and resume at any time.
- 🔊 **Sound Effects** - Add immersive audio effects.

## How to Play
### Controls
- **Move Left:** `←`
- **Move Right:** `→`
- **Rotate Piece:** `↑`
- **Soft Drop:** `↓`
- **Hard Drop:** `SPACE`
- **Hold Piece:** `C` (Can only swap once per drop)
- **Pause Game:** `P`
- **Save Game State:** `S`
- **Load Saved Game:** `L`

### Scoring System
- **1 line cleared** → `150 points`
- **2 lines cleared** → `300 points`
- **3 lines cleared** → `450 points`
- **4 lines (Tetris!)** → `600 points`
- **Level Up** → Every `1000 points`, making pieces fall faster.

### Game Over
- The game ends if a new piece spawns in an already occupied space.
- High scores are stored in `highscore.json`.

## How It Works
### Ghost Piece 🏁
- The **ghost piece** is a transparent preview of where the current tetromino will land.
- It updates dynamically as the player moves the active piece.
- Helps in precise placement and strategy.

### Hold Piece 🔄
- Press `C` to **hold** a piece and swap it later.
- Can only be swapped once per drop to prevent abuse.

### Save & Load 💾
- Press `S` to save the current game state.
- Press `L` to load the previously saved game state.

## Installation & Running the Game
Make sure you have Python installed.

### Install Pygame
```sh
pip install pygame
```

### Run the Game
```sh
python tetris.py
```

## Future Improvements
- 🎵 Add background music and sound effects.
- 🎨 Improve visual aesthetics.
- 🌍 Online multiplayer mode (planned feature).
 -->
