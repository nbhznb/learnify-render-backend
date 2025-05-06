from Polygons.Polygons import Polygon, plt, Circumcircle
from Polygons.utils import cropImage, splitQuad
import math
import copy
import os
import random
import cv2
import PIL.Image as IMG
import matplotlib.path as mpath
import matplotlib.patches as mpatches

class Fold:
    def __init__(self, questionCount):
        self.questionCount = questionCount
        self.question_path = ''
        self.answer_path = ''
        self.distractors_path = []
        self.STATIC_ROOT = os.path.join(os.getcwd(), "static")

    def generate_all_images(self):
        sides = [0, 0, 2, 4]
        XX = [0, 10, 15, 20]
        YY = [10, 15, 0, 20]
        polys = []
        plt.figure()
        temp = None

        for i in range(len(sides)):
            size = (i + 1) ** 2 * 100
            temp = Polygon(no_of_sides=sides[i], isRegular=False)
            temp.circumcircle = Circumcircle(size, XX[i], YY[i])
            temp.makeShape()
            temp.drawPolygon()
            polys.append(temp)

        plt.axis('image')
        plt.axis('off')
        question_baseImgPath = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_base.png')
        plt.savefig(question_baseImgPath, transparent=True)
        plt.close()

        # save a flipped version
        question_baseImgFlippedPath = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_base_flipped.png')
        os.system('convert ' + question_baseImgPath + ' -flop ' + question_baseImgFlippedPath)

        one = IMG.open(question_baseImgPath).convert('RGBA')
        two = IMG.open(question_baseImgFlippedPath).convert('RGBA')

        base_img_merge_filepath = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_base_merge.png')
        IMG.alpha_composite(one, two).save(base_img_merge_filepath)

        img = cv2.imread(base_img_merge_filepath, 0)
        height, width = img.shape
        # gives transparent image

        self.question_path = os.path.join(self.STATIC_ROOT, 'result', f'fold_question_{self.questionCount}.png')
        self.answer_path = os.path.join(self.STATIC_ROOT, 'result', f'fold_answer_{self.questionCount}.png')
        os.system('convert ' + question_baseImgPath + ' -strokewidth 1 -fill none -stroke black -draw \"stroke-dasharray 5 3 line ' + str(width / 2) + ',0 ' + str(width / 2) + ',' + str(height) + '\" ' + self.question_path)
        os.system('convert ' + base_img_merge_filepath + ' -strokewidth 1 -fill none -stroke black -draw \"stroke-dasharray 5 3 line ' + str(width / 2) + ',0 ' + str(width / 2) + ',' + str(height) + '\" ' + base_img_merge_filepath)
        os.system('convert ' + base_img_merge_filepath + '  -fill white -draw "rectangle 0,0 ' + str(width / 2) + ',' + str(height) + '" ' + self.answer_path)

        # adds white bg
        os.system('convert -flatten ' + self.question_path + ' ' + self.question_path)  # question
        os.system('convert -flatten ' + base_img_merge_filepath + ' ' + base_img_merge_filepath)  # intermediate output
        os.system('convert -flatten ' + self.answer_path + ' ' + self.answer_path)  # answer

        # distractors
        for j in range(3):
            dist_base_img = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_dist_{j}_base.png')
            dist_base_flipped_img = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_dist_{j}_base_flipped.png')
            dist_base_merge_img = os.path.join(self.STATIC_ROOT, 'tmp', f'fold_question_{self.questionCount}_dist_{j}_base_merge.png')
            plt.figure()
            # additional transformation
            for temp in polys:
                if random.random() <= 0.5:
                    temp.flip(how=random.choice(['vert', 'hori']))
                else:
                    temp.rotate(random.choice([-1, +1]) * random.choice([math.pi / 4, math.pi / 2]))
                temp.drawPolygon()

            plt.axis('image')
            plt.axis('off')

            # same base image
            plt.savefig(dist_base_img, transparent=True)
            plt.close()

            # save a flipped version
            os.system('convert ' + dist_base_img + ' -flop ' + dist_base_flipped_img)

            one = IMG.open(dist_base_img).convert('RGBA')
            two = IMG.open(dist_base_flipped_img).convert('RGBA')

            IMG.alpha_composite(one, two).save(dist_base_merge_img)

            img = cv2.imread(dist_base_merge_img, 0)
            height, width = img.shape
            distractor_final_path = os.path.join(self.STATIC_ROOT, 'result', f'fold_question_{self.questionCount}_dist_{j}.png')
            os.system('convert ' + dist_base_img + ' -strokewidth 1 -fill none -stroke black -draw \"stroke-dasharray 5 3 line ' + str(width / 2) + ',0 ' + str(width / 2) + ',' + str(height) + '\" ' + dist_base_img)
            os.system('convert ' + dist_base_merge_img + ' -strokewidth 1 -fill none -stroke black -draw \"stroke-dasharray 5 3 line ' + str(width / 2) + ',0 ' + str(width / 2) + ',' + str(height) + '\" ' + dist_base_merge_img)
            os.system('convert ' + dist_base_merge_img + ' -fill white -draw "rectangle 0,0 ' + str(width / 2) + ',' + str(height) + '" ' + distractor_final_path)

            os.system('convert -flatten ' + dist_base_img + ' ' + dist_base_img)  # base distractor
            os.system('convert -flatten ' + dist_base_merge_img + ' ' + dist_base_merge_img)  # intermediate distractor output
            os.system('convert -flatten ' + distractor_final_path + ' ' + distractor_final_path)  # final transformed distractor - folded
            self.distractors_path.append(distractor_final_path)

    def get_question(self):
        return self.question_path

    def get_answer(self):
        return self.answer_path

    def get_distractors(self):
        return self.distractors_path

if __name__ == "__main__":
    f = Fold(1)
    f.generate_all_images()
