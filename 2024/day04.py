if __name__ == "__main__":
    # parse input
    with open("data/day04.txt") as input_file:
        input_data = input_file.read()

    arr = [list(row) for row in input_data.split("\n")]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    total_occurrences = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == "X":
                for d in directions:
                    di, dj = d
                    x, y = i + di, j + dj
                    for s in "MAS":
                        if (
                            0 <= x < len(arr)
                            and 0 <= y < len(arr[0])
                            and arr[x][y] == s
                        ):
                            x += di
                            y += dj
                        else:
                            # exit early if index out of bounds or letter out of
                            # sequence is found
                            break
                    else:
                        # only increment if for loop completes without breaking,
                        # indicating a full sequence was found
                        total_occurrences += 1
    print(f"Part 1: {total_occurrences}")

    total_occurrences = 0
    diagonals = [
        ((1, 1), (0, 0), (-1, -1)),
        ((-1, 1), (0, 0), (1, -1)),
    ]
    # find each "A" and check both its diagonals for "SAM" or "MAS"
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == "A":
                for diagonal in diagonals:
                    letters = ""
                    for offset in diagonal:
                        di, dj = offset
                        x, y = i + di, j + dj
                        if 0 <= x < len(arr) and 0 <= y < len(arr[0]):
                            letters += arr[x][y]
                        else:
                            # exit early if out of bounds
                            break
                    if letters == "SAM" or letters == "MAS":
                        # check the other diagonal
                        continue
                    else:
                        # invalid sequence found, go to next cell
                        break
                else:
                    # only increment if for loop completes without breaking, anytime
                    # a break is made in the for loop an invalid sequence was found
                    # and we should just go to the next cell
                    total_occurrences += 1
    print(f"Part 2: {total_occurrences}")
