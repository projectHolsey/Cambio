"""
Class UserAction

###########################
Intention:

Flask API for the user actions.




"""


from flask_restful import Resource, Api, abort, reqparse

# card_args = reqparse.RequestParser()
# card_args.add_argument("value", type=str, required=True)
# card_args.add_argument("suit", type=str, required=True)
# card_args.add_argument("colour", type=str, required=True)
class UserAction(Resource):
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