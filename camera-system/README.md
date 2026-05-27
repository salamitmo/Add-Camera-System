# Camera System

Flexible camera system for 2D renderer architecture.

## Features

- Top view projection
- Left view projection
- Camera follow system
- Zoom in/out
- Camera panning
- World-to-screen transformation
- Screen-to-world transformation
- Smooth camera tracking

---

## Controls

| Key | Action |
|---|---|
| W A S D | Move robot on X/Y |
| R / F | Move robot on Z |
| Q / E | Zoom in/out |
| Arrow Keys | Pan camera |
| TAB | Switch camera view |

---

## Architecture

project/
│
├── renderer/
│   ├── camera.py
│   └── renderer.py
│
├── entities/
│   └── robot.py
│
└── main.py

---

## Coordinate Systems

### World Space
3D coordinates in the simulation world.

Example:
(100, 50, 20)

### Screen Space
2D pixel coordinates on the screen.

Example:
(500, 300)

---

## Projection Modes

### Top View
Projects:
(X, Y)

### Left View
Projects:
(X, Z)

---

## Camera Features

- Object following
- Smooth movement
- Zoom scaling
- Coordinate transformations
- Panning