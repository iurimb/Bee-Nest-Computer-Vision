import supervision as sv
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from supervision import Position

model = YOLO('best_new_bees.pt')
ABELHA_CIMA = "abelhas_cima.mp4"
ABELHA_CIMA_10FPS = "part3600-12900-10fps.avi"
sasa = r"C:\Users\noz\Documents\Clutch\Abelhas\part0-3600ABELHA_LATERAL.mp4"
vcap = cv2.VideoCapture(ABELHA_CIMA)
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

#tracker=sv.ByteTrack() #frame_rate: int = 30)
width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
 # choose codec according to format needed
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('tracking_counting_bees.mp4', fourcc, 15, (int(width), int(height)))

#input(width)
#input(height)
tracker = sv.ByteTrack(0.4, 50)
frames_generator = sv.get_video_frames_generator(ABELHA_CIMA)
# frames_generator = sv.get_video_frames_generator(ABELHA_CIMA_10FPS)
#video = cv2.VideoCapture(sasa)
#fps = video.get(cv2.CAP_PROP_FPS)
#input(fps)

'''LINE INPUTS. First, from left to right. Second, from right to left'''
x_start, y_start = 130, 360
x_end, y_end = 390, 360

#ASSIM É BEM PIOR
#x_end, y_end = 130, 355
#x_start, y_start = 390, 355

in_count = 0
out_count = 0

start, end = sv.Point(x_start, y_start), sv.Point(x_end, y_end)
line_start = (x_start, y_start)
line_end = (x_end, y_end)

#LINEZONE TRIGGERING ANCHORS (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT) 
line_zone = sv.LineZone(start=start, end=end, triggering_anchors=[sv.Position.CENTER])#, sv.Position.BOTTOM_CENTER])




annotator = sv.LineZoneAnnotator()
idx = 0
count_crossed = 0
'''
#cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
while video.isOpened():
    ret, frame = video.read()
    print(ret, frame)
    if ret == True: 
    # Display the resulting frame 
'''
polygon = np.array([
    [130, 300], #top_left
    [390, 300], #top_right
    [399, 450], #bottom_right
    [130, 450] #bottom_left
])

polygon_zone = sv.PolygonZone(polygon=polygon)
#zone_annotator = sv.PolygonZoneAnnotator(zone=polygon_zone, color=sv.Color.white(), thickness=6, text_thickness=6, text_scale=4)
thingy_counter = 0
for frame in frames_generator:
    #input(frame)
    idx = idx+1
    result = model.predict(frame, conf=0.4)[0]
    detections = sv.Detections.from_ultralytics(result)
    detections = tracker.update_with_detections(detections)
    
    #print(detections.tracker_id)
    orig_img = result.orig_img
    #print("LEN", len(detections))
    if detections.tracker_id.any():
        labels = [
        f"#{tracker_id} {class_name} {confidence:.2f}"
        for tracker_id, class_name, confidence
        in zip(detections.tracker_id, detections['class_name'], detections.confidence)
        ]
    print("index", idx)
    print("DETEC_ID", detections.tracker_id)
    #print("LABELS", labels)
    print("DETECTIONS", detections)
    img = cv2.line(orig_img, line_start, line_end, color=(255, 0, 0), thickness=2) 
    annotated_frame = bounding_box_annotator.annotate(scene=img.copy(), detections=detections)
    #annotated_frame = zone_annotator.annotate(scene=annotated_frame)
    #input(type(annotated_frame)) NPARRAY
    
    if(len(detections.tracker_id) > 0):
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        thingy = polygon_zone.trigger(detections=detections)
        
        if thingy == True:
            thingy_counter = thingy_counter+1
        print("THINGY", thingy, thingy_counter)
        
    elif(len(detections)>0 and detections.tracker_id == 0):
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

            
    crossed_in, crossed_out = line_zone.trigger(detections)
    
    #nao vou usar pq buga E pq fica ruim na tela
    #annotator.annotate(frame=annotated_frame, line_counter=line_zone)
    in_count = line_zone.in_count
    out_count = line_zone.out_count
    annotator._annotate_count(annotated_frame, sv.Point(100, 100), f"ABELHAS_IN {in_count}", True)
    annotator._annotate_count(annotated_frame, sv.Point(100, 120), f"ABELHAS_OUT {out_count}", False)

    print(crossed_in, crossed_out)
    #print("crossed", crossed_in, crossed_out)
    if np.any(crossed_in) or np.any(crossed_out):
        print("detec_crossed_in", detections[crossed_in])
        count_crossed = count_crossed+1
        #input("CONTOU!")
    
    video.write(annotated_frame)
    cv2.imshow("frame", annotated_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
        #TODO pensar em uma lógica pra anotar a detecção sem o ID
    #img_to_show = Image.fromarray(annotated_frame)
    #img_to_show.show()

        #input("stop")
        #detections_crossed_in = detections[crossed_in]
        
        #print("DETECTIONS_FULL", detections)
        #print("DETECTIONS_CROSSE", detections_crossed_in)
        #print("CROSSED", crossed_in, crossed_out)
        #input("veja ai")
       
        #for xyxy in detections_crossed_in.xyxy:
        #    crop = sv.crop_image(frame, xyxy)

        