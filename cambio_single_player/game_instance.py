import os

from cambio_multiplayer.dealer.cambio_dealer import cambio_dealer
from player_obj import player


class gameInstance:

    def __init__(self):
        self.accepted_vals = ["1", "2", "c", "q"]
        self.players = {}
        self.number_of_players = 1
        self.game_dealer = cambio_dealer()

        self.game_ongoing = False

    def deal_cards(self):

        for i in range(int(self.number_of_players)):
            game_player = player()
            for x in range(4):
                game_player.cards[x + 1] = self.game_dealer.deal_card()
                game_player.cards[x + 1].set_player_card()
            game_player.name = game_player.name + str(int(i + 1))
            self.players[i + 1] = game_player


    def start(self):
        self.game_ongoing = True
        self.game_dealer.get_cards()
        self.game_dealer.shuffle_cards()

        self.choose_number_of_players()

        self.deal_cards()

        self.game_dealer.despose_first_card()

        while self.game_ongoing:
            for player_id, player in self.players.items():

                os.system("cls")

                if self.player_turn(player):

                    print("Value of hand = ")
                    x = 0
                    for idx, player_card in game_player.cards.items():
                        print("Card : " + str(player_card))
                        x += player_card.return_numeric_value_cambio()
                    print(x)

    def player_turn(self, player):
        print(f"PLAYER : {player.name}")
        response = ""
        # while not response.lower() == "c" and not response.lower() == "q":

        print("")
        print("Current disposed card '" + str(self.game_dealer.disposed[-1]) + "'")
        print("Count of cards left : " + str(len(self.game_dealer.deck)))

        self.display_hand(player)

        new_card = None
        try:
            new_card = self.game_dealer.deal_card()
        except:
            print("Out of cards!!")
            return False

        count = len(player.cards.keys())
        player.cards[count] = new_card

        print("NEW : " + str(player.cards[count]))

        self.print_cards(player, self.game_dealer)

        self.check_if_player_has_card_to_dispose(player, self.game_dealer)

        if len(player.cards) == 0:
            print("Player has no cards left in hand!")
            return False

        response = self.choice()
        if response.lower() == "c" or response.lower() == "q":
            return True

        if str(response) == "1":
            print("Discarded card : " + str(player.cards[count]))
            self.game_dealer.disposed.append(player.cards[count])
            del (player.cards[count])

            self.print_cards(player, self.game_dealer)
            self.display_hand(player)

        if str(response) == "2":
            # Keep card - remove from hand for time being
            drawn_card = player.cards[count]
            del (player.cards[count])

            print("Select card to swap with: ")
            print("( Cards Available : " + ",".join(player.cards.keys()) + " )")
            card_swap = input("Enter index of card > ")
            while not any(str(card_swap) == str(x) for x in player.cards.keys()):
                print("Unaccepted entry, please enter another option")
                print("( Cards Available : " + ",".join(player.cards.keys()) + " )")
                card_swap = input("Enter index of card > ")

            # Add the chosen card to the discard pile
            self.game_dealer.disposed.append(player.cards[card_swap])
            # Swap the chosen card with the drawn card
            player.cards[card_swap] = drawn_card

            if not any(str(card_swap) == x for x in player.known_cards):
                player.known_cards.append(str(card_swap))

                self.print_cards(player, self.game_dealer)
                self.display_hand(player)

    def choose_number_of_players(self):
        while True:
            self.number_of_players = input("Enter number of players > ")
            try:
                # Convert it into integer
                val = int(self.number_of_players)
                if not 0 < val <= 4:
                    print("Unaccepted entry, requires 1-4 players. Please enter another option")
                    continue

                # Break out of the input loop
                self.number_of_players = int(self.number_of_players)
                break
            except ValueError:
                print("Unaccepted entry, enter a number between 1 and 4.")

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
            if game_dealer.disposed[-1].value == game_player.cards[int(item)].value:
                # There is a card in the player's hand of equal value to that of the top most discarded
                print(f"Your card ({str(game_player.cards[item])}) is of similar value to card on top of discard pile.\n Do you wish to discard?")
                discard = input("Enter (y)es or (n)o > ")

                while not any(x in str(discard).lower() for x in ["y","n"] ):
                    print("Bad entry, please try again")
                    discard = input("Enter (y)es or (n)o > ")

                # If the player wishes to discard
                if str(discard).lower() == "y":
                    print("Tossing your card to pile")
                    # Append the card to the top of discard pile
                    game_dealer.disposed.append(game_player.cards[item])
                    # remove the card from the player's known cards
                    cards_to_remove.append(item)
                    # remove the card from the player's hand
                    del(game_player.cards[item])

                    svd_crd = game_player.cards.popitem()

                    self.display_hand(game_player)

                    game_player.cards[svd_crd[0]] = svd_crd[1]
                else:
                    print("Player has chosen not to discard card.")

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
                print(f"{idx} : {str(item)}")

    # Function to print the cards
    def print_cards(self, game_player, game_dealer):

        s = ""
        print(s)
        for key, card in game_player.cards.items():

            if not game_player.cards[key].player_card:
                s = s + "\t\t\t\t       {}      ".format(str("NEW"))
            else:
                s = s + "\t        #{}       ".format(key)
        s = s + "\t\t\t\t     {}    ".format("Discarded")
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if not game_player.cards[key].player_card:
                s = s + "\t\t\t\t ________________"
            else:
                s = s + "\t ________________"
        s = s + "\t\t\t\t ________________"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if not game_player.cards[key].player_card:
                s = s + "\t\t\t\t|                |"
            else:
                s = s + "\t|                |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|   *       *    |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, value in game_player.cards.items():
            if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
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
                if not game_player.cards[key].player_card:
                    s = s + "\t\t\t\t|                |"
                else:
                    s = s + "\t|                |"
            else:
                s += "\t|                |"
        s = s + "\t\t\t\t|                |"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if not game_player.cards[key].player_card:
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
            if not game_player.cards[key].player_card:
                s = s + "\t\t\t\t ________________"
            else:
                s = s + "\t ________________"
        s = s + "\t\t\t\t ________________"
        print(s)

        s = ""
        for key, card in game_player.cards.items():
            if any(str(key) == str(x) for x in game_player.known_cards):
                if not game_player.cards[key].player_card:
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