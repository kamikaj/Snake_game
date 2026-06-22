# 🐍 Classic Snake game — Pygame Feature Expansion & Customization

A customized version of the classic **Snake** game built using Python and the **Pygame** framework. This project focused on taking a foundational arcade codebase and extending it with custom multimedia elements, UI assets, and a persistence layer.

The main goal was to understand how to manipulate an existing codebase, manage asset pipelines (audio/graphics), and implement features that enhance the overall player experience ("game juice").

---

## 🕹️ Input Controls Matrix

The game engine features an extended control scheme beyond the standard directional inputs:

| Key / Action | In-Game Function | Menu / Game Over Function |
| :--- | :--- | :--- |
| **⬆️ ⬇️ ⬅️ ➡️ Arrows** | Control Snake movement | Change Difficulty Level (Menu only) |
| **`SPACEBAR`** | Resume game from settings | Start Game / Restart (Game Over) |
| **`M`** | Cycle through random soundtracks | Cycle through random soundtracks |
| **`C`** | Change Snake color randomly | Change Snake color randomly |
| **`S`** | Open settings menu | *Dynamic error message prompt* |
| **`R`** | Clear state and full restart | — |
| **`ESCAPE`** | — | Exit application |

---

## 🌲 Procedural Environment & Adaptive Rendering

* **Procedural Decoration:** The grass patches and flowers are generated procedurally on every initialization (`initialize_grass` and `initialize_flowers`), utilizing random color shading, sizes, and coordinate distributions so no two playthroughs look exactly alike.
* **Direction-Aware Anatomy:** The snake head features a dynamic layout engine (`draw_eyes` and `draw_tongue`). The rendering matrix pivots the coordinates of the eyes, pupils, and flickering tongue based on the current `direction` vector (Up/Down/Left/Right).

---

## 🎨 Key Customizations & Enhancements

*   **🎵 Dedicated Audio Pipeline:** Integrated Pygame’s mixer subsystem to handle concurrent audio channels, including background soundtracks and synchronized sound effects for in-game actions.
*   **🖼️ UI & Visual Redesign:** Created custom retro-themed startup menus, state screens, and dynamically adjustable color palettes for the snake and game elements.
*   **💾 High-Score Persistence:** Added a native `json` data layer to track, serialize, and save the all-time high score locally on the user's drive.
*   **⚙️ Code Adaptation:** Practiced reading and refactoring foundational code to inject new features without disrupting the core game loop.

---

## 📸 Screenshots

![Game Menu](pictures/1.png)

![Gameplay](pictures/2.png)

---

## ⚙️ Quick Start & Installation

1. Clone or download this repository.
2. Install Pygame via terminal:
   ```bash
   pip install pygame
