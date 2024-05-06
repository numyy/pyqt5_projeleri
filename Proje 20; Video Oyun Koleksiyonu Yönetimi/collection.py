class Collection:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def remove_game(self, game):
        self.games.remove(game)

    def get_recommendations(self):
        recommendations = []
        for game in self.games:
            if game.get_average_rating() >= 4:
                recommendations.append(game)
        return recommendations