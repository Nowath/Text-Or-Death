"""
Game Server for Text or Death multiplayer game
"""
import socket
import threading
import time
import uuid
from game.player import Player, PlayerState
from utils.network import NetworkMessage, MessageType
from utils.word_generator import WordGenerator
import random

class GameServer:
    def __init__(self, config):
        self.config = config
        self.host = config.get("server", "host")
        self.port = config.get("server", "port")
        self.max_players = config.get("server", "max_players")
        
        self.socket = None
        self.running = False
        self.players = {}
        self.game_active = False
        self.current_round = 0
        self.word_generator = WordGenerator()
        self.ai_bots = []
        
    def start(self):
        """Start the game server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_players)
        
        self.running = True
        print(f"Server started on {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                print(f"New connection from {address}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
    
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        player_id = str(uuid.uuid4())
        player = None
        
        try:
            while self.running:
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break
                
                message = NetworkMessage.from_json(data)
                
                if message.type == MessageType.PLAYER_JOIN.value:
                    player = self.add_player(player_id, message.data.get("name", "Anonymous"), client_socket)
                    if player:
                        self.broadcast_player_joined(player)
                        self.send_game_state(player)
                
                elif message.type == MessageType.PLAYER_RESPONSE.value and player:
                    self.handle_player_response(player, message.data)
                
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            if player:
                self.remove_player(player_id)
            client_socket.close()
    
    def add_player(self, player_id, name, connection):
        """Add a new player to the game"""
        if len(self.players) >= self.max_players:
            self.send_message(connection, NetworkMessage(MessageType.PLAYER_JOIN, {"success": False, "reason": "Server full"}))
            return None
        
        player = Player(player_id, name, connection)
        self.players[player_id] = player
        
        self.send_message(connection, NetworkMessage(MessageType.PLAYER_JOIN, {"success": True, "player_id": player_id}))
        
        # Special mode for Nano - add AI bots for single player experience
        if name.lower() == "nano" and len(self.players) == 1:
            print("🎮 Welcome Nano! Starting single-player mode with AI bots...")
            self.add_ai_bots()
            # Send special welcome message
            welcome_msg = NetworkMessage("special_message", {
                "message": "Welcome to single-player mode, Nano! You're playing against AI bots.",
                "bots_added": len(self.ai_bots)
            })
            self.send_message(connection, welcome_msg)
        
        # Start game if we have enough players
        if len(self.players) >= 2 and not self.game_active:
            threading.Thread(target=self.start_game, daemon=True).start()
        
        return player
    
    def remove_player(self, player_id):
        """Remove a player from the game"""
        if player_id in self.players:
            player = self.players[player_id]
            del self.players[player_id]
            self.broadcast_player_left(player)
            
            # End game if not enough players
            if len(self.players) < 2 and self.game_active:
                self.end_game()
    
    def start_game(self):
        """Start a new game"""
        if self.game_active:
            return
        
        self.game_active = True
        self.current_round = 0
        
        # Reset all players
        for player in self.players.values():
            player.reset_for_new_game()
        
        self.broadcast_message(NetworkMessage(MessageType.GAME_START, {"players": len(self.players)}))
        
        # Start game rounds
        while self.game_active and len([p for p in self.players.values() if p.state != PlayerState.ELIMINATED]) > 1:
            self.run_round()
            time.sleep(2)  # Brief pause between rounds
        
        self.end_game()
    
    def run_round(self):
        """Run a single game round"""
        self.current_round += 1
        active_players = [p for p in self.players.values() if p.state != PlayerState.ELIMINATED]
        
        if len(active_players) <= 1:
            return
        
        # Generate word challenge
        difficulty = "easy" if self.current_round <= 3 else "medium" if self.current_round <= 6 else "hard"
        challenge = self.word_generator.create_typing_challenge(difficulty, 1)
        word = challenge["words"][0]
        
        # Send round start to all active players
        round_data = {
            "round": self.current_round,
            "word": word,
            "time_limit": self.config.get("game", "typing_time_limit"),
            "difficulty": difficulty
        }
        
        for player in active_players:
            player.start_typing(word)
            if hasattr(player, 'is_bot') and player.is_bot:
                # Schedule bot response
                self.simulate_bot_response(player.id, word)
            else:
                # Send to human players
                self.send_message(player.connection, NetworkMessage(MessageType.ROUND_START, round_data))
        
        # Wait for responses or timeout
        start_time = time.time()
        time_limit = self.config.get("game", "typing_time_limit")
        
        while time.time() - start_time < time_limit:
            time.sleep(0.1)
            
            # Check if all players have finished
            if all(p.state != PlayerState.TYPING for p in active_players):
                break
        
        # Process round results
        self.process_round_results(active_players, word)
    
    def handle_player_response(self, player, data):
        """Handle player typing response"""
        if player.state == PlayerState.TYPING:
            typed_text = data.get("text", "")
            player.update_typed_text(typed_text)
            
            # Check if word is complete
            if data.get("complete", False):
                correct = player.finish_typing()
                if correct:
                    player.add_score(10 + len(player.current_word))
                    player.rounds_survived += 1
    
    def process_round_results(self, players, word):
        """Process the results of a round"""
        results = []
        
        for player in players:
            if player.state == PlayerState.TYPING:
                player.finish_typing()  # Force finish for timeout
            
            correct = player.is_word_correct()
            if not correct:
                player.lose_life()
            
            results.append({
                "player_id": player.id,
                "name": player.name,
                "correct": correct,
                "typed": player.typed_text,
                "lives": player.lives,
                "eliminated": player.state == PlayerState.ELIMINATED
            })
        
        # Broadcast round results
        self.broadcast_message(NetworkMessage(MessageType.ROUND_END, {
            "round": self.current_round,
            "word": word,
            "results": results
        }))
    
    def end_game(self):
        """End the current game"""
        self.game_active = False
        
        # Find winner
        active_players = [p for p in self.players.values() if p.state != PlayerState.ELIMINATED]
        winner = None
        if len(active_players) == 1:
            winner = active_players[0]
            winner.state = PlayerState.WINNER
        
        # Broadcast game end
        self.broadcast_message(NetworkMessage(MessageType.GAME_END, {
            "winner": winner.get_stats() if winner else None,
            "final_scores": [p.get_stats() for p in self.players.values()]
        }))
    
    def send_message(self, connection, message):
        """Send message to a specific connection"""
        try:
            data = message.to_json() + "\n"
            connection.send(data.encode())
        except Exception as e:
            print(f"Send message error: {e}")
    
    def broadcast_message(self, message):
        """Broadcast message to all connected players"""
        for player in self.players.values():
            if not (hasattr(player, 'is_bot') and player.is_bot):
                self.send_message(player.connection, message)
    
    def broadcast_player_joined(self, player):
        """Broadcast that a player joined"""
        self.broadcast_message(NetworkMessage(MessageType.PLAYER_JOIN, {
            "player": player.get_stats(),
            "total_players": len(self.players)
        }))
    
    def broadcast_player_left(self, player):
        """Broadcast that a player left"""
        self.broadcast_message(NetworkMessage(MessageType.PLAYER_LEAVE, {
            "player_id": player.id,
            "name": player.name,
            "total_players": len(self.players)
        }))
    
    def send_game_state(self, player):
        """Send current game state to a player"""
        game_state = {
            "players": [p.get_stats() for p in self.players.values()],
            "game_active": self.game_active,
            "current_round": self.current_round
        }
        self.send_message(player.connection, NetworkMessage("game_state", game_state))
    
    def add_ai_bots(self):
        """Add AI bots for single player mode"""
        bot_names = ["TypeBot", "SpeedDemon", "WordWizard"]
        
        for i, bot_name in enumerate(bot_names):
            if len(self.players) >= self.max_players:
                break
                
            bot_id = f"bot_{i}"
            bot_player = Player(bot_id, bot_name, None)  # No connection for bots
            bot_player.is_bot = True
            self.players[bot_id] = bot_player
            self.ai_bots.append(bot_id)
        
        print(f"Added {len(self.ai_bots)} AI bots for single player mode")
        
        # Broadcast the new bots
        for bot_id in self.ai_bots:
            self.broadcast_player_joined(self.players[bot_id])
    
    def simulate_bot_response(self, bot_id, word):
        """Simulate AI bot typing response"""
        if bot_id not in self.players:
            return
            
        bot = self.players[bot_id]
        if bot.state != PlayerState.TYPING:
            return
        
        # Different bot difficulties
        if "TypeBot" in bot.name:
            success_rate = 0.7  # 70% success rate
            delay = random.uniform(2, 6)
        elif "SpeedDemon" in bot.name:
            success_rate = 0.9  # 90% success rate  
            delay = random.uniform(1, 3)
        else:  # WordWizard
            success_rate = 0.8  # 80% success rate
            delay = random.uniform(1.5, 4)
        
        # Schedule bot response
        def bot_response():
            time.sleep(delay)
            if bot.state == PlayerState.TYPING and self.game_active:
                # Determine if bot gets it right
                if random.random() < success_rate:
                    bot.typed_text = word
                else:
                    # Make a typo
                    if len(word) > 1:
                        typo_pos = random.randint(0, len(word) - 1)
                        typo_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                        bot.typed_text = word[:typo_pos] + typo_char + word[typo_pos + 1:]
                    else:
                        bot.typed_text = random.choice("abcdefghijklmnopqrstuvwxyz")
                
                bot.finish_typing()
        
        threading.Thread(target=bot_response, daemon=True).start()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.socket:
            self.socket.close()