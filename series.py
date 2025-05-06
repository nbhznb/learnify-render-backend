from Polygons.Polygons import Polygon, plt, rndangle
from Polygons.utils import cropImage, splitQuad
import random, os, time, cv2

class Series:
    '''
    A combination of pattern and number of sides repeating
    '''
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

        # odd side have one hatch, even have one hatch. series
        self.XX = int(random.random()*5)+3
        self.allhatches = Polygon.getHatches()
        random.shuffle(self.allhatches)
        self.SIDE_REPEAT_FREQ = random.choice(range(2,4))
        self.HATCH_REPEAT_FREQ = random.choice(range(2,4))
        # self.TOTAL_FIG = 2 * max(SIDE_REPEAT_FREQ, HATCH_REPEAT_FREQ)
        self.TOTAL_FIG = 6

        # Pick any N indexs
        self.rndindex = int(random.random() * (len(self.allhatches)-self.HATCH_REPEAT_FREQ) )
        self.two_hatches = self.allhatches[ self.rndindex : self.rndindex+self.HATCH_REPEAT_FREQ]

    def generate_all_images(self):
        for i in range(1, self.TOTAL_FIG+4):
            plt.figure()
            A = Polygon(no_of_sides= 3+(self.XX+i)%self.SIDE_REPEAT_FREQ, isRegular=False, hatch= self.two_hatches[(self.XX+i)%self.HATCH_REPEAT_FREQ])
            A.makeRandomCircumcircle()
            A.drawPolygon()
            plt.axis('image')
            plt.axis('off')

            # part of the question
            if i < self.TOTAL_FIG:
                question_tmpPath = os.path.join(self.tmp_dir, f'series_question_{self.questionCount}_part_{i}.png')
                plt.savefig(question_tmpPath)
                plt.close()
                img = cv2.imread(question_tmpPath, 0)
                img = cropImage(img)
                cv2.imwrite(question_tmpPath, img)
                os.system('convert ' + question_tmpPath + ' -bordercolor Black -border 4x4 ' + question_tmpPath)

            # answer
            elif i == self.TOTAL_FIG:
                self.answer_path = os.path.join(self.result_dir, f'series_answer_{self.questionCount}.png')
                plt.savefig(self.answer_path)
                plt.close()
                img = cv2.imread(self.answer_path, 0)
                img = cropImage(img)
                cv2.imwrite(self.answer_path, img)
                os.system('convert ' + self.answer_path + ' -bordercolor Black -border 4x4 ' + self.answer_path)

            # distractors
            else:
                distractor_path = os.path.join(self.result_dir, f'series_question_{self.questionCount}_dist_{i-self.TOTAL_FIG-1}.png')
                plt.savefig(distractor_path)
                plt.close()
                img = cv2.imread(distractor_path, 0)
                img = cropImage(img)
                cv2.imwrite(distractor_path, img)
                os.system('convert ' + distractor_path + ' -bordercolor Black -border 4x4 ' + distractor_path)
                self.distractors_path.append(distractor_path)

        # build question montage
        question_path = os.path.join(self.tmp_dir, f'series_question_{self.questionCount}_part_')
        self.question_path = os.path.join(self.result_dir, f'series_question_{self.questionCount}.png')

        os.system('montage -mode concatenate -tile ' + str(self.TOTAL_FIG-1) + 'x1 ' + question_path + '[1-' + str(self.TOTAL_FIG-1) + '].png ' + self.question_path)

    def get_question(self):
        return self.question_path

    def get_answer(self):
        return self.answer_path

    def get_distractors(self):
        return self.distractors_path

if __name__ == "__main__":
    s = Series(1)
    s.generate_all_images()
