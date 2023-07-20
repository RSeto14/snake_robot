from math import cos, sin, acos, asin, atan, pi
import numpy as np

import cv2
import mediapipe as mp
import math

## register address ########################
from socket import socket,AF_INET,SOCK_DGRAM
HOST=""
PORT=5000
SERVER="192.168.0.112"
sock=socket(AF_INET,SOCK_DGRAM)
sock.bind((HOST,PORT))
############################################

def main():

    ## Setting ######################################
    ctrl_time_step = 0.15 #[s]
    update = 1 #update capture every 1 step
    time_step = 0 # initialize time step
    #################################################

    ## initialize pose estimator #################################################
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0) # input image from camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    ##############################################################################

    while cap.isOpened():
        try:
            if time_step % update ==0: 
                ## mediapipe #######################################################################################
                _, frame = cap.read() # read frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB
                pose_results = pose.process(frame_rgb) # process the frame for pose detection
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # draw skeleton on the frame
                frame = cv2.flip(frame, 1) # Flip horizontal
                ####################################################################################################

                ## Calculate joint angle #################################################################################
                "------ change here -------------------------------------------------------------------------------------"
                if pose_results.pose_landmarks != None:
                    RShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                    #https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python
                else:
                    RShoulder = ("None","None")

                print("RShoulder",RShoulder)
                "--------------------------------------------------------------------------------------------------------"
                ##########################################################################################################

                ## openCV #############################################################################################
                #text
                cv2.putText(frame,"enter text here",(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),3,cv2.LINE_AA)
                
                # display the frame
                cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Output', 900, 500)
                cv2.imshow('Output', frame)
                #######################################################################################################



            ## controller #################################################
            "-------- change here ----------------------------------------"
            t = time_step*ctrl_time_step
            action = np.zeros(12) # joint angle
            action[0] = sin(t)
            "-------------------------------------------------------------"
            ###############################################################

            ## send action to real robot ###############################################################################
            msg=f"{action[0]},{action[1]},{action[2]},{action[3]},{action[4]},{action[5]},{action[6]},{action[7]},{action[8]},{action[9]},{action[10]},{action[11]}"
            sock.sendto(msg.encode(),(SERVER,PORT))
            print("msg",msg)
            ############################################################################################################

            time_step += 1

        except:
            break
            
        if cv2.waitKey(1) == 27: #press esc to close
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
