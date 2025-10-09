# Text or Death - Multiplayer Typing Game

A fast-paced multiplayer typing game where players must type words correctly or face elimination!

## Features

- **Multiplayer Online**: Up to 4 players can compete simultaneously
- **Progressive Difficulty**: Words get harder as rounds progress
- **Real-time Gameplay**: Live typing with immediate feedback
- **Lives System**: Players have 3 lives, lose one for each mistake
- **Scoring**: Points based on word length and typing speed
- **Clean UI**: Simple, focused interface for competitive typing

## Project Structure

```
text-or-death/
├── client/
│   └── main.py              # Client entry point
├── server/
│   └── server.py            # Server entry point
├── game/
│   ├── player.py            # Player class and state management
│   ├── game_server.py       # Server-side game logic
│   └── game_client.py       # Client-side game logic
├── utils/
│   ├── config.py            # Configuration management
│   ├── network.py           # Network utilities and message handling
│   └── word_generator.py    # Word generation and challenges
├── ui/
│   └── game_ui.py           # Pygame UI components
├── config.json              # Game configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. Install Python 3.7+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Starting the Server
```bash
python server/server.py
```

### Starting the Client
```bash
python client/main.py
```

### Gameplay
1. Enter your name when prompted
2. Wait for other players to join (minimum 2 players)
3. When a round starts, type the displayed word as quickly and accurately as possible
4. Press ENTER to submit or the word auto-submits when complete
5. Incorrect words cost you a life
6. Last player standing wins!

## Game Rules

- **Lives**: Each player starts with 3 lives
- **Elimination**: Lose all lives and you're out
- **Scoring**: 10 points + word length for correct words
- **Time Limit**: 10 seconds per word (configurable)
- **Difficulty**: Easy → Medium → Hard as rounds progress

## Configuration

Edit `config.json` to customize:
- Screen resolution and FPS
- Server host/port
- Player limits
- Time limits
- Difficulty progression

## Network Protocol

The game uses a custom JSON-based protocol over TCP sockets:
- `PLAYER_JOIN`: Player connection
- `ROUND_START`: New round with word challenge
- `PLAYER_RESPONSE`: Player's typed response
- `ROUND_END`: Round results
- `GAME_END`: Final scores and winner

## Extending the Game

### Adding Custom Words
Create word files: `words_easy.json`, `words_medium.json`, `words_hard.json`

### Custom Game Modes
Modify `game_server.py` to implement new game modes:
- Speed rounds
- Team battles
- Survival mode

### UI Themes
Extend `game_ui.py` with new color schemes and layouts

## Development

The codebase is modular and extensible:
- **Separation of Concerns**: Client/server logic separated
- **Event-Driven**: Network messages trigger game state changes
- **Configurable**: Easy to modify game parameters
- **Scalable**: Can be extended for more players or features

## Troubleshooting

- **Connection Issues**: Check firewall settings and port availability
- **Performance**: Adjust FPS in config for slower machines
- **Network Lag**: Consider implementing client-side prediction for smoother gameplay

Enjoy the game and may the fastest typer win! 🎮⌨️