import random
import billboard
import config


def get_random_artist():
    billboard_chart = random.choice(config.BILLBOARD_CHARTS)
    chart = billboard.ChartData(billboard_chart[0], year=billboard_chart[1])
    artist = chart[random.randint(0, len(chart)-1)].artist

    print(f"Selecting: {artist}")
    return artist
