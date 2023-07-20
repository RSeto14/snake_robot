import gym
from gym import wrappers
from math import cos, sin, acos, asin, atan, pi
import numpy as np
import snake
import glfw

import cv2
import mediapipe as mp
import math

def main():

    ## Setting ######################################
    env = gym.make('Snake-v0')
    ctrl_time_step  = 0.005 #[s]
    obs = env.reset()
    update = 50 # update capture every 50 step
    time_step = 0 # initialize time step
    #################################################

    ## initialize pose estimator #################################################
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0) # input image from camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    ###############################################################################

    while cap.isOpened():
        try:
            if time_step % update ==0: 
                ## Mediapipe ######################################################################################################################
                _, frame = cap.read() # read frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB
                pose_results = pose.process(frame_rgb) # process the frame for pose detection
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # draw skeleton on the frame
                frame = cv2.flip(frame, 1) # Flip horizontal

                "------ change here -------------------------------------------------------------------------------------"
                if pose_results.pose_landmarks != None:
                    RShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                    #https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python
                else:
                    RShoulder = ("None","None")

                print("RShoulder",RShoulder)
                "--------------------------------------------------------------------------------------------------------"
                ##################################################################################################################################

                ## openCV ############################################################################################
                #text
                cv2.putText(frame,"enter text here",(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),3,cv2.LINE_AA)
                
                # display the frame
                cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Output', 900, 500)
                cv2.imshow('Output', frame)
                #######################################################################################################



            ## controller ############################################################################################
            "-------- change here -------------------------------------------------------------------------------------"
            t = time_step*ctrl_time_step
            action = np.zeros(12) # joint angle
            action[0] = sin(t)
            "-----------------------------------------------------------------------------------------------------------"
            ##########################################################################################################


            ## gym mujoco ##############################################################################################
            env.render()
            glfw.set_window_size(env.viewer.window, width=1000, height=900)#mujoco window size
            obs, reward, done, info = env.step(action)
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