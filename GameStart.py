from Game.GameInstance import GameInstance
import argparse, sys

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument("foo", ..., required=True)
# parser.parse_args()

if len(sys.argv) > 1:
    create_server()
else:
    create_client()
