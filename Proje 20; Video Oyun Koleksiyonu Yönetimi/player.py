from collection import Collection
class Player:
    def __init__(self, name):
        self.name = name
        self.collection = Collection()
        self.favorite_games = []