import os
import time

from cambio.Cambio_game.server.player.PlayerObj import player
from cambio.Cambio_game.server.dealer.cambio_dealer import cambio_dealer
from cambio.Cambio_game.generic.commsIO.commsGlobals import commsGlobals
from cambio.Cambio_game.generic.commsIO.DealerRequests import *
from cambio.Cambio_game.generic.commsIO.jsonIO import *


class GameInstance():
    def __init__(self):
        self.number_of_players = 1
        self.game_dealer = cambio_dealer()
        self.game_ongoing = False

        self.current_player = None
        self.awaiting_response = True

        self.time_since_last_send = time.time()

        self.players = []

    def add_players(self):
        for item in commsGlobals.connections:
            new_player = player()
            new_player.name = item[0]
            self.players.append(new_player)
            # name of player and their object
            # self.players[item[0]] = player()

    def deal_cards(self):

        for player in self.players:
            for x in range(4):
                player.cards[x + 1] = self.game_dealer.deal_card()
                player.cards[x + 1].set_player_card()

            # game_player.name = game_player.name + str(int(i + 1))
            # self.players[i + 1] = game_player

    def reset_game_player_vars(self):
        self.current_player = None
        self.awaiting_response = False

    def start_game(self):
        self.add_players()
        self.game_dealer.get_cards()
        self.game_dealer.shuffle_cards()
        self.deal_cards()
        self.game_dealer.dispose_first_card()

        for player in self.players:
            self.reset_game_player_vars()

            self.current_player = player

            print(player.name, player)

            os.system("cls")

            if self.player_turn():

                print("Value of hand = ")
                x = 0
                for idx, player_card in game_player.cards.items():
                    print("Card : " + str(player_card))
                    x += player_card.return_numeric_value_cambio()
                print(x)

            for new_player_id, new_player in self.players.items():
                if player != new_player:
                    self.check_if_player_has_card_to_dispose(new_player, self.game_dealer)


    def send_current_hand(self):
        deck = self.current_player.cards

    def send_to_current_player(self, msg):

        if time.time() - self.time_since_last_send < 1:
            time.sleep(0.5)

        self.time_since_last_send = time.time()


        for item in commsGlobals.connections:
            if self.current_player.name == item[0]:
                try:
                    # Make into json
                    msg = convert_dict_to_str(msg)

                    if not isinstance(msg, bytes):
                        print(msg)
                        print(type(msg))
                        msg = str(msg).encode()

                    item[1].send(msg)
                except Exception as err:
                    print(err)

    # def display_hand(self, game_player):
    #     print("\ncurrent hand:")
    #     for idx, item in game_player.cards.items():
    #         if not any(str(idx) == str(x) for x in game_player.known_cards):
    #             print(f"{idx} \t\t : ?????")
    #         else:
    #             print(f"{idx} \t\t : {str(item)}")
    #
    #     print(f"Disposed : {self.game_dealer.disposed[-1]}")


    def player_turn(self):
        print(f"\nPLAYER : {self.current_player.name}")
        response = ""
        # while not response.lower() == "c" and not response.lower() == "q":

        # print("")
        # print("Current disposed card '" + str(self.game_dealer.disposed[-1]) + "'")
        print("Count of cards left : " + str(len(self.game_dealer.deck)))

        # self.display_hand(current_player)
        self.send_to_current_player(notify_user_turn(True))
        self.send_to_current_player(display_current_hand(dict(self.current_player.cards), self.current_player.known_cards))

        new_card = None
        try:
            new_card = self.game_dealer.deal_card()
        except:
            print("Out of cards!!")
            return False

        count = len(self.current_player.cards.keys()) + 1
        self.current_player.cards[count] = new_card

        print("Drawn \t : " + str(self.current_player.cards[count]))

        self.send_to_current_player( display_new_draw(new_card))
        self.send_to_current_player( display_last_disposed(self.game_dealer.disposed[-1]))

        if len(self.current_player.cards) == 0:
            print("Player has no cards left in hand!")

            return False


        # function to send and await response from correct player
        self.choice()

        #
        # if response.lower() == "c" or response.lower() == "q":
        #     return True
        #
        # if str(response) == "1":
        #     print("Discarded card : " + str(current_player.cards[count]))
        #     self.game_dealer.disposed.append(current_player.cards[count])
        #     del (current_player.cards[count])
        #
        #     # self.print_cards(current_player, self.game_dealer)
        #     self.display_hand(current_player)
        #
        # if str(response) == "2":
        #     # Keep card - remove from hand for time being
        #     drawn_card = current_player.cards[count]
        #     del (current_player.cards[count])
        #
        #     print("Select card to swap with: ")
        #     # print(f"( Cards Available : {current_player.cards.keys()} )")
        #     card_swap = input("Enter index of card > ")
        #     while not any(str(card_swap) == str(x) for x in current_player.cards.keys()):
        #         print("Unaccepted entry, please enter another option")
        #         print("( Cards Available : " + ",".join(current_player.cards.keys()) + " )")
        #         card_swap = input("Enter index of card > ")
        #
        #     # Add the chosen card to the discard pile
        #     self.game_dealer.disposed.append(current_player.cards[int(card_swap)])
        #     # Swap the chosen card with the drawn card
        #     current_player.cards[int(card_swap)] = drawn_card
        #
        #     if not any(int(card_swap) == x for x in current_player.known_cards):
        #         current_player.known_cards.append(int(card_swap))
        #
        #         # self.print_cards(current_player, self.game_dealer)
        #         self.display_hand(current_player)
        #
        # return False

    def choice(self):

        self.awaiting_response = True
        self.choice_response = None

        user_choice = {}
        for key, value in self.current_player.cards.items():
            # note to self - Because you overwrote the str value of the cards
            # this should be a safe way to display the card you want
            user_choice[key] = "Replace card : " + str(value)

        user_choice["d"] = "Discard new card!"
        user_choice["c"] = "CAMBIO!!!"
        # this can be re-added once it's correctly implemented!
        # user_choice["q"] = "Quit!"

        self.send_to_current_player( request_choice_new_draw(user_choice) )

        while self.awaiting_response:
            time.sleep(1)

        # Once the user had responded to the choice, the main_server class deals with the card discard
        # meaning once everthing it done, we can just move onto the next player's turn





# from flask import Flask
# from flask_restful import Resource, Api, abort, reqparse
# # Python program to implement client side of chat room.
# import socket
# import select
# import sys
#
# from cards.CreateDeck import create_deck
# from cambio_multiplayer.Instance_Server.server_code import server
# from comms_client.client_user_hand import UserHand
#
# # Flask is a lightweight rest API
# app = Flask(__name__)
# api = Api(app)
#
# class GameInstance:
#     def __init__(self):
#         self.active_player_count = 0
#
#         # Variables to setup server connection / make a public server
#         self.server_ip = None
#         self.__server_port = int(7789)      # Should never be changed
#         self.server_conn = None
#         self.is_server = False
#
#         self.server_flask = None
#
#         # Contains the player ID and obj
#         self.players = {}
#         self.deck_instance = None
#
#     def start_player(self):
#         """
#         Function to setup a new player.
#         Must instanciate a new connection with server
#         """
#         self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         self.server_ip = str("127.0.0.1")
#         self.server_conn.connect((self.server_ip, self.__server_port))
#
#         # Adding resources to the flask api for the client
#         api.add_resource(UserHand, "/card/<int:card_id>")
#
#         # now we've an establied connection, the game can reference an IP address for the flask connection
#         # Default address / port for flask is below
#         # BASE = "http://127.0.0.1:5000/"
#
#         # sending a get request to the url with the additional information attached
#         # response = requests.put(BASE + "video/20")
#
#         # printing the json response returned
#         # print(response)
#         # self.server_conn.close()
#
#     def start_server(self):
#         server_instance = server()
#         server_instance.server_setup()
#
#     # def reset_game(self):
#     #     self.active_player_count = 0
#     #     self.players = {}
#
