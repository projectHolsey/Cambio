from cards.CreateDeck import create_deck

class GameInstance:
    def __init__(self):
        self.active_player_count = 0

        # Contains the player ID and obj
        self.players = {}

        self.deck_instance = None

    def start(self):
        self.deck_instance = create_deck()
        self.reset_game()

    def reset_game(self):
        self.active_player_count = 0
        self.players = {}

