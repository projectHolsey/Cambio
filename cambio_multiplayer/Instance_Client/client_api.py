from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')
conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()


def process_cmd(cmd):
    """
    :param

    Commands that need dealing with on client side.

    1 - Use card ability
     > Server to ask if client wants to use card

    2 - Use ability < insert card abilities >

    3 - Finish round, ask for score / discard cards

    4 - Retrieve new cards.

    """


def send_cmd():
    """
    Commands to be sent from the client to server

    1 - Draw a card
     > Ask server for a card

    2 - Add card to pile
     > Send a discarded card to pile

    3 - Call Cambio
     > Send the cambio flag to server

    4 - (additional) reset game



    """

