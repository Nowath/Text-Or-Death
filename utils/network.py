"""
Network utilities for client-server communication
"""
import socket
import json
import threading
from enum import Enum

class MessageType(Enum):
    PLAYER_JOIN = "player_join"
    PLAYER_LEAVE = "player_leave"
    GAME_START = "game_start"
    ROUND_START = "round_start"
    WORD_CHALLENGE = "word_challenge"
    PLAYER_RESPONSE = "player_response"
    ROUND_END = "round_end"
    GAME_END = "game_end"
    PLAYER_ELIMINATED = "player_eliminated"
    HEARTBEAT = "heartbeat"

class NetworkMessage:
    def __init__(self, msg_type, data=None, player_id=None):
        self.type = msg_type
        self.data = data or {}
        self.player_id = player_id
    
    def to_json(self):
        return json.dumps({
            "type": self.type.value if isinstance(self.type, MessageType) else self.type,
            "data": self.data,
            "player_id": self.player_id
        })
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            msg_type=data["type"],
            data=data.get("data", {}),
            player_id=data.get("player_id")
        )

class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.message_handlers = {}
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        if self.socket:
            self.connected = False
            self.socket.close()
    
    def send_message(self, message):
        if self.connected and self.socket:
            try:
                data = message.to_json() + "\n"
                self.socket.send(data.encode())
                return True
            except Exception as e:
                print(f"Send failed: {e}")
                return False
        return False
    
    def listen(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        message = NetworkMessage.from_json(line.strip())
                        self.handle_message(message)
            except Exception as e:
                print(f"Listen error: {e}")
                break
        
        self.connected = False
    
    def handle_message(self, message):
        handler = self.message_handlers.get(message.type)
        if handler:
            handler(message)
    
    def register_handler(self, message_type, handler):
        self.message_handlers[message_type] = handler