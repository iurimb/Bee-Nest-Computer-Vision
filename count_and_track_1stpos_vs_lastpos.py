import cv2
import supervision as sv
from ultralytics import YOLO

import numpy as np
from PIL import Image
from supervision import Position
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from collections import defaultdict
from ultralytics.utils.plotting import Annotator, colors

# Importing datetime 
import datetime 
import time
from time import perf_counter
from timeit import default_timer as cronometro

# importing whole module
from tkinter import *
from tkinter.ttk import *
import datetime 
# importing strftime function to
# retrieve system's time
from time import strftime
#import time
from datetime import timedelta

# Initializing a date and time 
'''
inicio = cronometro()
# Seu código aqui


#start = time.perf_counter()
#print(start)

#input(dt)

while True: 
    fim = cronometro()
    time_delta = datetime.timedelta(seconds=fim-inicio) 
    #print(time_delta)
    #print(inicio)    
    date_and_time_of_video = (date_and_time_of_video + time_delta)
    #date_and_time_of_video = date_and_time_of_video + time_sec
    print(date_and_time_of_video)
#current_time_24hr = time.strftime("%H:%M:%S")
#current_time_12hr = time.strftime("%I:%M:%S %p")
#current_date = time.strftime("%Y-%m-%d")
'''

model_weight = "INSERT_WEIGHTS_PATH"
model = YOLO('model_weight')
VIDEO_PATH = "INSERT_VIDEO_PATH"
video_da_vez = VIDEO_PATH
vcap = cv2.VideoCapture(video_da_vez)
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()
track_history = defaultdict(list)

#tracker=sv.ByteTrack() #frame_rate: int = 30)
width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
 # choose codec according to format needed
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('Tracking_Counting_With_Time.mp4', fourcc, 15, (int(width), int(height)))

#input(width)
#input(height)
tracker = sv.ByteTrack(0.25, 50)
frames_generator = sv.get_video_frames_generator(video_da_vez)
heat_map_annotator = sv.HeatMapAnnotator()
#video = cv2.VideoCapture(sasa)
#fps = video.get(cv2.CAP_PROP_FPS)
#input(fps)

date_and_time_of_video = datetime.datetime(2024, 5, 31, 7, 10, 0)






'''CRIA A PRIMEIRA LINHA. First, from left to right. Second, from right to left'''
x_start_out, y_start_out = 130, 363
x_end_out, y_end_out = 390, 363

#ASSIM É BEM PIOR
#x_end, y_end = 130, 355
#x_start, y_start = 390, 355

out_count = 0
alt_out_count = 0

start_out, end_out = sv.Point(x_start_out, y_start_out), sv.Point(x_end_out, y_end_out)
out_line_start = (x_start_out, y_start_out)
out_line_end = (x_end_out, y_end_out)

#LINEZONE TRIGGERING ANCHORS (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT) 
out_line_zone = sv.LineZone(start=start_out, end=end_out, triggering_anchors=[sv.Position.CENTER])#, sv.Position.BOTTOM_CENTER])

'''CRIA A SEGUNDA LINHA. First, from left to right. Second, from right to left'''
#x_start_in, y_start_in = 130, 349
#x_end_in, y_end_in = 390, 349

x_start_in, y_start_in = 130, 365
x_end_in, y_end_in = 390, 365


in_count = 0
alt_in_count = 0
#ASSIM É BEM PIOR
#x_end, y_end = 130, 355
#x_start, y_start = 390, 355

start_in, end_in = sv.Point(x_start_in, y_start_in), sv.Point(x_end_in, y_end_in)
in_line_start = (x_start_in, y_start_in)
in_line_end = (x_end_in, y_end_in)

#LINEZONE TRIGGERING ANCHORS (TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT) 
in_line_zone = sv.LineZone(start=start_in, end=end_in, triggering_anchors=[sv.Position.CENTER])#, sv.Position.BOTTOM_CENTER])

#x_start, y_start = 130, 360
#x_end, y_end = 390, 360
#alternative_in_count = 0

annotator = sv.LineZoneAnnotator()
idx = 0
count_crossed = 0

in_zone_counter = 0
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

polygon_special = Polygon([[130, 300], [390, 300], [399, 450], [130, 450]])

pts = np.array([
    [130, 300], #top_left
    [390, 300], #top_right
    [399, 450], #bottom_right
    [130, 450] #bottom_left
], np.int32)

COLORS = sv.ColorPalette.DEFAULT
#COLORS = sv.Color.DEFAULT
#input(COLORS.colors)
pts = pts.copy().reshape((-1, 1, 2))
#input(pts.shape)
#input(polygon.shape)
polygon_zone = sv.PolygonZone(polygon=polygon)
#zone_annotator = sv.PolygonZoneAnnotator(zone=polygon_zone, color=sv.Color.white(), thickness=6, text_thickness=6, text_scale=4)
#thingy_counter = 0
list_to_record_tracking_in_zone = []

lost_tracks_list = []


for frame in frames_generator:
    start = time.time()
    #print("lost", tracker.lost_tracks)
    #print("tracked", tracker.tracked_tracks)
    
    
    #print("dict", track_history)
    #input(frame)
    idx = idx+1
    result = model.predict(frame, conf=0.4)[0]
    #result = model.track(frame, persist=True, conf=0.4)[0]
    #track = track_history[track_id]
    #print("hist", track_history)

            
    
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
    #img = cv2.polylines(orig_img, [pts], True, (0,0,255), 5)
    #img = cv2.line(orig_img, in_line_start, in_line_end, color=(255, 0, 0), thickness=2) 
    #img = cv2.line(img, out_line_start, out_line_end, color=(0, 255, 0), thickness=2) 
    

    annotated_frame = bounding_box_annotator.annotate(scene=frame.copy(), detections=detections)
    annotated_frame = sv.draw_polygon(scene=annotated_frame, polygon=polygon, color=COLORS.colors[0])
    annotated_frame = heat_map_annotator.annotate(scene=frame.copy(), detections=detections)
    #annotated_frame = zone_annotator.annotate(scene=annotated_frame)
    #input(type(annotated_frame)) NPARRAY
    
    if(len(detections.tracker_id) > 0):
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        annotated_frame = trace_annotator.annotate(scene=annotated_frame.copy(), detections=detections)
        
        boxes = result.boxes.xyxy.cpu()
        track_ids = detections.tracker_id.tolist()
        clss = result.boxes.cls.cpu().tolist() 

        print("BOXES AND TRACK_IDS", boxes, track_ids)
        for box, track_id, cls in zip(boxes, track_ids, clss):
            bbox_center = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2  # Bbox center
            track = track_history[track_id]  # Tracking Lines plot
            #print("TOAQUI")
            #print("TRACK", track)
            #print("TRACKHISTORY", track_history)
            track.append((float(bbox_center[0]), float(bbox_center[1])))
            if len(track) > 30:
                track.pop(0)
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                #print(points)
                #input (points)
            cv2.polylines(frame, [points], isClosed=False, color=colors(cls, True), thickness=2)
        if polygon_special.contains(Point((bbox_center[0], bbox_center[1]))):
            if track_id not in list_to_record_tracking_in_zone:
                list_to_record_tracking_in_zone.append(track_id)
                in_zone_counter = in_zone_counter+1

        #in_polygon_per_frame = len(polygon_zone.trigger(detections=detections))
        #if detections.tracker_id not in list_to_record_tracking_in_zone:
        #    in_zone_counter = in_zone_counter + 1
        #    list_to_record_tracking_in_zone.append(detections.tracker_id)
        #if thingy == True:
        #    thingy_counter = thingy_counter+1
        #print("THINGY", thingy, thingy_counter)
        
    elif(len(detections)>0 and detections.tracker_id == 0):
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        boxes = result.boxes.xyxy.cpu()
        #track_ids = detections.tracker_id.int().cpu().tolist() 
        for box in boxes:
            bbox_center = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2  # Bbox center

        #if polygon_special.contains(Point((bbox_center[0], bbox_center[1]))):
        #    in_zone_counter = in_zone_counter+1
    
    
    elif(len(detections) == 0):
        list_to_record_tracking_in_zone.clear()
        in_zone_counter = 0

    if tracker.lost_tracks:
        for losttrack in tracker.lost_tracks:
            if losttrack not in lost_tracks_list:
                lost_tracks_list.append(losttrack)
                #pega o primeiro e o ultimo ponto (0 e -1) do ID correspondente. Pega só o Y [1] no fim
                first_y_position = track_history[losttrack.external_track_id][0][1]
                last_y_position = track_history[losttrack.external_track_id][-1][1]
                
                if (first_y_position - last_y_position) < 0:
                    alt_out_count = alt_out_count + 1
                else: 
                    alt_in_count = alt_in_count + 1

                #print(first_y_position, last_y_position)
                #input("PAREI")
                #print(losttrack.track_id, losttrack.frame_id, losttrack.start_frame)#print(losttrack.split())
    
    crossed_in, _ = in_line_zone.trigger(detections)
    _, crossed_out = out_line_zone.trigger(detections)
    #nao vou usar pq buga E pq fica ruim na tela
    #annotator.annotate(frame=annotated_frame, line_counter=line_zone)
    in_count = in_line_zone.in_count
    out_count = out_line_zone.out_count
    #annotator._annotate_count(annotated_frame, sv.Point(150, 100), f"ABELHAS_IN {in_count} (BLUE_LINE) ", True)
    #annotator._annotate_count(annotated_frame, sv.Point(150, 120), f"ABELHAS_OUT {out_count} (GREEN_LINE)", False)
    annotator._annotate_anything_count(annotated_frame, sv.Point(120, 20), f"ABELHAS NO FRAME ATUAL {in_zone_counter}")

    annotator._annotate_anything_count(annotated_frame, sv.Point(120, 50), f"ENTRADA DE ABELHAS {alt_in_count}")
    annotator._annotate_anything_count(annotated_frame, sv.Point(120, 80), f"SAIDA DE ABELHAS {alt_out_count}")

    #annotator._annotate_anything_count(annotated_frame, sv.Point(150, 270), f"TEMPO {date_and_time_of_video}")


    print(crossed_in, crossed_out)
    #print("crossed", crossed_in, crossed_out)
    if np.any(crossed_in) or np.any(crossed_out):
        print("detec_crossed_in", detections[crossed_in])
        #count_crossed = count_crossed+1
        #input("CONTOU!")
    
    
    end = time.time()
    timedelta_total = end - start
    if video_da_vez == ABELHA_CIMA_10FPS:
        timedelta_total = timedelta_total/3
    date_and_time_of_video = date_and_time_of_video + timedelta(seconds=timedelta_total)  
    date_and_time_of_video_print = date_and_time_of_video.strftime("%d/%m/%Y, %H:%M:%S")
    annotator._annotate_anything_count(annotated_frame, sv.Point(120, 110), f"{date_and_time_of_video_print}")



    #video.write(annotated_frame)
    cv2.imshow("frame", annotated_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

       
        #for xyxy in detections_crossed_in.xyxy:
        #    crop = sv.crop_image(frame, xyxy)

        
