from cambio.cambio_multiplayer.dealer.dealer_obj import dealer

import abc
from cambio.cambio_multiplayer.cards import CreateDeck
from cambio.cambio_multiplayer.cards import CardValuesAndSuits

class cambio_dealer(dealer):

    def __init__(self):
        super(cambio_dealer, self).__init__()

    def get_cards(self):
        self.deck = CreateDeck.create_deck_cambio()