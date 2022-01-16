from cards.CreateDeck import create_deck
from Instance_Server.server_code import server

class GameInstance:
    def __init__(self):
        self.active_player_count = 0

        # Contains the player ID and obj
        self.players = {}

        self.deck_instance = None

    def start_player(self):
        self.deck_instance = create_deck()
        self.reset_game()

    def start_server(self):
        server.server_setup()

    def reset_game(self):
        self.active_player_count = 0
        self.players = {}

