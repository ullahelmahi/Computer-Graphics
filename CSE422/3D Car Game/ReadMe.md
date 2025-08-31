# 3D Car Racing

A fun and fast-paced 3D car racing game built using OpenGL and GLUT in Python. The game features both single-player and multiplayer modes where players compete to score points while using special powers like jump, shoot, and cheat modes. The HUD (heads-up display) shows real-time stats such as scores, power levels, and status effects like freezing or boosts.

---

## Introduction

This project is a 3D car racing game designed to showcase basic OpenGL rendering, user input handling, and game state management in Python. Players control cars on a track, trying to outscore opponents or the clock while managing their available powers. The game includes visual feedback for power-ups, freezes, cheat modes, and cooldown timers.

The game supports multiplayer mode (local, split controls) and single-player mode, with different UI placements for each. It demonstrates usage of GLUT for windowing and input, and OpenGL for rendering text and game elements.

---

## Features

- Real-time 3D rendering of cars and racing environment  
- Single-player and multiplayer modes  
- Display of player scores, jump and shoot powers on screen  
- Status indicators for freeze and cheat modes, with timers and cooldowns  
- Responsive keyboard and mouse controls  
- Cheat power with limited duration and cooldown  
- Obstacle boost effects

---

## Controls

### General Controls

- **Arrow Keys / WASD**: Move car (depends on player)  
- **Spacebar or F **: Jump (if jump powers or shoot powers available)  
- **C**: Activate cheat mode (if off cooldown)
- **M**: Activate Multiplayer

### Multiplayer Controls

- **Player 1:**  
  - Movement: Arrow keys  
  - Jump: SpaceBar  
  - Shoot: SpaceBar 
  - Cheat: 'C' key  

- **Player 2:**  
  - Movement: WASD  
  - Jump: 'F' key 
  - Shoot: 'F' key  
  - Cheat: 'C' key  

*(Customize keys in the code under keyboardListener and specialKeyListener functions.)*

---

## Credits

### This game was developed by:

Mohammad Ulla Hel Mahi

Akib Sarwar

Md Readus Shalehin

We hope you enjoy playing it as much as we enjoyed building it!

## Installation and Dependencies

Make sure you have Python 3.x installed. Then install required packages:

```bash
pip install PyOpenGL PyOpenGL_accelerate


