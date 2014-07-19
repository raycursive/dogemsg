import json

class Contact:
    def __init__ (self, key, name = "", alias = "", email = ""):
        self.name = name
        self.alias = alias
        self.email = email
        self.key = key

    def __repr__(self):
        return json.dumps(self.get_information())

    def get_information(self):
        return {"name" : self.name,
                "alias" : self.alias,
                "email" : self.email,
                "key" : self.key
            }
