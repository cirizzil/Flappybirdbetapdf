

- What this project does.  
- How to run and generate the PDF.  
- How to play.  
- Known limitations (must use Adobe Acrobat, etc.).

Feel free to adjust any specific details or wording as you see fit.

---

# Flappy Bird in PDF (Button Version)

This repository contains a Python script that generates a **Flappy Bird**–style game **embedded in a PDF file**. Once generated, the PDF can be opened in **Adobe Acrobat** (desktop) to play the game by clicking on **Start** and **FLAP** buttons.

## How It Works
![image](https://github.com/user-attachments/assets/06a606ed-2ac3-4b89-8432-11076518991d)


1. The Python script creates a **grid of invisible button widgets** for the background.  
2. It embeds **Acrobat JavaScript** into the PDF that controls:  
   - The bird’s position and velocity.  
   - Scrolling pipes.  
   - Collision detection.  
   - Score updates.  
3. Because PDF can show/hide each button field, the code simulates a moving bird and pipes.  
4. **Gravity** pulls the bird down each frame; clicking **“FLAP”** gives the bird an upward jump.

## Requirements

- **Python 3.6+** (should work on most modern Python versions).  
- **Adobe Acrobat** (Reader DC or Acrobat Pro DC, desktop version). Other PDF readers generally **do not** support the JavaScript and form features used here.

## Usage

1. **Clone or Download** this repository.  
2. Navigate to the folder in a terminal/command prompt.  
3. Run the Python script:
   ```bash
   python flappyinpdf_button.py
   ```
   This creates a file named **`flappy_out.pdf`** in the same folder.

4. **Open** `flappy_out.pdf` with **Adobe Acrobat** (desktop).  
   - _Do not open in a web browser_ or another PDF viewer; the game won’t run.  

5. **Click “Start”** (in the center of the PDF) to begin the game.  
6. **Click “FLAP”** (on the right side) repeatedly to keep the bird from falling.  
   - Each click sets an upward velocity.  
   - Gravity pulls the bird down automatically over time.  
7. Avoid **collisions** with pipes or going off the top/bottom of the play area.  
8. When the bird collides, the game ends with a “Game Over!” message.  

## Adjusting the Difficulty

Inside the JavaScript code (in `flappyinpdf_button.py`), look for the lines:

```js
var gravity = 0.3;
var flapStrength = 3.0;
```

- **Increasing** `gravity` makes the bird fall faster.  
- **Decreasing** `flapStrength` makes the bird’s jump smaller.  

Tweak these to your liking.

## Troubleshooting

1. **No Movement or Buttons Don’t Work**  
   - Ensure you’re in **Adobe Acrobat** (desktop app).  
   - Go to **Edit → Preferences → JavaScript** and confirm “Enable Acrobat JavaScript” is on.  
   - Also check **Security (Enhanced)** settings—try disabling “Protected Mode” or add a privileged location.

2. **Bird Won’t Flap**  
   - Make sure you’re actually clicking the **FLAP** button.  
   - Lower `gravity` or raise `flapStrength` if the bird seems to keep sinking.

3. **No PDF Generated**  
   - Double-check you’re running **`python flappyinpdf_button.py`** in the correct folder, and that no errors appear in the console.

## License

This project is provided for educational and fun demonstration purposes. Use at your own risk.  
Feel free to modify and share as you like, but note that **PDF JavaScript** functionality may be blocked or unsupported in many readers.

---

Enjoy your PDF-based Flappy Bird!
