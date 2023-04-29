from os.path import join as join_path
from pathlib import Path
import os
from deepface import DeepFace

# import cv2

# import matplotlib.pyplot as plt


BASE_URL = Path(__file__).resolve().parent


def is_found(my_list: list):
    print('it came to Finder')
    results_list = []
    if my_list[0]:
        if my_list[-1]:
            pictures_folder = join_path(BASE_URL, 'db', 'pictures', 'found_people')
        else:
            pictures_folder = join_path(BASE_URL, 'db', 'pictures', 'lost_people')
        pictures = os.listdir(pictures_folder)
        for j in my_list[0]:
            try:
                for i in pictures:
                    if my_list[-1]:
                        img2_path = join_path(BASE_URL, 'db', 'pictures', 'found_people', i)
                        img2_path_for_user_id = join_path('db', 'pictures', 'found_people', i)
                    else:
                        img2_path = join_path(BASE_URL, 'db', 'pictures', 'lost_people', i)
                        img2_path_for_user_id = join_path('db', 'pictures', 'lost_people', i)
                    print('comparing it!', join_path(BASE_URL,j), img2_path)
                    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
                    result = DeepFace.verify(img1_path=join_path(BASE_URL, j), img2_path=img2_path,
                                             model_name=models[1],
                                             enforce_detection=False)
                    print(result)
                    if result['verified']:
                        results_list.append(img2_path_for_user_id)
                        print("sameness!")
            except Exception as e:
                print(e)
    if results_list:
        return results_list
    else:
        return False
