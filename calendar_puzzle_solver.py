import pickle
import time
from collections import defaultdict

import numpy as np

''' Given 8 pieces, A to H, and a board with
months (rows 1 and 2) and days (rows 3 to partially 7),
find all solutions and store them in a pickled dict.
Pieces can rotate and be flipped

0 [[' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
1  [' ' 'A' 'A' 'B' 'B' 'G' 'G' ' ' ' ']
2  [' ' 'A' ' ' 'B' 'B' 'G' 'G' ' ' ' ']
3  [' ' 'A' 'A' 'B' 'B' 'E' 'G' 'H' ' ']
4  [' ' 'F' 'F' 'F' 'C' 'E' 'H' 'H' ' ']
5  [' ' 'F' 'C' 'C' 'C' 'E' ' ' 'H' ' ']
6  [' ' 'F' 'C' 'D' 'D' 'E' 'E' 'H' ' ']
7  [' ' 'D' 'D' 'D' ' ' ' ' ' ' ' ' ' ']
8  [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']]
     0   1   2   3   4   5   6   7   8 
Each piece has a list with all possible locations where it could fit
each expressed as a set of cells occuppied, each cell is a tuple with the row and column
For example, for above board location of piece A is 
'A':{(1, 2), (2, 1), (3, 1), (1, 1), (3, 2)}

'''

initial_instances = {
    "A": [
        {(1, 1), (1, 2), (2, 1), (3, 1), (3, 2)},
        {(1, 1), (1, 2), (2, 2), (3, 1), (3, 2)},
        {(1, 1), (2, 1), (2, 2), (2, 3), (1, 3)},
        {(1, 1), (2, 1), (1, 2), (2, 3), (1, 3)},
    ],
    "B": [
        {(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)},
        {(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)},
    ],
    "C": [
        {(1, 3), (2, 1), (2, 2), (2, 3), (3, 1)},
        {(1, 1), (2, 1), (2, 2), (2, 3), (3, 3)},
        {(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)},
        {(3, 1), (1, 2), (2, 2), (3, 2), (1, 3)},
    ],
    "D": [
        {(2, 1), (2, 2), (2, 3), (1, 3), (1, 4)},
        {(1, 1), (1, 2), (2, 2), (2, 3), (2, 4)},
        {(1, 1), (2, 1), (2, 2), (3, 2), (4, 2)},
        {(1, 2), (2, 2), (2, 1), (3, 1), (4, 1)},
        {(1, 2), (2, 2), (3, 2), (3, 1), (4, 1)},
        {(1, 1), (2, 1), (3, 1), (3, 2), (4, 2)},
        {(2, 1), (2, 2), (1, 2), (1, 3), (1, 4)},
        {(1, 1), (1, 2), (1, 3), (2, 3), (2, 4)},
    ],
    "E": [
        {(2, 1), (2, 2), (2, 3), (2, 4), (1, 4)},
        {(1, 1), (1, 2), (2, 2), (3, 2), (4, 2)},
        {(2, 1), (1, 1), (1, 2), (1, 3), (1, 4)},
        {(1, 1), (2, 1), (3, 1), (4, 1), (4, 2)},
        {(1, 1), (2, 1), (2, 2), (2, 3), (2, 4)},
        {(4, 1), (4, 2), (3, 2), (2, 2), (1, 2)},
        {(1, 1), (1, 2), (1, 3), (1, 4), (2, 4)},
        {(1, 2), (1, 1), (2, 1), (3, 1), (4, 1)},
    ],
    "F": [
        {(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)},
        {(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)},
        {(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)},
        {(1, 3), (1, 2), (1, 1), (2, 1), (3, 1)},
    ],
    "G": [
        {(1, 1), (2, 1), (3, 1), (2, 2), (3, 2)},
        {(1, 2), (2, 1), (3, 1), (2, 2), (3, 2)},
        {(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)},
        {(2, 1), (1, 2), (1, 3), (2, 2), (2, 3)},
        {(1, 1), (2, 1), (1, 2), (2, 2), (3, 1)},
        {(1, 1), (2, 1), (1, 2), (2, 2), (3, 2)},
        {(1, 1), (2, 1), (1, 2), (2, 2), (1, 3)},
        {(1, 1), (2, 1), (1, 2), (2, 2), (2, 3)},
    ],
    "H": [
        {(1, 1), (1, 2), (1, 3), (1, 4), (2, 3)},
        {(1, 1), (1, 2), (1, 3), (1, 4), (2, 2)},
        {(2, 1), (2, 2), (2, 3), (2, 4), (1, 3)},
        {(2, 1), (2, 2), (2, 3), (2, 4), (1, 2)},
        {(1, 2), (2, 2), (3, 2), (4, 2), (2, 1)},
        {(1, 2), (2, 2), (3, 2), (4, 2), (3, 1)},
        {(1, 1), (2, 1), (3, 1), (4, 1), (2, 2)},
        {(1, 1), (2, 1), (3, 1), (4, 1), (3, 2)},
    ],
}

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
months_locations = {
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
}

days = list(range(1, 32))


def all_possible_positions(pieces):
    """Shift horizontally and vertically each figure"""
    result = dict()
    for letter, variants in pieces.items():
        result[letter] = list()
        letter_rows = letter_cols = 0

        for variant in variants:
            letter_rows = max([n[0] for n in variant])
            letter_cols = max([n[1] for n in variant])

            for i in range(7 - letter_rows + 1):
                for j in range(7 - letter_cols + 1):
                    result[letter].append({(n[0] + i, n[1] + j) for n in variant})
    return result


def left_instances(instances, cells_not_allowed, used_pieces):
    """returns possible locations which are still possible as they don´t overlap with cells not allowed"""
    result = dict()
    for letter, variants in instances.items():
        if letter in used_pieces:
            continue
        result[letter] = list()
        for variant in variants:
            is_variant_allowed = True
            for pos in variant:
                if pos in cells_not_allowed:
                    is_variant_allowed = False
                    break
            if is_variant_allowed:
                result[letter].append(variant)
    return result


def print_calendar(solutions):
    '''solutions is a list of dictionaries, each one listing the cells of each piece
    print_calendars prints the last solution in the list'''
    # solution = solutions[-1]
    calendar = np.zeros((9, 9), dtype="U1")
    calendar[:, :] = " "
    calendar[0, :] = calendar[-1, :] = calendar[:, 0] = calendar[:, -1] = " "
    calendar[0:3, -2] = calendar[-2, 3:] = " "
    sol = solutions[-1]
    for k, v in sol.items():
        for cell in v:
            calendar[cell] = k
    print(calendar, end="", flush=True)


def location_available(variant, cells_not_allowed):
    '''True if cells in variant do not intersect with cell_not_allowed
    TODO use sets!'''
    months_locations = {
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
    }
    if (
        len(set.intersection(months_locations, set.union(cells_not_allowed, variant)))
        == 12
    ):
        return False

    for cell in variant:
        if cell in cells_not_allowed:
            return False
    return True


def solution_found(cells_not_allowed):
    '''All pieces in place and one of the empty cells in top two rows'''
    return (
        len(cells_not_allowed) == 47
        and len(set.intersection(months_locations, cells_not_allowed)) == 11
    )


def still_possible(available_instances):
    '''False if any of remaining pieces has no available locations to be placed in'''
    for k in available_instances.keys():
        if len(available_instances[k]) == 0:
            return False
    return True


def place_next_piece(original, cells_not_allowed, solutions, letter):

    used_pieces = "".join(["".join(list(solutions[-1].keys()))])
    if used_pieces not in "ABCDEFGH":
        return "go back", solutions

    available_instances = left_instances(original, cells_not_allowed, used_pieces)

    for variant in available_instances[letter]:
        if location_available(variant, cells_not_allowed):
            solutions[-1][letter] = variant
            if solution_found(set.union(cells_not_allowed, variant)):
                temp = solutions[-1].copy()
                del temp["H"]
                solutions.append(temp)
                continue
            elif letter != "H":
                _, solutions = place_next_piece(
                    original,
                    set.union(cells_not_allowed, variant),
                    solutions,
                    "ABCDEFGH"["ABCDEFGH".find(letter) + 1],
                )

            del solutions[-1][letter]

    return "go back", solutions


def save_results(solutions):
    '''Save a text file grouping solutions by date plus a pickled dict for further use'''
    cells_not_allowed = {(1, 7), (2, 7), (7, 4), (7, 5), (7, 6), (7, 7)}
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
    day_conversion = dict()
    count = 1
    for r in range(3, 8):
        for c in range(1, 8):
            day_conversion[(r, c)] = str(count)
            count += 1

    result = defaultdict(list)
    with open("result.txt", "w") as f:
        error_count = 0
        for sol in solutions:
            # print_calendar([sol])
            spots = list()
            for r in range(1, 8):
                for c in range(1, 8):
                    if (r, c) not in cells_not_allowed and not any(
                        [(r, c) in sol[k] for k in sol.keys()]
                    ):
                        spots.append((r, c))
            # print(spots)
            if len(spots) != 2:
                continue

            if spots[0][0] < 3:
                month, day = spots[0], spots[1]
            else:
                day, month = spots[0], spots[1]

            label = month_conversion[month] + "-" + day_conversion[day].zfill(2)
            result[label].append(sol)

        with open("calendar_solution_dict.pickle", "wb") as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print(f"{error_count} errors")
        for date in result.keys():
            f.write(date + "\n")
            for sol in result[date]:
                f.write(str(sol) + "\n")
    return None


def main(initial_instances):
    all_instances = all_possible_positions(initial_instances)
    cells_not_allowed = {(1, 7), (2, 7), (7, 4), (7, 5), (7, 6), (7, 7)}
    available_instances = left_instances(
        all_instances, cells_not_allowed, used_pieces=""
    )
    original = available_instances.copy()

    print(
        "Number of possible positions: ",
        sum([len(available_instances[k]) for k in available_instances.keys()]),
    )

    solutions = list()

    letter = "A"
    variants = original[letter]
    used_pieces = letter
    c = 0
    for variant in variants:
        print(time.time())
        c += 1
        if location_available(variant, cells_not_allowed):
            print("\n=======\n", used_pieces[-1], c, end=" - \n", flush=True)
            solutions.append({letter: variant})
            _, solutions = place_next_piece(
                original, set.union(cells_not_allowed, variant), solutions, "B"
            )
        del solutions[-1][letter]
    print(len(solutions))

    save_results(solutions)

    print("Finished!")


if __name__ == "__main__":
    main(initial_instances)


