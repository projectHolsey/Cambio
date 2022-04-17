import abc
ABC = abc.ABCMeta('ABC', (object,), {})

class Card(ABC):
    def __init__(self, card_value, suit, colour):
        self.value = card_value
        self.suit = suit
        self.colour = colour

    def return_numeric_value_cambio(self):
        if self.value == 'ace':
            return 1
        if any(item is self.value for item in ['jack', 'queen', 'king']):
            return 12
        if self.value == 'joker':
            return 0

        # by default just return card's value as it's numeric value
        return int(self.value)



