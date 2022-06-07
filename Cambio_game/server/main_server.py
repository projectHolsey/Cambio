import socket
import logging
import time
from _thread import *

from cambio.Cambio_game.server.dealer import cambio_dealer
from cambio.Cambio_game.server.Game.GameInstance import GameInstance
from cambio.Cambio_game.generic.commsIO.jsonIO import *
from cambio.Cambio_game.generic.commsIO.commsGlobals import commsGlobals


class main_server():
    def __init__(self):
        self.connection_descriptions = None

        self.max_player_count = 1
        self.packet_size = 4096

        self.accepted_vals = ["1", "2", "c", "q"]
        self.players = []
        self.number_of_players = None
        self.game_dealer = None

        self.game_ongoing = False

        self.server_ip = "0.0.0.0"
        self.port = 9999
        self.server_socket = None

        self.game_instance = None


    def restart(self):
        commsGlobals.connections = []
        self.connection_descriptions = {}

        self.server_socket = None

        self.game_instance = GameInstance()

    def start(self):
        # Reset game variables
        self.restart()

        # Context - Will auto close when finished with socket / program exited
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server_socket:

            try :
                self.server_socket.bind((self.server_ip, self.port))
                self.server_socket.listen()
            except socket.error as err:
                print(err)
                raise ConnectionError("Failed to start server!!")
                return

            while len(commsGlobals.connections) < self.max_player_count or self.game_instance.game_ongoing:
                conn, addr = self.server_socket.accept()
                print(f"Connection from {addr}")

                """
                we need to read to check they're for this server
                we then need to add their connection to list of clients connected
                kick off a thread to listen to each connection constantly(?)
                """
                msg = conn.recv(self.packet_size)

                name = self.parse_setup_request(msg, conn)

                if not name:
                    # discard the connection
                    continue

                self.add_connection(conn, addr, name)

                # Start new background thread to
                start_new_thread(self.background_read_thread, (conn, addr, name))

                # conn.send(b"hello")
                # self.broadcast("HELLO")

            self.game_instance.start_game()


    def parse_setup_request(self, data, conn):
        json_dict = parse_json_in_to_dict(data)

        if "name" in json_dict:
            return json_dict["name"]
        else:
            return None

    def add_connection(self, conn, addr, name):
        # self.connections[name] = conn
        self.connection_descriptions[addr] = {"name": name, "conn": conn}
        commsGlobals.connections.append((name, conn))


    def background_read_thread(self, conn, addr, name):
        logging.debug(f"Starting background thread for client : {addr}")
        disconnect_client = False
        while not disconnect_client:
            try:
                server_in = conn.recv(commsGlobals.packet_size)
                print(server_in)
                if "broadcast" in str(server_in):
                    self.broadcast(bytes(name) + server_in)
                else:
                    self.handle_response(bytes(server_in).decode(), name)


            except Exception as e:
                disconnect_client = True
                print(e)
                print(f"Disconnecting client {addr}")
                break


    def broadcast(self, msg):
        # Adding ability to disable broadcasts during specific events
        if commsGlobals.disable_broadcasts:
            while commsGlobals.disable_broadcasts:
                time.sleep(0.1)

        # Loop through each connection and broadcast the message sent to everyone
        for connection in commsGlobals.connections:
            try:
                if isinstance(msg, bytes):
                    connection[1].send(bytes(msg))
                else:
                    connection[1].send(str(msg).encode())
            except Exception as err:
                commsGlobals.connections.remove(connection)


    def handle_response(self, response, name):
        """
        Potential responses:
         - 'card_to_dispose'    - String
            -> 'dispose'            - Boolean
         - 'choice_response'    - String
        """

        # convert from dict to
        response = parse_json_in_to_dict(response)

        if 'card_to_dispose' in response:
            if str(response['dispose']).lower() == "y":
                # check if card to dispose in player's known cards
                """"""""""""""""""""""""""""""""""""""""""
                # Need to implement this
                self.dispose_card(response["card_to_dispose"], False, name)
        if "choice_response" in response:
            self.handle_choice_response(response["choice_response"], name)

    def handle_choice_response(self, response, name):
        try:
            card_number = int(response)
            self.dispose_card(card_number, False, name)
        except ValueError:
            if "d" in str(response).lower():
                self.dispose_card(None, True, name)
            if "q" in str(response).lower():
                print("someone wants to quit")
            if "c" in str(response).lower():
                print("Someone wants cambio")

        # allow the gameInstance to move onto the next player
        self.game_instance.awaiting_response = False

    def dispose_card(self, number=None, new_draw=False, name=None):
        """
        This method really needs tidying up at some point.
        """
        for player in self.game_instance.players:
            if player.name == name:
                if number in player.cards:
                    # del(player.cards[number])
                    for card in player.cards:
                        if not card.player_card:
                            self.game_instance.game_dealer.disposed.append(player.cards[number])
                            player.cards[number] = card
                            print("replaced player card")
                            return
                elif new_draw:
                    for card in player.cards:
                        if not card.player_card:
                            player.cards.remove(card)
                            print("removed a player's card")
                            return



























# # handle the server side interaction
#
# import socketserver
#
# class main_server(socketserver.BaseRequestHandler):
#
#     # def __init__(self):
#     #     super(main_server, self).__init__()
#         # self.main_player = None
#         #
#         # self.accepted_vals = ["1", "2", "c", "q"]
#         # self.players = {}
#         # self.number_of_players = 1
#         #
#         # self.game_dealer = cambio_dealer()
#         #
#         # self.game_ongoing = False
#
#     def start(self):
#         HOST, PORT = "localhost", 9999
#
#         # Create the server, binding to localhost on port 9999
#         with socketserver.TCPServer((HOST, PORT), main_server) as server:
#             # Activate the server; this will keep running until you
#             # interrupt the program with Ctrl-C
#             server.serve_forever()
#
#     def start_game(self):
#         self.game_ongoing = True
#         self.game_dealer.get_cards()
#         self.game_dealer.shuffle_cards()
#
#         self.choose_number_of_players()
#
#         self.deal_cards()
#
#         self.game_dealer.dispose_first_card()
#
#         while self.game_ongoing:
#             for player_id, player in self.players.items():
#
#                 os.system("cls")
#
#                 if self.player_turn(player):
#
#                     print("Value of hand = ")
#                     x = 0
#                     for idx, player_card in game_player.cards.items():
#                         print("Card : " + str(player_card))
#                         x += player_card.return_numeric_value_cambio()
#                     print(x)
#
#
#                 for new_player_id, new_player in self.players.items():
#                     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#                     if player != new_player:
#                         self.check_if_player_has_card_to_dispose(new_player, self.game_dealer)
#
#
#     def parse_request(self, json_dict):
#         pass
#
#
#     """
#     The request handler class for our server.
#
#     It is instantiated once per connection to the server, and must
#     override the handle() method to implement communication to the
#     client.
#     """
#
#     def handle(self):
#         data = self.request.recv(1024).strip()
#         # just send back the same data, but upper-cased
#         print(data)
#
#         self.request.sendall(data.upper())
#
#         # if self.client_address[0] not in self.players:
#         #     request = {"request" : "name"}
#         #     jsonData = json.dumps(request)
#         #     self.request.sendall(bytes(jsonData))
#         #
#         # else:
#         #     data = self.request.recv(1024).strip()
#         #     self.parse_request(json.loads(data))
#         #     request = {"request": "wait"}
#         #     self.request.sendall(bytes(jsonData))
#
