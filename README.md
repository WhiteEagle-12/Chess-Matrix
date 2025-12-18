# Gemini Chess Coach Pro

An advanced chess analysis tool powered by Stockfish and Google Gemini.

## Features

- **AI Coaching**: Get personalized, persona-based commentary on your moves from a "Grandmaster Coach" (powered by Gemini).
- **Stability Health Bar**: Visualize the "Practical Difficulty" of a position. A 10-segment bar shows how many "safe" moves exist, helping you understand if a position is solid or a "tactical tightrope."
- **Deep Analysis**: Uses Stockfish (MultiPV 10) to analyze the top 10 lines for every move.
- **Archetype Profiling**: Analyzes your playstyle (Accuracy, ACPL, Complexity) and assigns you an archetype (e.g., "The Magician", "The Solid Pro").
- **Game Library**: Save your games and analysis locally in the browser. Sidebar indicators show which games were "Solid" vs "Volatile".
- **Interactive Review**:
  - **Best Line Explorer**: Step through the engine's best variation.
  - **Practice Mode**: Retry mistakes by playing against the engine from the critical position.

## How to Use

1. **Open the App**: Simply open `index.html` in your web browser.
2. **Setup**:
   - Click the **Settings** (Gear icon) and enter your Google Gemini API Key.
   - (The key is stored locally in your browser).
3. **Load a Game**:
   - Click the **Upload** button (bottom right) and paste a PGN.
   - Or load a previously saved game from the sidebar (Hamburger menu).
4. **Analyze**: Click the **Review** button to start the full game analysis.

## Technical Details

- **Frontend**: Pure HTML/JS/CSS (Tailwind).
- **Engine**: Stockfish.js (Web Worker).
- **AI Model**: Gemini 1.5 Flash (via REST API).
