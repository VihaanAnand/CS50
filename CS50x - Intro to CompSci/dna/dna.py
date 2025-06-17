import csv
import sys


def main():

    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    with open(sys.argv[1]) as data:
        reader = csv.DictReader(data)
        database = []
        for line in reader:
            dline = dict()
            for item in list(line):
                if item == "name":
                    dline["name"] = line["name"]
                else:
                    dline[item] = int(line[item])
            database.append(dline)

    with open(sys.argv[2]) as dnaFile:
        dna = dnaFile.read()

    STRs = list(database[0])[1:]
    dnaAnalysis = dict()
    for STR in STRs:
        longest = longest_match(dna, STR)
        dnaAnalysis[STR] = longest

    for person in database:
        personMatch = True
        for STR in STRs:
            if not dnaAnalysis[STR] == person[STR]:
                personMatch = False
                break
        if personMatch == True:
            print(person["name"])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()