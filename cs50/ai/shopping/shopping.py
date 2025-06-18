import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            newev = []
            newev.append(int(row["Administrative"]))
            newev.append(float(row["Administrative_Duration"]))
            newev.append(int(row["Informational"]))
            newev.append(float(row["Informational_Duration"]))
            newev.append(int(row["ProductRelated"]))
            newev.append(float(row["ProductRelated_Duration"]))
            newev.append(float(row["BounceRates"]))
            newev.append(float(row["ExitRates"]))
            newev.append(float(row["PageValues"]))
            newev.append(float(row["SpecialDay"]))
            match row["Month"]:
                case "Jan":
                    newev.append(0)
                case "Feb":
                    newev.append(1)
                case "Mar":
                    newev.append(2)
                case "Apr":
                    newev.append(3)
                case "May":
                    newev.append(4)
                case "June":
                    newev.append(5)
                case "Jul":
                    newev.append(6)
                case "Aug":
                    newev.append(7)
                case "Sep":
                    newev.append(8)
                case "Oct":
                    newev.append(9)
                case "Nov":
                    newev.append(10)
                case "Dec":
                    newev.append(11)
            newev.append(int(row["OperatingSystems"]))
            newev.append(int(row["Browser"]))
            newev.append(int(row["Region"]))
            newev.append(int(row["TrafficType"]))
            match row["VisitorType"]:
                case "New_Visitor":
                    newev.append(0)
                case "Returning_Visitor":
                    newev.append(1)
            match row["Weekend"]:
                case "FALSE":
                    newev.append(0)
                case "TRUE":
                    newev.append(1)
            evidence.append(newev)
            match row["Revenue"]:
                case "FALSE":
                    labels.append(0)
                case "TRUE":
                    labels.append(1)
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives_correct = 0
    positives = 0
    negatives_correct = 0
    negatives = 0
    for index in range(len(labels)):
        label = labels[index]
        prediction = predictions[index]
        if label == 1:
            positives += 1
            if prediction == 1:
                positives_correct += 1
        else:
            negatives += 1
            if prediction == 0:
                negatives_correct += 1
    sensitivity = positives_correct / positives
    specificity = negatives_correct / negatives
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()

