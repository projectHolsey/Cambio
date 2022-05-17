from cambio.cambio_multiplayer.cards.CardObj import Card
from cambio.cambio_multiplayer.cards.CambioCard import CambioCard
from cambio.cambio_multiplayer.cards.CardValuesAndSuits import *


def create_deck_cambio(include_joker=True):
    """
        Create a deck of cards

        :param: 'include_joker': Boolean - True = include joker
        """

    # (Clubs/Spades are black, Hearts/Diamonds are red)
    deck = []

    for card_value in value:
        if card_value == 'joker' and include_joker:
            deck.append(CambioCard(card_value, None, 'black'))
            deck.append(CambioCard(card_value, None, 'red'))
            continue

        for suit in suits:
            if suit == 'clubs' or suit == 'spades':
                deck.append(CambioCard(card_value, suit, 'black'))
            else:
                deck.append(CambioCard(card_value, suit, 'red'))

    return deck

def create_deck(include_joker=True):
    """
        Create a deck of cards

        :param: 'include_joker': Boolean - True = include joker
        """

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



