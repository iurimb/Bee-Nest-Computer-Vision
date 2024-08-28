# Bee-Nest-Computer-Vision Project

## Objectives: 
**Analysis of a bee nest. Bee detection, tracking and counting (in and out). Custom dataset. Using Yolov8, ByteTrack and Supervision.**
Detect and track bees going in and out of their nest is a challenging task. Bees are small, fast and blend in with the background. The main goal of the project was to develop a proof of concept and to test different ways of tracking the movement of the bees and counting if they go in or out. 

Worth mentioning I also fooled around with getting the time and counting the amount of bees in the current frame by using a zone of interest polygon (invisible in the video), and with the HeatMapAnnotator as well as TraceAnnotator. 

## Disclaimers 
The code is functionable, but not yet organized, so I also couldn't yet organize the python environment. You might note (until I solve this) that there are many commented lines in the codes, and even parts of it that are 'outdated' (for example, some polygon shapes not being used). 

The dataset used was a custom video I can't upload. I show examples below of the type of image taken, so it's reproducible.

## Folders 

- detect_count_and_track: folder containing three scripts to detect, track and count (ins and outs) of bees in nests. See section "Running the codes" for details. 
- results: folder with short videos representing the outputs of each method. 
- training_loop: script to train a yolo model for object detection.
- Weights: trained model weights (remember it heavily depends on the initial setting and conditions. You can re-train a network using new data and use the codes here available to track and count, but some changes might be necessary to adapt for the use_case, mainly in the method of counting.
- Line_Zone: Line_Zone code I use that contains a modified function for annotating info. You could substitute the original line_zone file with mine or only copy the modified method code into yours ("_annotate_anything_count"). Alternatevely, you can give it a different name and import it. 

## About the task 

The following image contains an example of the nest with one bee that's just arrived and is going in, with the camera angle in such a way that it looks down on the nest. 

![frame_388](https://github.com/user-attachments/assets/9c14bbe8-6f29-4120-a075-cf920dd75322)

The dataset used was built by filming the nest for approximately 7 minutes. The film was made with a simple cellphone camera. I then extracted the first 2 minutes of the original video as individual frames and uploaded them to an online Annotation Tool. 

After annotating some 200~300 frames for object detection, I trained a yolov8-n network for bee detection. It's worth mentioning that, as a project decision, only the frames that contained bees standing/walking on the nest were prioritized. To detect a bee that's flying around is a way harder task, since flying bees are too fast for a simple camera to accurately represent them, they appear only as a distorted blur that's barely visible. The next image shows the issue at hand: 

![frame_386](https://github.com/user-attachments/assets/e94a531f-8d41-4363-a7d4-344fabd896ca)

Because of these specificities, tracking and, most importantly, counting the number of bees that go in and out become a challenging task. Hence, I tried different techniques and filters. The three methods available in "detect_count_and_track" are: 1) using lines and crossing lines as references; 2) comparing the first position of detection of each tracked bee to the last one; 3) using two points as references and compare the first and last detections of a given bee (tracked) to those points to define if it's going in or out. You'll find three source codes correspondently.

Worth mentioning it was firstly considered solving this problem by modelling it as a classification problem, that'd have as input the cropped images of the last frames in which a tracked bee would appear. The idea behind it being the pose of the bee could indicate if it's going in or out. But the images cropped were too low resolution and this method, that was promising, had to be dropped. 

All methods had their value, but also their shortcomings due to the nature of the task. The methods using two points or even just comparing first to last position were more effective than a single line or two lines (as the code available). This project was merely experimental and is by no means a finished product.

## Running the codes
Codes are found in the "training_loop" and "detect_count_and_track" folders. 
The training_loop code is easily executed by just inserting your 'data.yaml' file_path into the "data" variable. 

The detect, track and count codes are also easily executable (abstracting from the dependencies... I'm on it ASAP) by plugging in the model_weights path and the video_file path into the code. Below the imports, you'll find:

model_weight = "INSERT_WEIGHTS_PATH"
model = YOLO('model_weight')
VIDEO_PATH = "INSERT_VIDEO_PATH"

That should do it. 


### Some final observations 
#### 1) I used a modified version of the annotator method in "LineZoneAnnotator" to display information on the videos. I uploaded my "Line_Zone" file together with the code. 
**2)** I can't upload the original video used for training and testing. But I've uploaded the weights of the trained netowrk and they can be used for similar tasks.
**3)** I did not have the time to adequately organize the code, I reckon it is a bit messy and there's work to be done there. I'm currently working on refactoring the personal projects I upload to github. 
