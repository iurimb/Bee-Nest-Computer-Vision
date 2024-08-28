# Bee-Nest-Computer-Vision
Computer Vision project. Analysis of a bee nest. Bee detection, tracking and counting (in and out). Custom dataset. Using Yolov8, ByteTrack and Supervision. 

Detect and track bees going in and out of their nest is a challenging task. Bees are small, fast and blend in with the background. The main goal of the project was to develop an MVP and to test different ways of tracking the movement of the bees and counting if they go in or out. 

The following image contains an example of the nest with one bee that's just arrived and is going in, with the camera angle in such a way that it looks down on the nest. 

![frame_388](https://github.com/user-attachments/assets/9c14bbe8-6f29-4120-a075-cf920dd75322)

The dataset used was built by filming the nest for approximately 7 minutes. The film was made with a simple cellphone camera. I then extracted the first 2 minutes of the original video as individual frames and uploaded them to an online Annotation Tool. 

After annotating some 200~300 frames for object detection, I trained a yolov8-n network for bee detection. It's worth mentioning that, as a project decision, only the frames that contained bees standing/walking on the nest were prioritized. To detect a bee that's flying around is a way harder task, since flying bees are too fast for a simple camera to accurately represent them, they appear only as a distorted blur that's barely visible. The next image shows the issue at hand: 

![frame_386](https://github.com/user-attachments/assets/e94a531f-8d41-4363-a7d4-344fabd896ca)

Because of these specificities, tracking and, most importantly, counting the number of bees that go in and out become a challenging task. Hence, I tried different techniques and filters. Mainly, I tried: 1) using a line to analyse if the detected bee crossed it from inside out (going out) or the inverse (going in); 2) using two points as references and compare the first and last detections of a given bee (tracked) to those points to define if it's going in or out;

Both methods had their shortcomings due to the nature of the task, but also their successes. The methods using two points were, in the end, more effective.

The dataset is custom and is not available online. I have only uploaded the main python files and a few 'utils' python codes that I used (for example, video_to_frame). I've also uploaded a short video showing results. 

**OBSERVATION**: I did not have the time to adequately organize the code, I reckon it is a bit messy and there's work to be done there. I'm currently working on refactoring the personal projects I upload to github. 
