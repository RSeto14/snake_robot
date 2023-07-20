import cv2
import mediapipe as mp
import math

def main():

    ## initialize pose estimator
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

    
    while cap.isOpened():
        try:
            # read frame
            _, frame = cap.read()
            # convert to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # process the frame for pose detection
            pose_results = pose.process(frame_rgb)
            # draw skeleton on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            #Flip horizontal
            frame = cv2.flip(frame, 1)
            

            "------ change here -------------------------------------------------------------------------------------"

            if pose_results.pose_landmarks != None:
                RShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                #https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python

            else:
                RShoulder = ("None","None")

            print(RShoulder)
            "--------------------------------------------------------------------------------------------------------"

            #text
            cv2.putText(frame,"enter text here",(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),3,cv2.LINE_AA)
            
            # display the frame
            cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Output', 900, 500)
            cv2.imshow('Output', frame)
            
        except:
            break
            
        if cv2.waitKey(1) == 27: #press esc to close
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()