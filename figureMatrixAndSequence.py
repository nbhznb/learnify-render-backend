from Polygons.Polygons import Polygon, plt, Circumcircle
from Polygons.utils import cropImage
import math
import copy
import os
import random
import cv2

gridSize = 25
radius = 10
startX = 0
startY = 0

def shift_polys(polys, pos_by=1, hatch_by=1):
    tmep_polys = copy.deepcopy(polys)

def draw_grid():
    # This is to get a border so that while cropping, we do not crop the whitespaces we want to show.
    plt.gca().add_patch(
        plt.Rectangle(
            (-gridSize / 2, -gridSize * 3 + gridSize / 2),   # (x,y)
            gridSize * 3,          # width
            gridSize * 3,          # height
            fill=None,
            edgecolor='black'  # Added edge color for better visibility
        )
    )

    # draw boxes grid
    for i in range(3):
        for j in range(3):
            plt.gca().add_patch(
                plt.Rectangle(
                    (-gridSize / 2 + gridSize * i, -gridSize * (j + 1) + gridSize / 2),   # (x,y)
                    gridSize,          # width
                    gridSize,          # height
                    fill=None,
                    edgecolor='blue'
                )
            )

def draw_polygon_grid(poly, index):
    # The incoming index is 1 to 9
    # Assigns the figure an appropriate circumcircle
    index -= 1  # Convert to 0-based index
    row = index // 3  # Row index (0, 1, 2)
    col = index % 3   # Column index (0, 1, 2)

    # Calculate the center of the grid cell
    center_x = startX + col * gridSize
    center_y = startY - row * gridSize

    # Assign the circumcircle with the correct center
    poly.circumcircle = Circumcircle(radius, center_x, center_y)
    poly.makeShape()
    poly.drawPolygon()

class FigureMatrixAndSequence:
    def __init__(self, questionCount):
        self.questionCount = questionCount
        self.question_path = ''
        self.answer_path = ''
        self.distractors_path = []
        self.STATIC_ROOT = os.path.join(os.getcwd(), "static")
        self.logic_choice = random.random()
        
        # Ensure required directories exist
        self.tmp_dir = os.path.join(self.STATIC_ROOT, 'tmp')
        self.result_dir = os.path.join(self.STATIC_ROOT, 'result')
        os.makedirs(self.tmp_dir, exist_ok=True)
        os.makedirs(self.result_dir, exist_ok=True)

    def generate_all_images(self):
        if self.logic_choice < 0.5:
            plt.figure()
            draw_grid()
            polys = []
            XX = 0

            rank = list(range(1, 10))
            random.shuffle(rank)
            for i in rank:
                temp = Polygon(no_of_sides=int(random.random() * 6),
                               isRegular=False, hatch='random')
                draw_polygon_grid(temp, i)
                polys.append(temp)
                XX += 1

            # question
            plt.axis('image')
            plt.axis('off')
            question_tmpPath = os.path.join(self.tmp_dir, f'figureMatrix_question_{self.questionCount}_part_0.png')

            plt.savefig(question_tmpPath, dpi=150)
            img = cv2.imread(question_tmpPath, 0)
            img = cropImage(img)
            cv2.imwrite(question_tmpPath, img)
            plt.close()

            # generates remaining 4 parts for question
            for i in range(1, 9):
                plt.figure()
                draw_grid()

                # shift polygons by one position
                temp_circumcircle = polys[0].circumcircle
                for j in range(len(polys) - 1):
                    polys[j].circumcircle = polys[j + 1].circumcircle

                polys[len(polys) - 1].circumcircle = temp_circumcircle

                for k in range(len(polys)):
                    polys[k].gen_points()
                    polys[k].drawPolygon()

                plt.axis('image')
                plt.axis('off')
                if i in [1, 2, 3, 4]:
                    question_tmpPath = os.path.join(self.tmp_dir, f'figureMatrix_question_{self.questionCount}_part_{i}.png')
                elif i == 5:
                    question_tmpPath = os.path.join(self.result_dir, f'figureMatrix_answer_{self.questionCount}.png')
                    self.answer_path = question_tmpPath
                else:
                    question_tmpPath = os.path.join(self.result_dir, f'figureMatrix_question_{self.questionCount}_dist_{i - 6}.png')
                    self.distractors_path.append(question_tmpPath)

                plt.savefig(question_tmpPath, dpi=150)

                img = cv2.imread(question_tmpPath, 0)
                img = cropImage(img)
                cv2.imwrite(question_tmpPath, img)
                plt.close()

        else:
            plt.figure()
            draw_grid()
            polys = []
            XX = 0

            rank = list(range(1, 10))
            random.shuffle(rank)
            hatches = ['-', '+', 'x', '\\', '*', 'o', 'O', '.', '/', '|']
            random.shuffle(hatches)

            for i in rank:
                temp = Polygon(no_of_sides=int(random.random() * 6) + 3,
                               isRegular=False, hatch=hatches[i % 10])
                draw_polygon_grid(temp, i)
                polys.append(temp)
                XX += 1

            # question
            plt.axis('image')
            plt.axis('off')
            question_tmpPath = os.path.join(self.tmp_dir, f'figureMatrix_question_{self.questionCount}_part_0.png')

            plt.savefig(question_tmpPath, dpi=150)
            img = cv2.imread(question_tmpPath, 0)
            img = cropImage(img)
            cv2.imwrite(question_tmpPath, img)
            plt.close()

            # generates remaining 4 parts for question
            for i in range(1, 9):
                plt.figure()
                draw_grid()

                # shift polygons by one position
                temp_circumcircle = polys[0].circumcircle
                for j in range(len(polys) - 1):
                    polys[j].circumcircle = polys[j + 1].circumcircle

                polys[len(polys) - 1].circumcircle = temp_circumcircle

                for k in range(len(polys)):
                    polys[k].gen_points()
                    polys[k].drawPolygon()

                plt.axis('image')
                plt.axis('off')
                if i in [1, 2, 3, 4]:
                    question_tmpPath = os.path.join(self.tmp_dir, f'figureMatrix_question_{self.questionCount}_part_{i}.png')
                elif i == 5:
                    question_tmpPath = os.path.join(self.result_dir, f'figureMatrix_answer_{self.questionCount}.png')
                    self.answer_path = question_tmpPath
                else:
                    question_tmpPath = os.path.join(self.result_dir, f'figureMatrix_question_{self.questionCount}_dist_{i - 6}.png')
                    self.distractors_path.append(question_tmpPath)

                plt.savefig(question_tmpPath, dpi=150)

                img = cv2.imread(question_tmpPath, 0)
                img = cropImage(img)
                cv2.imwrite(question_tmpPath, img)
                plt.close()

        self.question_path = os.path.join(self.result_dir, f'figureMatrix_question_{self.questionCount}.png')
        os.system('montage -mode concatenate -tile 5x1 -border 5 ' + os.path.join(self.tmp_dir, f'figureMatrix_question_{self.questionCount}_part_[0-4].png') + ' ' + self.question_path)

    def get_question(self):
        return self.question_path

    def get_answer(self):
        return self.answer_path

    def get_distractors(self):
        return self.distractors_path

if __name__ == "__main__":
    f = FigureMatrixAndSequence(1)
    f.generate_all_images()
