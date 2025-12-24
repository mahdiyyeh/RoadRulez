# RoadRulez - Educational Driving Game

An educational driving game application built with Python, Tkinter, and Pygame that teaches road safety rules through interactive quizzes and gameplay.

## Features

- **Learning Center**: Learn about road signs, car safety, and crossing safely
- **Quiz System**: Take quizzes to earn coins
- **Game Levels**: Play interactive driving game levels with quizzes
- **Car Customization**: Customize your car using earned coins
- **Car Brand Search**: Search and view car brand logos
- **User Accounts**: Register, login, and manage your account
- **Leaderboards**: Track your best scores for each level
- **Coin System**: Earn coins through quizzes and spend them on gameplay and customization

## Requirements

- Python 3.7+
- Required packages (see installation below)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RoadRulez
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install pygame pillow easygui pyautogui requests dnspython
```

## Running the Application

```bash
python3 road-rulez-app.py
```

## Project Structure

- `road-rulez-app.py` - Main application file
- `config.py` - Configuration constants and settings
- `database_manager.py` - Database operations
- `game_engine.py` - Game logic and classes
- `quiz_manager.py` - Quiz functionality
- `learning_manager.py` - Learning content management
- `utils.py` - Utility functions

## License

This project is for educational purposes.

