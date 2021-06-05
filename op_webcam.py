from datetime import datetime
import cv2 as cv
import os
import sys
import argparse
import json
from skeleton import Skeleton
import argparse

# use if necessary
# sys.path.append('/usr/local/python')

ROOT_PATH = './'
recordings_dir = os.path.join(ROOT_PATH, 'recordings')

class SkeletonSequence():
    def __init__(self):
        # patient data, including joint angle sequence
        self.sequence_data = []

        # joint angle sequences
        self.skeletons = []

    def add(self, body_keypoints):
        self.skeletons.append(Skeleton(body_keypoints))

    def load_from_json(self, folder_name=None):
        sf = open(folder_name)
        self.sequence_data = json.load(sf)

        for joint_angles in self.sequence_data['joint_angles']:
            self.skeletons.append(Skeleton(joint_angles, load_from_json=True))

    def save_as_json(self, folder_name=None):
        action_dir = os.path.join(recordings_dir, folder_name)
        file_name = "recording_{:%Y%m%dT%H%M%S}.json".format(datetime.now())
        joint_angles = []
        for s in self.skeletons:
            joint_angles.append(s.joint_angles)

        if not self.sequence_data:
            self.sequence_data = {'patient_name': '', 'joint_angles': joint_angles}

        with open(os.path.join(action_dir, file_name), 'w', encoding='utf-8') as write_file:
            json.dump(self.sequence_data, write_file, ensure_ascii=False, indent=4)


try:
    import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

def set_params():
    params = dict()
    params['model_pose'] = 'BODY_25'
    params['model_folder'] = "../openpose/models/"

    return params

if __name__ == '__main__':

    params = set_params()
    skeleton_seq = SkeletonSequence()
    skeleton_seq_comp = SkeletonSequence()

    parser = argparse.ArgumentParser(description='Record an action or compare with an existing one')

    parser.add_argument('command', help="'record' or 'compare'")

    parser.add_argument('--folder', default='action1', help='Name of an action folder inside of recordings directory.')

    parser.add_argument('--data', help='Path to the json recording of an action.')

    args = parser.parse_args()

    if args.command == 'compare':
        assert args.data, "Argument --data is required for loading a recording from a json file."
        skeleton_seq_comp.load_from_json(args.data)

    try:
        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        stream = cv.VideoCapture(0)
        font = cv.FONT_HERSHEY_SIMPLEX

        startTime = datetime.now()
        while True:
            # Process Image
            datum = op.Datum()
            _, image = stream.read()
            datum.cvInputData = image
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))

            body_keypoints = datum.poseKeypoints
            if (body_keypoints.shape[0]) > 1:
                print('This program does not support more than 1 person in the frame!')
                break

            skeleton_seq.add(body_keypoints)

            # Display Image
            output_image = datum.cvOutputData
            cv.putText(output_image, "Press 'q' to quit", (20, 30),
                                font, 1, (0, 0, 0), 1, cv.LINE_AA)
            cv.imshow("Openpose result", output_image)

            key = cv.waitKey(1)
            if key == ord('q'):
                print("Time taken:", str(datetime.now() - startTime))
                print('Skeletons collected :: ', len(skeleton_seq.skeletons))

                if args.command == 'record':
                    assert args.folder, "Argument --folder is required to save this recording as a json file."

                    skeleton_seq.save_as_json(args.folder)

                break

    except Exception as e:
        print(e)
        sys.exit(-1)