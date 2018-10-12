from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
from threading import Lock

ANSWERS_PATH = 'simple-questionnaire/data/answers.csv'
QUESTIONS_PATH = 'simple-questionnaire/data/questions.csv'

app = Flask(__name__)
lock = Lock()


def load_questions(path):
    """
    Read questions from file
    :param path: path to questions file
    :return: questions as list of triples - left part, right part and question number
    """
    questions = []

    with open(path, 'r') as f:
        for line in f:
            q_part1, q_part2 = line.split(';')
            question = {
                'p1': q_part1,
                'p2': q_part2,
                'num': len(questions) + 1}

            questions.append(question)

    return questions


@app.route('/')
def main():
    """
    Main page
    """
    return render_template('questions.html', questions=questions)


@app.route('/send_form', methods=['POST'])
def send_form():
    """
    Collect answers and show "Thank you" form
    """
    answers = list()

    questions = sorted([s for s in request.form.keys() if s.startswith('q')])

    answers.append(request.form['code'])
    answers.append(datetime.now().strftime('%Y/%m/%d %H:%M'))

    for q in questions:
        answers.append(request.form[q])

    write_answers(ANSWERS_PATH, answers)

    return render_template('thank_you.html')


def write_answers(path, answers):
    """
    Writes answers to file in csv format
    :param answers: list of answers
    """
    csv = ';'.join(answers)

    with lock:
        with open(path, 'a') as wf:
            wf.write(csv + '\n')


questions = load_questions(QUESTIONS_PATH)

if __name__ == '__main__':
    app.run()
