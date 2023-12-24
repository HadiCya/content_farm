import random
import billboard


def get_random_artist(billboard_charts):
    billboard_chart = random.choice(billboard_charts)
    chart = billboard.ChartData(billboard_chart[0], year=billboard_chart[1])
    artist = chart[random.randint(0, len(chart)-1)].artist

    print(f"Selecting: {artist}")
    return artist
