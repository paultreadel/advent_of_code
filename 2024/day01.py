from collections import Counter

if __name__ == "__main__":
    # parse input
    with open("data/day01.txt") as input_file:
        input_data = input_file.read()
    pairs = [tuple(map(int, line.split())) for line in input_data.splitlines()]
    lh_data, rh_data = zip(*pairs)

    # part 1
    ordered_lh, ordered_rh = sorted(lh_data), sorted(rh_data)
    differences = [abs(lh - rh) for lh, rh in zip(ordered_lh, ordered_rh)]
    total_difference = sum(differences)
    print(f"Part 1: {total_difference}")

    # part 2
    rh_occurrences = Counter(rh_data)
    similarity_scores = [lh * rh_occurrences.get(lh, 0) for lh in lh_data]
    total_similarity = sum(similarity_scores)
    print(f"Part 2: {total_similarity}")
