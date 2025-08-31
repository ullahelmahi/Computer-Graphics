# Computer-Graphics
# 🎮 CSE422 Computer Graphics Lab – Mini Game Projects

This repository contains a collection of **mini games and graphical applications** developed as part of the **CSE422: Computer Graphics Lab** course. All projects are written in **C/C++ using the OpenGL library**, and demonstrate key concepts in 2D/3D graphics, transformations, animation, and user interaction.

---

## 📂 Contents

Each folder in this repository corresponds to a specific lab assignment or game project, including:

- 🚗 3D Car Racing Game    
- 🧱 Bullet Frenzy  
- ✨ Catch the Diamonds 
- ...

> Projects are implemented using **OpenGL (GL/glut.h)** and compiled with **g++ or Code::Blocks**.

---

## ⚙️ How to Run the Projects

To compile and run the projects successfully, you **must have the OpenGL library installed and properly linked**. 

✅ Good news:  
We've included a **`OpenGL` folder containing the required OpenGL library headers and binaries**. You don't need to install anything separately.

### 📁 Required Folder: `OpenGL/`
Make sure the included `OpenGL` folder remains in your project directory. It contains:
- `glut.h`
- `gl.h`, `glu.h`
- Corresponding `.lib` and `.dll` files (for Windows)

---

## 🛠 Compilation (Windows Example)

If you're using **Code::Blocks** or **Dev C++**, include the path to the `OpenGL` folder in your compiler's settings.

### Example (g++):
```bash
g++ main.cpp -o output.exe -lopengl32 -lglu32 -lfreeglut
