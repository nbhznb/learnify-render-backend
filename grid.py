from Polygons.Polygons import Polygon, plt, Circumcircle
from Polygons.utils import cropImage
import math
import copy
import os
import random
import cv2
import PIL.Image as IMG
import matplotlib.path as mpath
import matplotlib.patches as mpatches

class Grid:
    def __init__(self, questionCount):
        self.questionCount = questionCount
        self.lenSequence = 3
        self.numPolygons = 3
        self.question_path = ''
        self.answer_path = ''
        self.distractors_path = []
        self.STATIC_ROOT = os.path.join(os.getcwd(), "static")

    def generate_all_images(self):
        dist_root_seq_of_polygons = []
        for l in range(self.lenSequence):
            # Cleans canvas starts a new figure
            plt.figure()

            # Make a random polygon (the outer most Polygon)
            A = Polygon()
            A.makeRandomCircumcircle()

            # This stores the polygons that make up an image.
            # We should store this and use it to create a distractor image
            seqs_of_polygons = []
            for j in range(self.numPolygons):
                # any number of sides
                B = Polygon(no_of_sides=int(random.random() * 3) + 3)
                # same center and radius
                B.clone_circumcircle(A)
                # Center remains same as A but the radius can be anything less than A's radius
                B.circumcircle.radius = 0.5 * A.circumcircle.radius
                # make the sides
                B.makeShape()
                # draw the polygon on the canvas
                B.drawPolygon()
                seqs_of_polygons.append(B)
                A.circumcircle.radius = B.circumcircle.radius

            plt.axis('image')
            plt.axis('off')
            question_base_path = os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_{l}_0.png')
            plt.savefig(question_base_path)
            plt.close()

            img = cv2.imread(question_base_path, 0)
            img = cropImage(img)
            cv2.imwrite(question_base_path, img)

            img = IMG.open(question_base_path)
            img = img.resize((300, 300), IMG.LANCZOS)
            img.save(question_base_path, quality=90)

            for level in [1, 2]:
                plt.figure()
                # transformations for each embedded polygon
                # TODO: shuffle order and rules to generate distractors
                for i in range(len(seqs_of_polygons)):
                    if i == 0:
                        seqs_of_polygons[i].rotate(math.pi * 0.5)  # 90 degrees
                    elif i == 1:
                        seqs_of_polygons[i].flip('vert')
                    elif i == 2:
                        seqs_of_polygons[i].rotate(math.pi * 0.75)  # 270 degrees

                    seqs_of_polygons[i].drawPolygon()

                if l == 2 and level == 1:
                    dist_root_seq_of_polygons = copy.deepcopy(seqs_of_polygons)

                plt.axis('image')
                plt.axis('off')
                question_transform_path = os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_{l}_{level}.png')
                plt.savefig(question_transform_path)
                plt.close()

                img = cv2.imread(question_transform_path, 0)
                img = cropImage(img)
                cv2.imwrite(question_transform_path, img)
                img = IMG.open(question_transform_path)
                img = img.resize((300, 300), IMG.LANCZOS)
                img.save(question_transform_path, quality=90)

            level_montage_path = os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_level_{l}_final.png')

            if l == 2:
                self.answer_path = os.path.join(self.STATIC_ROOT, 'result', f'grid_answer_{self.questionCount}.png')
                os.system("cp " + os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_2_2.png') + ' ' + self.answer_path)
                os.system("montage -mode concatenate -border 2 " + os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_{l}_[0-1].png') + " -tile 3x1 -geometry +1+1 " + level_montage_path)

                # generate distractors
                for dist in range(3):
                    # create copy of level 2 part 1 question - from which answer is generated
                    dist_seq_of_polygons = copy.deepcopy(dist_root_seq_of_polygons)

                    plt.figure()
                    if dist == 0:
                        # order of transformations are shuffled for the distractors
                        for i in range(len(dist_seq_of_polygons)):
                            if i == 0:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.75)  # 270 degrees
                            elif i == 1:
                                dist_seq_of_polygons[i].flip('hori')
                            elif i == 2:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.5)  # 90 degrees

                            dist_seq_of_polygons[i].drawPolygon()
                    if dist == 1:
                        # order of transformations are shuffled for the distractors
                        for i in range(len(dist_seq_of_polygons)):
                            if i == 0:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.5)  # 90 degrees
                            elif i == 1:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.75)  # 270 degrees
                            elif i == 2:
                                dist_seq_of_polygons[i].flip('hori')

                            dist_seq_of_polygons[i].drawPolygon()
                    if dist == 2:
                        # order of transformations are shuffled for the distractors
                        for i in range(len(dist_seq_of_polygons)):
                            if i == 0:
                                dist_seq_of_polygons[i].flip('vert')
                            elif i == 1:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.75)  # 270 degrees
                            elif i == 2:
                                dist_seq_of_polygons[i].rotate(math.pi * 0.5)  # 90 degrees

                            dist_seq_of_polygons[i].drawPolygon()

                    plt.axis('image')
                    plt.axis('off')
                    distractor_path = os.path.join(self.STATIC_ROOT, 'result', f'grid_question_{self.questionCount}_dist_{dist}.png')
                    plt.savefig(distractor_path)
                    plt.close()

                    img = cv2.imread(distractor_path, 0)
                    img = cropImage(img)
                    cv2.imwrite(distractor_path, img)
                    img = IMG.open(distractor_path)
                    img = img.resize((300, 300), IMG.LANCZOS)
                    img.save(distractor_path, quality=90)

                    self.distractors_path.append(distractor_path)

            else:
                os.system("montage -mode concatenate -border 2 " + os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_{l}_[0-2].png') + " -tile 3x1 -geometry +1+1 " + level_montage_path)

        self.question_path = os.path.join(self.STATIC_ROOT, 'result', f'grid_question_{self.questionCount}.png')
        os.system("montage -mode concatenate -border 2 " + os.path.join(self.STATIC_ROOT, 'tmp', f'grid_question_{self.questionCount}_level_[0-2]_final.png') + " -tile 1x3 -geometry +1+1 " + self.question_path)

    def get_question(self):
        return self.question_path

    def get_answer(self):
        return self.answer_path

    def get_distractors(self):
        return self.distractors_path

if __name__ == "__main__":
    g = Grid(1)
    g.generate_all_images()
