class message_unit:
    def __init__(self, text, room_id = None, email = None, response = None):
        self.text = text
        self.room_id = room_id
        self.response = response
        self.person_email = email
        self.purpose = None