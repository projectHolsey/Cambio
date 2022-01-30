"""
In here I'm going to attempt to create a short version of 'dealing' a hand to a user

There will be some use cases where you need to take additional cards - I would say just grab the highest number in the
 list / dict and + 1
"""

from flask import Flask
from flask_restful import Resource, Api, abort, reqparse


# # Flask is a lightweight rest API
# app = Flask(__name__)
# api = Api(app)

# Can hold up to 4 cards
user_hand = {}

dealing_cards = True

card_args = reqparse.RequestParser()
card_args.add_argument("value", type=str, required=True)
card_args.add_argument("suit", type=str, required=True)
card_args.add_argument("colour", type=str, required=True)
"""
parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')
args = parser.parse_args()"""

class UserHand(Resource):
    # Methods for get, post, put, patch, delete.
    def get(self, card_id):
        return user_hand[card_id]

    def put(self, card_id):
        if dealing_cards:
            # if len(user_hand) == 4:
            if len(user_hand) == 4:
                abort(409)
                return
            card_number = len(user_hand)
            try:
                card = card_args.parse_args()
                user_hand[card_number + 1] = card
                return '', 202
            except Exception as e:
                print(e)

    def delete(self, card_id):
        if card_id in user_hand:
            del(user_hand[card_id])
            return '', 202
        else:
            return '', 404

    def patch(self, card_id):
        new_card = card_args.parse_args()
        found = False
        if card_id not in user_hand:
            abort(404)

        # replace with new card
        user_hand[card_id] = new_card
        return '', 202



# if __name__ == '__main__':
#     app.run(debug=True)