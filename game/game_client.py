"""
Game Client for Text or Death multiplayer game
"""
import pygame
import threading
from game.player import Player, PlayerState
from utils.network import NetworkClient, NetworkMessage, MessageType
from ui.game_ui import GameUI

class GameClient:
    def __init__(self, config):
        self.config = config
        self.screen_width = config.get("client", "screen_width")
        self.screen_height = config.get("client", "screen_height")
        self.fps = config.get("client", "fps")
        
        # Initialize pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Text or Death")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.connected = False
        self.player_id = None
        self.players = {}
        self.current_word = ""
        self.typed_text = ""
        self.game_active = False
        self.current_round = 0
        self.time_remaining = 0
        
        # UI
        self.ui = GameUI(self.screen, config)
        
        # Network
        self.network_client = NetworkClient(
            config.get("client", "server_host"),
            config.get("client", "server_port")
        )
        self.setup_network_handlers()
    
    def setup_network_handlers(self):
        """Setup network message handlers"""
        self.network_client.register_handler(MessageType.PLAYER_JOIN.value, self.handle_player_join)
        self.network_client.register_handler(MessageType.PLAYER_LEAVE.value, self.handle_player_leave)
        self.network_client.register_handler(MessageType.GAME_START.value, self.handle_game_start)
        self.network_client.register_handler(MessageType.ROUND_START.value, self.handle_round_start)
        self.network_client.register_handler(MessageType.ROUND_END.value, self.handle_round_end)
        self.network_client.register_handler(MessageType.GAME_END.value, self.handle_game_end)
        self.network_client.register_handler("game_state", self.handle_game_state)
        self.network_client.register_handler("special_message", self.handle_special_message)
    
    def connect_to_server(self, player_name):
        """Connect to the game server"""
        if self.network_client.connect():
            # Start listening thread
            listen_thread = threading.Thread(target=self.network_client.listen, daemon=True)
            listen_thread.start()
            
            # Send join request
            join_message = NetworkMessage(MessageType.PLAYER_JOIN, {"name": player_name})
            self.network_client.send_message(join_message)
            return True
        return False
    
    def run(self):
        """Main game loop"""
        # Show connection screen
        player_name = self.ui.show_connection_screen()
        if not player_name:
            return
        
        # Connect to server
        if not self.connect_to_server(player_name):
            self.ui.show_error("Failed to connect to server")
            return
        
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_active and self.current_word:
                    if event.key == pygame.K_BACKSPACE:
                        self.typed_text = self.typed_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.submit_word()
                    else:
                        char = event.unicode
                        if char.isprintable():
                            self.typed_text += char
                            
                            # Auto-submit if word is complete
                            if self.typed_text.lower() == self.current_word.lower():
                                self.submit_word()
    
    def submit_word(self):
        """Submit the typed word to server"""
        if self.current_word and self.network_client.connected:
            response_message = NetworkMessage(
                MessageType.PLAYER_RESPONSE,
                {
                    "text": self.typed_text,
                    "complete": True
                },
                self.player_id
            )
            self.network_client.send_message(response_message)
    
    def update(self):
        """Update game state"""
        pass
    
    def render(self):
        """Render the game"""
        self.screen.fill((0, 0, 0))  # Black background
        
        if not self.connected:
            self.ui.draw_waiting_screen("Connecting to server...")
        elif not self.game_active:
            self.ui.draw_lobby_screen(self.players)
        else:
            self.ui.draw_game_screen(
                self.current_word,
                self.typed_text,
                self.players,
                self.current_round,
                self.time_remaining
            )
        
        pygame.display.flip()
    
    # Network message handlers
    def handle_player_join(self, message):
        """Handle player join message"""
        data = message.data
        if "success" in data:
            if data["success"]:
                self.connected = True
                self.player_id = data["player_id"]
            else:
                self.ui.show_error(data.get("reason", "Failed to join"))
        elif "player" in data:
            player_data = data["player"]
            self.players[player_data["id"]] = player_data
    
    def handle_player_leave(self, message):
        """Handle player leave message"""
        player_id = message.data["player_id"]
        if player_id in self.players:
            del self.players[player_id]
    
    def handle_game_start(self, message):
        """Handle game start message"""
        self.game_active = True
        self.current_round = 0
        self.typed_text = ""
        self.current_word = ""
    
    def handle_round_start(self, message):
        """Handle round start message"""
        data = message.data
        self.current_round = data["round"]
        self.current_word = data["word"]
        self.typed_text = ""
        self.time_remaining = data["time_limit"]
        
        # Start countdown timer
        threading.Thread(target=self.countdown_timer, args=(data["time_limit"],), daemon=True).start()
    
    def handle_round_end(self, message):
        """Handle round end message"""
        data = message.data
        results = data["results"]
        
        # Update player states based on results
        for result in results:
            player_id = result["player_id"]
            if player_id in self.players:
                self.players[player_id]["lives"] = result["lives"]
                self.players[player_id]["state"] = "eliminated" if result["eliminated"] else "waiting"
        
        self.current_word = ""
        self.typed_text = ""
    
    def handle_game_end(self, message):
        """Handle game end message"""
        self.game_active = False
        data = message.data
        winner = data.get("winner")
        
        if winner:
            self.ui.show_game_over(winner, data["final_scores"])
    
    def handle_game_state(self, message):
        """Handle game state update"""
        data = message.data
        self.players = {p["id"]: p for p in data["players"]}
        self.game_active = data["game_active"]
        self.current_round = data["current_round"]
    
    def handle_special_message(self, message):
        """Handle special messages from server"""
        data = message.data
        print(f"🎮 {data.get('message', '')}")
        if data.get('bots_added'):
            print(f"Added {data['bots_added']} AI opponents!")
    
    def countdown_timer(self, duration):
        """Countdown timer for rounds"""
        import time
        for i in range(duration, 0, -1):
            if not self.game_active or not self.current_word:
                break
            self.time_remaining = i
            time.sleep(1)
        self.time_remaining = 0
    
    def cleanup(self):
        """Cleanup resources"""
        if self.network_client:
            self.network_client.disconnect()