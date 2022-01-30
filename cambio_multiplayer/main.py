# from Game.GameInstance import GameInstance
import argparse

def main():
    parser = argparse.ArgumentParser(description='Cambio parameters')
    # added argument for starting application in server / client mode
    parser.add_argument("--server", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    Instance = GameInstance()
    if args.server:
        Instance.start_server()
    else:
        Instance.start_player()



if __main__ == "__main__":
    main(sys.argv[1:])