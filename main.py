import argparse
import os
from generateQuestionPaper import generate_question

def main():
    cleanup_static_folders()
    parser = argparse.ArgumentParser(description="Generate non-verbal reasoning quiz images.")
    parser.add_argument("--question_num", type=int, required=True, help="Question number to generate")
    args = parser.parse_args()

    generate_question(args.question_num)


def cleanup_static_folders():
    static_dirs = ['static/result', 'static/tmp']

    for directory in static_dirs:
        folder_path = os.path.join(os.getcwd(), directory)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    main()
