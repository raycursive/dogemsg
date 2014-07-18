import json

class contact:
    def __init__ (self, key, name = "", alias = ""):
        self.name = name
        self.alias = alias
        self.key = key

    def __repr__(self):
        return json.dumps(self.get_information())

    def get_information(self):
        return {"name" : self.name,
                  "alias" : self.alias,
                  "key" : self.key
            }
