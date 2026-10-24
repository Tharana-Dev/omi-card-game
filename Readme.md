# 🃏 Omi: Sri Lankan Card Game

A fully playable, AI-driven implementation of the traditional Sri Lankan trick-taking card game **Omi**, built entirely with Python and Pygame. 

This project features a human player, an AI partner, and two AI opponents, complete with an interactive trump-selection phase, dynamic scoring, and intelligent card-playing heuristics.

## ✨ Features

- **Complete Game Loop:** Play through rounds until one team reaches 10 points.
- **Intelligent AI:** AI opponents can follow suit, recognize when their partner is winning a trick, and strategically play trumps.
- **Dynamic Resizing:** The UI adapts to resizable windows, scaling cards and repositioning played cards automatically.
- **Trump Selection:** If you are the declarer, you get to choose the trump suit via a custom UI popup.
- **Scoring System:** Implements full Omi rules, including the 8-trick sweep (3 points) and the bonus round tie-breaker.
- **Modular Architecture:** Clean separation of concerns between game logic (`game_logic.py`), AI (`ai.py`), and rendering (`render.py`).

## 🛠️ Technologies
- **Language:** Python 3
- **GUI & Graphics:** Pygame
- **Architecture:** Object-Oriented Programming (OOP)

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tharana-Dev/omi-card-game.git
   cd omi-card-game
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame
   ```

3. **Add Assets (Optional):**
   The game is designed to run even without media files, but for the full experience, place the following files in the root directory:
   - `image.png` (Table background)
   - `card_play.wav` (Card swoosh sound)
   - `game_over.wav` (Game over sound)
   - `start_bg.mp3` (Menu music)

4. **Run the game:**
   ```bash
   python main.py
   ```

## 🎮 Controls

- **Mouse:** Click a card to play it (legal cards are highlighted with a green border).
- **Resize Window:** Drag the window corners to resize the table.

## 📜 Game Rules (Short Version)
- Teams: You & Partner (AI) vs. Left AI & Right AI.
- Follow the led suit if possible. If you can't, play any card.
- Trump beats any non-trump card.
- First team to 10 points wins the game.

## 📂 Project Structure
```text
omi-card-game/
├── main.py          # Entry point, UI loop, start screen
├── game_logic.py    # Core engine, rules, scoring, state management
├── ai.py            # AI decision-making and heuristics
├── render.py        # Card drawing and rotation logic
├── config.py        # Constants (colors, sizes, fonts, ranks)
└── README.md        # Documentation
```

## 👨‍💻 Author
**Tharana Nimsara** — [@Tharana-Dev](https://github.com/Tharana-Dev)
- Portfolio: [tharana-dev.vercel.app](https://tharana-dev.vercel.app/)
