# Calendar_Puzzle
In a calendar like the one below and with the given eight pieces, the task is to use all of the pieces so the remaining cells show the date. There are multiple solutions for each day of the year (rotating and flipping pieces is allowed). This code does this by brute force, checking all possible different positions. There are 96 different ways in which you can place piece A, 98 for B, 82 for C, 154 for D, 151 for E, 80 for F, 196 for G and 154 for H (pieces with simmetries have less possible locations).

![Calendar grid](https://github.com/jccabrejas/Calendar_Puzzle/blob/71b67f322840a25d493106abc5067c659a00e11c/images/calendar_puzzle.png)
![Pieces](https://github.com/jccabrejas/Calendar_Puzzle/blob/71b67f322840a25d493106abc5067c659a00e11c/images/calendar_puzzle_pieces.png)

One example for December 19th

![Example](https://github.com/jccabrejas/Calendar_Puzzle/blob/de5e0c40a9e1bad7595508b7389190415c65d1aa/images/Dec-19_017.png)

The code also includes a Twitter bot which (I hope) will tweet one of the solutions for each day at 7am UTC, mostly following [this tutorial from Miguel Garcia](https://realpython.com/twitter-bot-python-tweepy/) using [Tweepy](https://github.com/tweepy/tweepy)

Link to the Twitter account of the [Calender Puzzle Bot](https://twitter.com/CalendarPuzzle)
