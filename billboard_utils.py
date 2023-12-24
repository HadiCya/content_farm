import random
import billboard


def get_random_artist(billboard_charts):
    charts = []

    for billboard_chart in billboard_charts:
        charts.append(billboard.ChartData(
            billboard_chart[0], year=billboard_chart[1]))

    chart = random.choice(charts)
    artist = chart[random.randint(0, len(chart)-1)].artist

    print(f"Selecting: {artist}")
    return artist
