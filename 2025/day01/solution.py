# filename = "sample.txt"
filename = "data.txt"


if __name__ == "__main__":
    with open(filename, "r") as f:
        lines = f.read()
    operations = []
    dial_position = 50
    times_at_zero = 0
    times_crossed_zero = 0
    for line in lines.split("\n"):
        value_sign = +1 if line[0] == "R" else -1
        value = int(line[1:])
        operation = value_sign * value
        dial_position_prev = dial_position
        dial_position += operation
        # this math will count landings on zero's as crossing, this is addressed
        # once it is known if the dial landed on zero (after modulo to its range)
        times_crossed_zero += abs(dial_position // 100)
        dial_position %= 100
        if dial_position == 0:
            times_at_zero += 1
        # adjustments to right that end on zero are not considered crossings,
        # e.g. 90 + 10 = 100 is detected as a crossing, but the landing on zero is
        # already accounted for in the zero counts, conversely 90 + 110 = 200,
        # originally detected as 2 crossings but should count as one crossing and one
        # zero count
        if dial_position == 0 and operation > 0:
            times_crossed_zero -= 1
        # adjustments to left that started on zero are not considered crossings,
        # similar logic to the positive operation case applies
        if dial_position_prev == 0 and operation < 0:
            times_crossed_zero -= 1

    print(f"Part 1: {times_at_zero}")
    print(f"Part 2: {times_at_zero + times_crossed_zero}")
