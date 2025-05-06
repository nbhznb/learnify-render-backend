from Polygons.Polygons import Polygon, plt
from Polygons.utils import cropImage, splitQuad
import cv2
import random
import math
import os

class Cut:
    def __init__(self, polyNum, questionCount):
        self.polyNum = polyNum
        self.questionCount = questionCount
        self.optionNum = 3  # number of distractors
        self.question_path = ''
        self.answer_path = ''
        self.distractors = []
        self.distractors_path = []
        self.quadrantNum = random.choice([0, 1, 2, 3])
        self.STATIC_ROOT = os.path.join(os.getcwd(), "static")

    def distractor_sequence(self, A):
        seqs_of_polygons = [A]
        polys = []
        for j in range(self.polyNum):
            B = Polygon(no_of_sides=random.choice([0, int(random.random() * 7) + 3]), isRegular='any', hatch=None)
            B.clone_circumcircle(A)
            B.circumcircle.x = B.circumcircle.x
            B.circumcircle.y = B.circumcircle.y
            B.circumcircle.radius = random.choice([10, 20, 40, 50]) + B.circumcircle.radius
            B.makeShape()
            B.drawPolygon()
            seqs_of_polygons.append(B)
        self.distractors = seqs_of_polygons

    def generate_question_answer_pair(self):
        plt.figure()
        A = Polygon()
        A.makeRandomCircumcircle()
        A.drawPolygon()
        self.distractor_sequence(A)
        plt.axis('image')
        plt.axis('off')
        question_tmpPath = os.path.join(self.STATIC_ROOT, 'tmp', f'cut_question_{self.questionCount}.png')
        plt.savefig(question_tmpPath)
        img = cv2.imread(question_tmpPath, 0)
        img = cropImage(img)
        cv2.imwrite(question_tmpPath, img)
        self.question_path = os.path.join(self.STATIC_ROOT, 'result', f'cut_question_{self.questionCount}.png')
        self.answer_path = os.path.join(self.STATIC_ROOT, 'result', f'cut_answer_{self.questionCount}.png')
        img = cv2.imread(question_tmpPath, 0)
        quad, rest_img = splitQuad(img, self.quadrantNum)
        cv2.imwrite(self.answer_path, quad)
        cv2.imwrite(self.question_path, rest_img)
        plt.close()

    def genDistractors(self):
        for j in range(self.optionNum):
            plt.figure()
            for i in self.distractors:
                choice = random.choice(['flip', 'rotate', 'swap'])
                if choice == 'flip':
                    i.flip(how=random.choice(['vert', 'hori']))
                elif choice == 'rotate':
                    i.rotate(theta=random.choice([math.pi / 2, math.pi / 4, math.pi]))
                elif choice == 'swap':
                    i.swap_polygons(random.choice(self.distractors))
                i.drawPolygon()
            plt.axis('image')
            plt.axis('off')
            distractor_tmpPath = os.path.join(self.STATIC_ROOT, 'tmp', f'cut_question_{self.questionCount}_dist_{j}.png')
            plt.savefig(distractor_tmpPath)
            img = cv2.imread(distractor_tmpPath, 0)
            img = cropImage(img)
            cv2.imwrite(distractor_tmpPath, img)
            img = cv2.imread(distractor_tmpPath, 0)
            quad, rest_img = splitQuad(img, self.quadrantNum)
            distractor_finalPath = os.path.join(self.STATIC_ROOT, 'result', f'cut_question_{self.questionCount}_dist_{j}.png')
            cv2.imwrite(distractor_finalPath, quad)
            self.distractors_path.append(distractor_finalPath)
            plt.close()

    def getQuestion(self):
        return self.question_path

    def getAnswer(self):
        return self.answer_path

    def getDistractors(self):
        return self.distractors_path
