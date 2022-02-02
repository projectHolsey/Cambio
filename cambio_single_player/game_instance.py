import os

from dealer_obj import dealer
from player_obj import player

from cards import CardValuesAndSuits

class gameInstance:

    def __init__(self):
        self.accepted_vals = ["1", "2", "c", "q"]

    def start(self):
        game_dealer = dealer()
        game_dealer.get_cards()
        game_dealer.shuffle_cards()

        game_player = player()
        x = 1
        while len(game_player.cards) < 4:
            game_player.cards[str(x)] = game_dealer.deal_card()
            x += 1

        game_dealer.despose_first_card()

        print()

        response = ""
        while not response.lower() == "c" and not response.lower() == "q":

            print("")
            print("Current disposed card '" + str(game_dealer.disposed[-1]) + "'")
            print("Count of cards left : " + str(len(game_dealer.deck)))

            self.display_hand(game_player)

            new_card = None
            try:
                new_card = game_dealer.deal_card()
            except:
                print("Out of cards!!")
                break
            game_player.cards[x] = new_card
            print("NEW : " + str(game_player.cards[x]))

            game_player.known_cards.append("5")
            self.print_cards(game_player, game_dealer)
            game_player.known_cards.remove("5")

            self.check_if_player_has_card_to_dispose(game_player, game_dealer)

            if len(game_player.cards) == 0:
                print("Player has no cards left in hand!")
                break

            response = self.choice()
            if str(response) == "1":
                print("Discarded card : " + str(game_player.cards[x]))
                game_dealer.disposed.append(game_player.cards[x])
                del (game_player.cards[x])

                self.print_cards(game_player, game_dealer)
                self.display_hand(game_player)

            if str(response) == "2":
                # Keep card - remove from hand for time being
                drawn_card = game_player.cards[x]
                del (game_player.cards[x])

                print("Select card to swap with: ")
                print("( Cards Available : " + ",".join(game_player.cards.keys()) + " )")
                card_swap = input("Enter index of card > ")
                while not any(str(card_swap) == str(x) for x in game_player.cards.keys()):
                    print("Unaccepted entry, please enter another option")
                    print("( Cards Available : " + ",".join(game_player.cards.keys()) + " )")
                    card_swap = input("Enter index of card > ")

                # Add the chosen card to the discard pile
                game_dealer.disposed.append(game_player.cards[card_swap])
                # Swap the chosen card with the drawn card
                game_player.cards[card_swap] = drawn_card

                if not any(str(card_swap) == x for x in game_player.known_cards):
                    game_player.known_cards.append(str(card_swap))

                    self.print_cards(game_player, game_dealer)
                    self.display_hand(game_player)

        print("Value of hand = ")
        x = 0
        for idx, player_card in game_player.cards.items():
            print("Card : " + str(player_card))
            x += player_card.return_numeric_value_cambio()
        print(x)

    def choice(self):
        print("")
        print("Choose an option")
        print("1 - Discard new card")
        print("2 - Swap new card")
        print("c - Cambio")
        print("q - Quit")
        x = input("Enter choice >")
        while not any(str(x) == y for y in self.accepted_vals):
            print("Unaccepted entry, please enter another option : " + str(self.accepted_vals))
            x = input("Enter choice >")
        return x


    def check_if_player_has_card_to_dispose(self, game_player, game_dealer):
        cards_to_remove = []
        for item in game_player.known_cards:
            if game_dealer.disposed[-1].value == game_player.cards[str(item)].value:
                # There is a card in the player's hand of equal value to that of the top most discarded
                print(f"Your card ({str(game_player.cards[str(item)])}) is of similar value to card on top of discard pile.\n Do you wish to discard?")
                discard = input("Enter (y)es or (n)o > ")
                while not str(discard).lower() == "y" or str(discard).lower() == "n":
                    print("Bad entry, please try again")
                    discard = input("Enter (y)es or (n)o > ")

                # If the player wishes to discard
                if str(discard).lower() == "y":
                    print("Tossing your card to pile")
                    # Append the card to the top of discard pile
                    game_dealer.disposed.append(game_player.cards[str(item)])
                    # remove the card from the player's known cards
                    cards_to_remove.append(str(item))
                    # remove the card from the player's hand
                    del(game_player.cards[str(item)])

        for item in cards_to_remove:
            game_player.known_cards.remove(item)

        # Can't display the cards again because it will include card # 5 atm
        # if cards_to_remove:
        #     print_cards(game_player)
        #     display_hand(game_player)





    def display_hand(self, game_player):
        print("\ncurrent hand:")
        for idx, item in game_player.cards.items():
            if not any(str(idx) == str(x) for x in game_player.known_cards):
                print(f"{idx} : ?????")
            else:
                print(f"{idx} : {item}")

    # Function to print the cards
    def print_cards(self, game_player, game_dealer):

        s = ""
        print(s)
        for key, card in game_player.cards.items():
            if str(key) == "5":
                s = s + "\t\t\t\t       {}      ".format(str("NEW"))
            else:
                s = s + "\t        #{}       ".format(key)
        s = s + "\t\t\t\t     {}    ".format("Discarded")
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if str(key) == "5":
                s = s + "\t\t\t\t ________________"
            else:
                s = s + "\t ________________"
        s = s + "\t\t\t\t ________________"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if str(key) == "5":
                s = s + "\t\t\t\t|                |"
            else:
                s = s + "\t|                |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if str(key) == "5":
                if card.value == "10":
                    s = s + "\t\t\t\t|  {}            |".format(card.value)
                elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
                    # If it equals -1, 1 or 12 it's a king, queen, jack or ace
                    s = s + "\t\t\t\t|  {}             |".format(card.value[:1])
                elif card.return_numeric_value_cambio() == 0:
                    s = s + "\t\t\t\t|  {}         |".format(card.value)
                else:
                    s = s + "\t\t\t\t|  {}             |".format(card.value)
            elif any(str(key) == str(x) for x in game_player.known_cards):
                if card.value == "10":
                    s = s + "\t|  {}            |".format(card.value)
                elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
                    # If it equals -1, 1 or 12 it's a king, queen, jack or ace
                    s = s + "\t|  {}             |".format(card.value[:1])
                elif card.return_numeric_value_cambio() == 0:
                    s = s + "\t|  {}         |".format(card.value)
                else:
                    s = s + "\t|  {}             |".format(card.value)
            else:
                s += "\t|                |"

        card = game_dealer.disposed[-1]
        if card.value == "10":
            s = s + "\t\t\t\t|  {}            |".format(card.value)
        elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
            # If it equals -1, 1 or 12 it's a king, queen, jack or ace
            s = s + "\t\t\t\t|  {}             |".format(card.value[:1])
        elif card.return_numeric_value_cambio() == 0:
            s = s + "\t\t\t\t|  {}         |".format(card.value)
        else:
            s = s + "\t\t\t\t|  {}             |".format(card.value)
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|      * *       |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|    *     *     |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|   *       *    |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|   *       *    |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if str(key) == "5":
                if value.suit:
                    val = "\u2664"
                    if str(value.suit).lower() == "hearts":
                        val = "\u2661"
                    if str(value.suit).lower() == "clubs":
                        val = "\u2667"
                    if str(value.suit).lower() == "diamonds":
                        val = "\u2662"
                    s = s + "\t\t\t\t|       {}        |".format(val)
                else:
                    s = s + "\t\t\t\t|                |"
            elif any(str(key) == str(x) for x in game_player.known_cards):
                if value.suit:
                    val = "\u2664"
                    if str(value.suit).lower() == "hearts":
                        val = "\u2661"
                    if str(value.suit).lower() == "clubs":
                        val = "\u2667"
                    if str(value.suit).lower() == "diamonds":
                        val = "\u2662"
                    s = s + "\t|       {}        |".format(val)
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|          *     |"
        value = game_dealer.disposed[-1]
        if value.suit:
            val = "\u2664"
            if str(value.suit).lower() == "hearts":
                val = "\u2661"
            if str(value.suit).lower() == "clubs":
                val = "\u2667"
            if str(value.suit).lower() == "diamonds":
                val = "\u2662"
            s = s + "\t\t\t\t|       {}        |".format(val)
        else:
            s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|         *      |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|        *       |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|                |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|                |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if str(key) == "5":
                if card.value == "10":
                    s = s + "\t\t\t\t|            {}  |".format(card.value)
                elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
                    # If it equals -1, 1 or 12 it's a king, queen, jack or ace
                    s = s + "\t\t\t\t|            {}   |".format(card.value[:1])
                elif card.return_numeric_value_cambio() == 0:
                    s = s + "\t\t\t\t|         {}  |".format(card.value)
                else:
                    s = s + "\t\t\t\t|            {}   |".format(card.value)
            elif any(str(key) == str(x) for x in game_player.known_cards):
                if card.value == "10":
                    s = s + "\t|            {}  |".format(card.value)
                elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
                    # If it equals -1, 1 or 12 it's a king, queen, jack or ace
                    s = s + "\t|            {}   |".format(card.value[:1])
                elif card.return_numeric_value_cambio() == 0:
                    s = s + "\t|         {}  |".format(card.value)
                else:
                    s = s + "\t|            {}   |".format(card.value)
            else:
                s += "\t|        *       |"
        card = game_dealer.disposed[-1]
        if card.value == "10":
            s = s + "\t\t\t\t|            {}  |".format(card.value)
        elif any(card.return_numeric_value_cambio() == x for x in [12, 1, -1]):
            # If it equals -1, 1 or 12 it's a king, queen, jack or ace
            s = s + "\t\t\t\t|            {}   |".format(card.value[:1])
        elif card.return_numeric_value_cambio() == 0:
            s = s + "\t\t\t\t|         {}  |".format(card.value)
        else:
            s = s + "\t\t\t\t|            {}   |".format(card.value)
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if str(key) == "5":
                s = s + "\t\t\t\t ________________"
            else:
                s = s + "\t ________________"
        s = s + "\t\t\t\t ________________"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if str(key) == "5":
                    if card.return_numeric_value_cambio() > 10 or card.return_numeric_value_cambio() < 0:
                        s = s + "\t\t\t\t       ({})       ".format(str(card.return_numeric_value_cambio()))
                    else:
                        s = s + "\t\t\t\t        ({})       ".format(str(card.return_numeric_value_cambio()))
                else:
                    if card.return_numeric_value_cambio() > 10 or card.return_numeric_value_cambio() < 0:
                        s = s + "\t       ({})     ".format(str(card.return_numeric_value_cambio()))
                    else:
                        s = s + "\t       ({})      ".format(str(card.return_numeric_value_cambio()))
            else:
                s = s + "\t       ({})      ".format("?")
        s = s + "\t\t\t\t        ({})    ".format(str(game_dealer.disposed[-1].return_numeric_value_cambio()))
        print(s)

        print()