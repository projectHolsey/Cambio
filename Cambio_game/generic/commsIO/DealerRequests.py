from cambio.Cambio_game.generic.commsIO.commsGlobals import commsGlobals

def create_msg_dict(response_required=False):

    version = commsGlobals.comms_version
    base = commsGlobals.root_json_server

    return {base: {"version":version}, "response_required":response_required}


def add_msg_type(current_dict={}, type=""):
    current_dict["type"] = type
    return current_dict


def notify_user_turn(user_turn_start=False):
    base_dict = create_msg_dict()
    add_msg_type(base_dict, "notify")

    return_dict = {"user_turn_start": user_turn_start}

    return {**base_dict, **return_dict}


# def notify_hold_broadcasts(stop_broadcast=False):
#     base_dict = create_msg_dict()
#     add_msg_type(base_dict, "notify")
#
#     return_dict = {"stop_broadcast": stop_broadcast}
#
#     return {**base_dict, **return_dict}


def display_current_hand(cards, known_cards):
    base_dict = create_msg_dict()
    add_msg_type(base_dict, "display")

    unlinked = cards.copy()
    for card, value in unlinked.items():
        if card not in known_cards:
            value = "???????"
        else:
            value = str(value)

    return_dict = {"current_hand": cards}

    return {**base_dict, **return_dict}

# items = [{"some_val":1},{"some_val":2}]
# print(display_current_hand(items))

def display_last_disposed(card={}):
    base_dict = create_msg_dict()
    add_msg_type(base_dict, "display")

    return_dict = {"last_disposed": str(card)}

    return {**base_dict, **return_dict}

def display_new_draw(card={}):
    base_dict = create_msg_dict()
    add_msg_type(base_dict, "display")

    return_dict = {"new_draw": str(card)}

    return {**base_dict, **return_dict}


def request_dispose_card(card={}):
    base_dict = create_msg_dict(response_required=True)
    add_msg_type(base_dict, "request")

    return_dict = {"dispose_card": card}

    return {**base_dict, **return_dict}


def request_choice_new_draw(choice={}):
    base_dict = create_msg_dict(response_required=True)
    add_msg_type(base_dict, "request")

    return_dict = {"choice": choice}

    return {**base_dict, **return_dict}