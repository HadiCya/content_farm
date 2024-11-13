import random
import billboard
import config


def get_random_artist():
    # billboard_chart = random.choice([('greatest-alternative-artists', None), ('artist-100', None), ('top-rap-artists', 2023), ('top-rap-artists', None), ('top-r-and-b-hip-hop-artists', 2021), ('top-r-and-b-hip-hop-artists', None)])
    # chart = billboard.ChartData(billboard_chart[0], year=billboard_chart[1])
    # artist = chart[random.randint(0, len(chart)-1)].artist

    # print(f"Selecting: {artist}")
    return "Drake"


def get_5_songs():
    try:
        songs = [song.title for song in billboard.ChartData(
            'r-b-hip-hop-songs')]
        random.shuffle(songs)
        return songs[:5]
    except:
        print("An error occured!")
