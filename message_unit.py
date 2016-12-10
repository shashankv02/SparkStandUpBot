class message_unit:
    def __init__(self, text, room_id = None):
        self.text = text
        self.room_id = room_id
        self.response = None