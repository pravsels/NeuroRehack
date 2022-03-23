# NeuroRehack-Project-1

low cost, audio-visual feedback system for neuro-rehabilitation exercise verification and report generation.

Video Demos Playlist: https://www.youtube.com/playlist?list=PLYUXcqZAo0xhRsWlfbZt_NONLY_MhdJzH

# Web Links

NeuroRehack '21 Page: https://www.neurorehack.com/

NeuroRehack Project Page Archive: https://archive.ph/BuHvh

NeuroRehack Main Page Archive: https://archive.ph/0dWOo

# Usage

To process the video file of an action, so as to store salient data from openpose as json, you'll need to provide the action folder's name as an argument:

  ```
  python create_json_recordings.py --folder=left_hand_raise
  ```

To re-generate json data from previously saved webcam footage, use the `--webcam` flag.

  The expected folder structure is:
  - video_recordings
    - left_hand_raise
      - left_hand_raise.mp4
    - right_arm_ex
    ...

To compare a user's current action (from webcam) to that of a recorded one, you'll need to provide the action folder's name as an argument. Note that the json data of this action (from the above step) needs to already exist.

```
python compare.py --folder=left_hand_raise
python compare_actions.py --folder=left_hand_raise
```

The expected folder structure is:
- json_recordings
  - left_hand_raise
    - left_hand_raise.json
  - right_arm_ex
  ...

If you've already generated an output video by recording your action using the command above and simply want the program to calculate a score, then set the `--no_webcam` flag:

```
python compare.py --folder=left_hand_raise --no_webcam
python compare_actions.py --folder=left_hand_raise --no_webcam
```

For windows users:
1. Update the model folder in config.json file to your openpose models folder:
    eg. C:\\Users\\hp\\openpose\\models

2. Update the path to your openpose installation in the compare_actions.py file at dir_path line 23

## Relevant Links
### Recommended tool for recording and editing action videos:-
https://webcamera.io/

### Datasets:-
https://docs.google.com/document/d/1KZ_6ZwL2hCQgLg7qI6_QH7wH0Z4PDG3t8uKVXPLAaFY/edit?usp=sharing

### Common Problems Faced while installing OpenPose:-
https://docs.google.com/document/d/1KZ_6ZwL2hCQgLg7qI6_QH7wH0Z4PDG3t8uKVXPLAaFY/edit?usp=sharing
