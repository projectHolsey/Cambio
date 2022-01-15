from cards.CardObj import Card
from cards.CardValuesAndSuits import *


def create_deck():
    """
    Create a deck of cards

    :param: 'include_joker': Boolean - True = include joker
    """

    def create_deck(include_joker=True):
        # (Clubs/Spades are black, Hearts/Diamonds are red)
        deck = []

        for card_value in value:
            if card_value == 'joker' and include_joker:
                deck.append(Card(card_value, None, 'black'))
                deck.append(Card(card_value, None, 'red'))
                continue

            for suit in suits:
                if suit == 'clubs' or suit == 'spades':
                    deck.append(Card(card_value, suit, 'black'))
                else:
                    deck.append(Card(card_value, suit, 'red'))

        return deck
