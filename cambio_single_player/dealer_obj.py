import random

from cards import CreateDeck
from cards import CardValuesAndSuits

class dealer:
    def __init__(self):
        # Create a new deck of card objects
        self.deck = []
        self.disposed = []

    def get_cards(self):
        self.deck = CreateDeck.create_deck()

    def shuffle_cards(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)

    def despose_first_card(self):
        self.disposed.append(self.deck[0])
        self.deck.pop(0)