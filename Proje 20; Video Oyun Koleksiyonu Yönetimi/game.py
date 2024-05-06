class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform
        self.ratings = []

    def add_rating(self, rating):
        self.ratings.append(rating)

    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)