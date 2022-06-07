from cambio.Cambio_game.game_instance_transformed import gameInstance
from cambio.Cambio_game.client.client_main import client_main

import sys

def main():
    list_of_arguments = sys.argv

    if "-server" in list_of_arguments:
        x = main_server()
        x.start()
    else:
        x = client_main()
        x.start("name1")

if __name__ == "__main__":
    main()