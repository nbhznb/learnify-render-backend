from cutImage import Cut
from dice import Dice
from figureMatrixAndSequence import FigureMatrixAndSequence
from fold import Fold
from grid import Grid
from series import Series
import os

def generate_question(question_num):
    '''
    by default:
    even questions are easy, odd questions are difficult
    2 questions - 1 easy, 1 difficult per question type
    '''
    static_dir = os.path.join(os.getcwd(), 'static')
    result_dir = os.path.join(static_dir, 'result')

    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)

    # cut
    if question_num in [1, 2]:
        if question_num % 2 == 0:
            polygon_num = 4
        else:
            polygon_num = 2
        c = Cut(polygon_num, question_num)
        c.generate_question_answer_pair()
        question_filepath = os.path.relpath(c.getQuestion(), static_dir)
        answer_filepath = os.path.relpath(c.getAnswer(), static_dir)
        c.genDistractors()
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in c.getDistractors()]
        print(f"Cut question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "cutImage",
                "text": "Identify the missing part of the shape.",
                "explanation": "The correct answer is the part of the shape that fits perfectly into the missing section. The wrong answers are either flipped, rotated, or swapped versions of the correct shape.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data

    # dice
    elif question_num in [3, 4]:
        d = Dice(question_num)
        d.generate_question()
        question_filepath = os.path.relpath(d.getQuestion(), static_dir)
        d.generate_answer()
        answer_filepath = os.path.relpath(d.getAnswer(), static_dir)
        d.generate_distractors()
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in d.getDistractors()]
        print(f"Dice question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "dice",
                "text": "Identify the correct arrangement of symbols on the dice.",
                "explanation": "The correct answer shows the correct arrangement of symbols on the dice. The wrong answers show incorrect arrangements.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data

    # fold
    elif question_num in [5, 6]:
        f = Fold(question_num)
        f.generate_all_images()
        question_filepath = os.path.relpath(f.get_question(), static_dir)
        answer_filepath = os.path.relpath(f.get_answer(), static_dir)
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in f.get_distractors()]
        print(f"Fold question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "fold",
                "text": "Identify the correct folded shape.",
                "explanation": "The correct answer shows the correct folded shape. The wrong answers show incorrectly folded shapes.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data

    # figure matrix and sequence
    elif question_num in [7, 8]:
        f = FigureMatrixAndSequence(question_num)
        f.generate_all_images()
        question_filepath = os.path.relpath(f.get_question(), static_dir)
        answer_filepath = os.path.relpath(f.get_answer(), static_dir)
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in f.get_distractors()]
        print(f"Figure matrix & sequence question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "figureMatrixAndSequence",
                "text": "Identify the correct pattern in the matrix.",
                "explanation": "The correct answer shows the correct pattern in the matrix. The wrong answers show incorrect patterns.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data

    # grid
    elif question_num in [9, 10]:
        g = Grid(question_num)
        g.generate_all_images()
        question_filepath = os.path.relpath(g.get_question(), static_dir)
        answer_filepath = os.path.relpath(g.get_answer(), static_dir)
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in g.get_distractors()]
        print(f"Grid question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "grid",
                "text": "Identify the correct sequence of transformations.",
                "explanation": "The correct answer shows the correct sequence of transformations. The wrong answers show incorrect sequences.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data

    # series
    elif question_num in [11, 12]:
        s = Series(question_num)
        s.generate_all_images()
        question_filepath = os.path.relpath(s.get_question(), static_dir)
        answer_filepath = os.path.relpath(s.get_answer(), static_dir)
        distractor_filepaths = [os.path.relpath(path, static_dir) for path in s.get_distractors()]
        print(f"Series question generated: {question_filepath}, {answer_filepath}, {distractor_filepaths}")

        question_data = {
            str(question_num): {
                "category": "series",
                "text": "Identify the correct pattern in the series.",
                "explanation": "The correct answer shows the correct pattern in the series. The wrong answers show incorrect patterns.",
                "question": question_filepath,
                "answer": answer_filepath,
                "distractors": distractor_filepaths
            }
        }
        return question_data
