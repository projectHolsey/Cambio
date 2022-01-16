from Game.GameInstance import GameInstance
import argparse, sys


parser = argparse.ArgumentParser(description='Cambio parameters')
parser.add_argument('--server', choices=["false", "true"], default="false", type=str.lower)
args = parser.parse_args()

Instance = GameInstance
if args.server:
    GameInstance.start_server()
else:
    GameInstance.start_player()
