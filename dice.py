from Polygons.Polygons import Polygon, plt
from Polygons.utils import cropImage
import math
import random
import cv2
import os

class Dice:
    def __init__(self, questionCount):
        self.questionCount = questionCount
        self.question_path = ''
        self.answer_path = ''
        self.distractors_path = []
        self.STATIC_ROOT = os.path.join(os.getcwd(), "static")
        
        # Ensure required directories exist
        self.tmp_dir = os.path.join(self.STATIC_ROOT, 'tmp')
        self.result_dir = os.path.join(self.STATIC_ROOT, 'result')
        os.makedirs(self.tmp_dir, exist_ok=True)
        os.makedirs(self.result_dir, exist_ok=True)

        self.layout_type = random.choice([1, 2, 3, 4, 5])
        self.symbols = ['#', '*', '-', '?', '^', '**', u'\u2605', u'\u2020', u'\u002B']
        self.triplets = [(2, 5, 1), (6, 2, 1), (2, 3, 5), (2, 3, 6), (1, 4, 6), (4, 1, 5), (4, 6, 3), (5, 3, 4)]
        self.wrong_triplets = [(2, 1, 4), (2, 4, 5), (4, 6, 2), (2, 3, 4)]
        random.shuffle(self.symbols)
        random.shuffle(self.triplets)
        random.shuffle(self.wrong_triplets)

    def generate_question(self):
        side = 10
        zoom = 3
        plt.figure()

        # First four are always drawn the same way
        for i in range(4):
            polygon = plt.Rectangle((0, -i * side), side, side, fill=False)
            plt.gca().text(side / 2, -(i * side - side / 2), self.symbols[i],
                           fontsize=side * zoom,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        if self.layout_type == 1:
            # Draw 5
            polygon = plt.Rectangle((-side, -side), side, side, fill=False)
            plt.gca().text(-side / 2, -side / 2, self.symbols[4],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

            # Draw 6
            polygon = plt.Rectangle((side, -side), side, side, fill=False)
            plt.gca().text(side + side / 2, -side / 2, self.symbols[5],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        elif self.layout_type == 2:
            # Draw 5
            polygon = plt.Rectangle((-side, 0), side, side, fill=False)
            plt.gca().text(-side / 2, +side / 2, self.symbols[4],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

            # Draw 6
            polygon = plt.Rectangle((side, -side), side, side, fill=False)
            plt.gca().text(side + side / 2, -side / 2, self.symbols[5],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        elif self.layout_type == 3:
            # Draw 5
            polygon = plt.Rectangle((-side, -side), side, side, fill=False)
            plt.gca().text(-side / 2, -side / 2, self.symbols[4],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

            # Draw 6
            polygon = plt.Rectangle((side, -2 * side), side, side, fill=False)
            plt.gca().text(side + side / 2, -side / 2 - side, self.symbols[5],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        elif self.layout_type == 4:
            # Draw 5
            polygon = plt.Rectangle((-side, 0), side, side, fill=False)
            plt.gca().text(-side / 2, -side / 2 + side, self.symbols[4],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

            # Draw 6
            polygon = plt.Rectangle((side, -2 * side), side, side, fill=False)
            plt.gca().text(side + side / 2, -side / 2 - side, self.symbols[5],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        elif self.layout_type == 5:
            # Draw 5
            polygon = plt.Rectangle((-side, -side), side, side, fill=False)
            plt.gca().text(-side / 2, -side / 2, self.symbols[4],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

            # Draw 6
            polygon = plt.Rectangle((side, -3 * side), side, side, fill=False)
            plt.gca().text(side + side / 2, -side / 2 - 2 * side, self.symbols[5],
                           fontsize=zoom * side,
                           multialignment='center',
                           verticalalignment='center', horizontalalignment='center')
            plt.gca().add_patch(polygon)

        plt.axis('image')
        plt.axis('off')
        question_tmpPath = os.path.join(self.tmp_dir, f'dice_question_{self.questionCount}.png')
        plt.savefig(question_tmpPath)

        # crop the question image
        self.question_path = os.path.join(self.result_dir, f'dice_question_{self.questionCount}.png')
        img = cv2.imread(question_tmpPath, 0)
        img = cropImage(img)
        cv2.imwrite(self.question_path, img)
        plt.close()

    def draw_three_sides(self, symbols, name):
        plt.figure()
        side = 10
        zoom = 3
        angle = math.pi / 8
        polygon = plt.Polygon([(0, 0), (0, -side), (side * math.cos(angle), side * math.sin(angle) - side), (side * math.cos(angle), side * math.sin(angle))], fill=False)
        plt.gca().add_patch(polygon)
        plt.gca().text(side * math.cos(angle) / 2, (side * math.sin(angle) - side) / 2, symbols[0],
                       fontsize=zoom * side,
                       multialignment='center',
                       verticalalignment='center', horizontalalignment='center')

        polygon = plt.Polygon([(0, 0), (0, -side), (-side * math.cos(angle), side * math.sin(angle) - side), (-side * math.cos(angle), side * math.sin(angle))], fill=False)
        plt.gca().add_patch(polygon)
        plt.gca().text(-side * math.cos(angle) / 2, (side * math.sin(angle) - side) / 2, symbols[1],
                       fontsize=zoom * side,
                       multialignment='center',
                       verticalalignment='center', horizontalalignment='center')

        polygon = plt.Polygon([(0, 0), (side * math.cos(angle), side * math.sin(angle)), (0, 2 * side * math.sin(angle)), (-side * math.cos(angle), side * math.sin(angle))], fill=False)
        plt.gca().add_patch(polygon)
        plt.gca().text(0, side * math.sin(angle), symbols[2],
                       fontsize=zoom * side,
                       multialignment='center',
                       verticalalignment='center', horizontalalignment='center')

        plt.axis('image')
        plt.axis('off')
        plt.savefig(name)
        plt.close()

    def generate_answer(self):
        correct_choice = random.choice([0, 1, 2, 3, 4, 5, 6, 7])
        temp_triplet = self.triplets[correct_choice]
        answer_tmpPath = os.path.join(self.tmp_dir, f'dice_answer_{self.questionCount}.png')
        self.draw_three_sides([self.symbols[j - 1] for j in temp_triplet], answer_tmpPath)

        # crop the answer image
        img = cv2.imread(answer_tmpPath, 0)
        img = cropImage(img)
        self.answer_path = os.path.join(self.result_dir, f'dice_answer_{self.questionCount}.png')
        cv2.imwrite(self.answer_path, img)

    def generate_distractors(self):
        for i in range(3):
            temp_triplet = self.wrong_triplets[i]
            distractor_tmpPath = os.path.join(self.tmp_dir, f'dice_question_{self.questionCount}_dist_{i}.png')
            self.draw_three_sides([self.symbols[j - 1] for j in temp_triplet], distractor_tmpPath)

            # crop the distractor image
            img = cv2.imread(distractor_tmpPath, 0)
            img = cropImage(img)
            distractor_finalPath = os.path.join(self.result_dir, f'dice_question_{self.questionCount}_dist_{i}.png')
            cv2.imwrite(distractor_finalPath, img)
            self.distractors_path.append(distractor_finalPath)

    def getQuestion(self):
        return self.question_path

    def getAnswer(self):
        return self.answer_path

    def getDistractors(self):
        return self.distractors_path

if __name__ == "__main__":
    d = Dice(1)
    d.generate_question()
    d.generate_answer()
    d.generate_distractors()
