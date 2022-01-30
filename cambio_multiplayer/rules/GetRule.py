from rules.CardRules import rules


def return_rule(card):
    """
    rules:
    1-6             : No effect
    7-8             : Look at own card
    9-10            : Look at another's card
    jack/queen      : Blind trade
    king            : Look then trade if wanted
    joker           : No effect

    """

    numeric_value = card.return_numeric_value_cambio()

    # default cards and joker
    if 0 <= numeric_value <= 6:
        return rules[1]

    if numeric_value == 7 or numeric_value == 8:
        return rules[2]

    if numeric_value == 9 or numeric_value == 10:
        return rules[3]

    if any(item is card.value for item in ['jack', 'queen']):
        return rules[4]

    if card.value is 'king':
        return rules[5]