"""
Use command to run file:
python testbench.py --filename testbench.csv
"""
import argparse
import csv

import indexed_data
from hip_agent import HIPAgent


def score_testbench(filename):
    """
    scores the csv file having questions.

    Args:
        filename: The filename to be scored.
    """
    # Parse the CSV file
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        headers = next(reader)
        data = list(reader)

    # Get the correct answers
    correct_answers = []

    # Instantiate a HIP agent
    agent = HIPAgent()

    # Get the user's responses
    user_responses = []
    db = indexed_data.get_indexed_data()
    for row in data:
        answer_choices = [row[headers.index("answer_0")],
                          row[headers.index("answer_1")],
                          row[headers.index("answer_2")],
                          row[headers.index("answer_3")]]
        correct_answers.append(answer_choices.index(row[headers.index("correct")]))
        response = agent.get_response(row[headers.index("question")], answer_choices, db)
        user_responses.append(response)

    # Calculate the score
    score = 0
    answers = []
    for i in range(len(data)):
        if user_responses[i] == correct_answers[i]:
            score += 1
            answers += [[1, user_responses[i], correct_answers[i]]]
        else:
            answers += [[0, user_responses[i], correct_answers[i]]]

    # Display the score
    print(f"Score:{score}/{len(data)}\n\n")
    print(answers)


def create_parser():
    parser = argparse.ArgumentParser(description='script to run test bench')
    parser.add_argument('--filename', help='run the test bench provided', default='testbench.csv')
    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    score_testbench(args.filename)
