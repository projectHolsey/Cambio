from cambio.cambio_multiplayer.cards.CardObj import Card

import abc

class CambioCard(Card):

    def __init__(self, card_value, suit, colour):
        super(CambioCard, self).__init__(card_value, suit, colour)

        self.player_card = False

    def return_numeric_value_cambio(self):
        if self.value == 'ace':
            return 1
        if any(item is self.value for item in ['jack', 'queen']):
            return 12
        if self.value == 'king':
            if self.colour == 'red':
                return -1
            return 12
        if self.value == 'joker':
            return 0

        # by default just return card's value as it's numeric value
        return int(self.value)

    def set_player_card(self):
        self.player_card = True