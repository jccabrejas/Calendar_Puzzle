import argparse
import configparser
import datetime
import os
import pathlib
import pickle
import sys
from itertools import product
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import tweepy
from matplotlib import colors


def read_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def get_grid(sol):
    grid = np.zeros((9, 9))

    grid[:, :] = 0
    value = 50
    for _, v in sorted(sol.items()):
        for r, c in v:
            grid[r, c] = value
        value += 50
    return np.flipud(grid)


def get_text_conversion():
    text_conversion = dict()
    for p in product(range(1, 9), range(1, 9)):
        text_conversion[p] = ""

    month_conversion = {
        (1, 1): "Jan",
        (1, 2): "Feb",
        (1, 3): "Mar",
        (1, 4): "Apr",
        (1, 5): "May",
        (1, 6): "Jun",
        (2, 1): "Jul",
        (2, 2): "Aug",
        (2, 3): "Sep",
        (2, 4): "Oct",
        (2, 5): "Nov",
        (2, 6): "Dec",
    }
    for coords, month in month_conversion.items():
        text_conversion[coords] = month

    count = 1
    for r in range(3, 8):
        for c in range(1, 8):
            if count < 32:
                text_conversion[(r, c)] = str(count).zfill(2)
            count += 1
    return text_conversion


def get_cell_contours(cell):
    r, c = cell
    return [c, c, c + 1, c + 1, c], [8 - r, 8 - r + 1, 8 - r + 1, 8 - r, 8 - r]


def get_key_by_value(mydict, value):
    return list(mydict.keys())[list(mydict.values()).index(value)]


def make_plot(grid, text_conversion, cells, month, day, suffix):
    cmap = colors.ListedColormap(['white','tomato','yellow','lawngreen','lightblue','indianred', 'violet', 'mediumpurple', 'orange'])
    fig, ax = plt.subplots()
    ax.pcolormesh(grid, cmap=cmap, edgecolors="k", linewidths=1)

    for r, c in text_conversion.keys():
        ax.text(r + 0.3, 8 - c + 0.3, text_conversion[(c, r)])

    ax.plot(cells[0], cells[1], c="black", linewidth=4)
    ax.plot(cells[2], cells[3], c="red", linewidth=4)
    ax.plot(cells[4], cells[5], c="red", linewidth=4)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title(f'{month} - {day} (version {suffix})')
    
    p = pathlib.Path(month)
    p.mkdir(parents=True, exist_ok=True)
    p = pathlib.Path(month+'/'+day)
    p.mkdir(parents=True, exist_ok=True)

    plt.savefig(f'{month}/{day}/{month}-{day}_{suffix}.png')
    plt.close(fig)

def get_contours(text_conversion, month, day):
    month_cell = get_key_by_value(text_conversion, month)
    day_cell = get_key_by_value(text_conversion, day)
    contour_month_x, contour_month_y = get_cell_contours(month_cell)
    contour_day_x, contour_day_y = get_cell_contours(day_cell)
    contour_calendar_x = [1, 1, 7, 7, 8, 8, 4, 4, 1]
    contour_calendar_y = [1, 8, 8, 6, 6, 2, 2, 1, 1]
    return [
        contour_calendar_x,
        contour_calendar_y,
        contour_month_x,
        contour_month_y,
        contour_day_x,
        contour_day_y,
    ]


def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    try:
        filename = os.path.join(os.getcwd(), filename)
        config.read(filename)
    except FileNotFoundError:
        print('config.ini file not found')
        sys.exit()
    return config


def post_tweet(month, day, message, suffix):

    config = read_config()
    bot_key = config['bot_credentials']['bot_consumer_key']
    bot_secret = config['bot_credentials']['bot_consumer_secret']
    token = config['bot_credentials']['bot_access_token']
    token_secret = config['bot_credentials']['bot_access_token_secret']

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(bot_key, bot_secret)
    auth.set_access_token(token, token_secret)

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Error during authentication")
        sys.exit()


    filename = f'{month}/{day}/{month}-{day}_{suffix}.png'
    media = api.media_upload(filename)
    sleep(30)
 
    # https://stackoverflow.com/questions/70129448/how-to-create-tweet-using-tweepy-api-v-2/76509550#76509550
    newapi = tweepy.Client(
        consumer_key=bot_key,
        consumer_secret=bot_secret,
        access_token=token,
        access_token_secret=token_secret)
    newapi.create_tweet(text = message, media_ids = [media.media_id])
    return None

def main():
    parser = argparse.ArgumentParser()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    parser.add_argument("--month", help=str(months),
        choices=months, type=str)
    parser.add_argument("--day", help="1, 2, ..., 31",
        choices=list(range(1,32)), type=int)
    args = parser.parse_args()
    solutions = read_data("calendar_solution_dict.pickle")

    mydate = datetime.datetime.now()
    month = mydate.strftime("%b")
    day = mydate.strftime("%d").zfill(2)

    if args.month and args.day:
        month = args.month
        day = str(args.day).zfill(2)

    label = f'{month}-{day}'
    n = len(solutions[label])
    r = random.randrange(0,n)
    sol = solutions[label][r]
    suffix = f'{r}_of_'+ str(len(solutions[label]))
    message = f'#{r} of ' + str(len(solutions[label])) + ' solutions. Feel free tto reply with your own solution! #apuzzleaday'

    text_conversion = get_text_conversion()
    contours = get_contours(text_conversion, month, day)

    make_plot(get_grid(sol), text_conversion, contours, month, day, suffix)
    post_tweet(month, day, message, suffix)
    print('Tweet sent!')

if __name__ == "__main__":
    main()
