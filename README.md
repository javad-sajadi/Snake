# Snake: Graphical Desktop Game with Dynamic Grids & Save State

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter%20%2B%20Pillow-brightgreen.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive graphical implementation of the classic **Snake** arcade game built with Python, Tkinter, and PIL, featuring dynamic grid geometry, 10 difficulty levels, and full game state persistence (Save / Load).

---

## 🎮 Key Features

- **Dynamic Grid Dimensions:** Configurable grid width ($X > 4$) and height ($Y > 4$).
- **10 Difficulty Levels:** Granular speed scaling from casual pacing (Level 1) to ultra-fast reflex mode (Level 10).
- **Save & Resume System:** Pause anytime with `P` to save game state to disk and resume later seamlessly.
- **Custom Visual Sprites:** Custom textures for the snake head, body segments, apples, and boundaries.

---

## 🕹️ Controls & Gameplay

| Key | Action |
| :---: | :--- |
| **$\uparrow$ / `W`** | Move Up |
| **$\downarrow$ / `S`** | Move Down |
| **$\leftarrow$ / `A`** | Move Left |
| **$\rightarrow$ / `D`** | Move Right |
| **`P` / `Space`** | Pause Game / Save State Menu |

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/javad-sajadi/Snake.git
cd Snake
pip install -r requirements.txt
```

### 2. Launch the Game
```bash
python snake_game.py
```

---

## 📁 Repository Structure

```
.
├── snake_game.py       # Standalone executable graphical desktop game
├── snake_game.ipynb    # Interactive notebook version with game development logic
├── bodys.png           # Snake body segment texture
├── bodys2.png          # Snake head texture
├── bodys3.png          # Target apple texture
├── wall.png            # Boundary grid texture
├── requirements.txt    # Python dependencies (Pillow, NumPy)
└── .gitignore          # Ignore rules for save files, caches, and system files
```

---

## 📜 Author & License
- **Author:** [Javad Sajadi](https://github.com/javad-sajadi)
- **License:** MIT License
