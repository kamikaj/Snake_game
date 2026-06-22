# 🐍 Classic Snake game — Pygame Feature Expansion & Customization

A customized version of the classic **Snake** game built using Python and the **Pygame** framework. This project focused on taking a foundational arcade codebase and extending it with custom multimedia elements, UI assets, and a persistence layer.

The main goal was to understand how to manipulate an existing codebase, manage asset pipelines (audio/graphics), and implement features that enhance the overall player experience ("game juice").

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
