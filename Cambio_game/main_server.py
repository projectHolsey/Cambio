# handle the server side interaction

import socketserver

class main_server(socketserver.BaseRequestHandler):

    # def __init__(self):
    #     super(main_server, self).__init__()
        # self.main_player = None
        #
        # self.accepted_vals = ["1", "2", "c", "q"]
        # self.players = {}
        # self.number_of_players = 1
        #
        # self.game_dealer = cambio_dealer()
        #
        # self.game_ongoing = False

    def start(self):
        self.game_ongoing = True
        self.game_dealer.get_cards()
        self.game_dealer.shuffle_cards()

        self.choose_number_of_players()

        self.deal_cards()

        self.game_dealer.dispose_first_card()

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


                for new_player_id, new_player in self.players.items():
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    if player != new_player:
                        self.check_if_player_has_card_to_dispose(new_player, self.game_dealer)


    def parse_request(self, json_dict):
        pass


    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        data = self.request.recv(1024).strip()
        # just send back the same data, but upper-cased
        print(data)

        self.request.sendall(data.upper())
        # if self.client_address[0] not in self.players:
        #     request = {"request" : "name"}
        #     jsonData = json.dumps(request)
        #     self.request.sendall(bytes(jsonData))
        #
        # else:
        #     data = self.request.recv(1024).strip()
        #     self.parse_request(json.loads(data))
        #     request = {"request": "wait"}
        #     self.request.sendall(bytes(jsonData))



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), main_server) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()