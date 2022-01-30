from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
# Python program to implement client side of chat room.
import socket
import select
import sys

from cards.CreateDeck import create_deck
from cambio_multiplayer.Instance_Server.server_code import server
from comms_client.client_user_hand import UserHand

# Flask is a lightweight rest API
app = Flask(__name__)
api = Api(app)

class GameInstance:
    def __init__(self):
        self.active_player_count = 0

        # Variables to setup server connection / make a public server
        self.server_ip = None
        self.__server_port = int(7789)      # Should never be changed
        self.server_conn = None
        self.is_server = False

        self.server_flask = None

        # Contains the player ID and obj
        self.players = {}
        self.deck_instance = None

    def start_player(self):
        """
        Function to setup a new player.
        Must instanciate a new connection with server
        """
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_ip = str("127.0.0.1")
        self.server_conn.connect((self.server_ip, self.__server_port))

        # Adding resources to the flask api for the client
        api.add_resource(UserHand, "/card/<int:card_id>")

        # now we've an establied connection, the game can reference an IP address for the flask connection
        # Default address / port for flask is below
        # BASE = "http://127.0.0.1:5000/"

        # sending a get request to the url with the additional information attached
        # response = requests.put(BASE + "video/20")

        # printing the json response returned
        # print(response)
        # self.server_conn.close()

    def start_server(self):
        server_instance = server()
        server_instance.server_setup()

    # def reset_game(self):
    #     self.active_player_count = 0
    #     self.players = {}

