import cv2
import mediapipe as mp
import math

class pose_estimator():

    def __init__(self):
        ## initialize pose estimator
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    
    def estimator(self):
        # read frame
        _, frame = self.cap.read()

        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # process the frame for pose detection
        pose_results = self.pose.process(frame_rgb)

        # draw skeleton on the frame
        self.mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        #Flip horizontal
        frame = cv2.flip(frame, 1) 


        return pose_results, frame
    

    def calculation(self, pose_results):

        mp_pose = self.mp_pose

        "------ change here -------------------------------------------------------------------------------------"

        if pose_results.pose_landmarks != None:
            RShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
            #https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python
            RShoulder_x = RShoulder[0]

        else:
            RShoulder_x = 0


        return RShoulder_x
    
        "--------------------------------------------------------------------------------------------------------"
    


    
    def display(self,frame):
        #text
        cv2.putText(frame,"enter text here",(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),3,cv2.LINE_AA)
        
        # display the frame
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Output', 900, 500)
        #cv2.resizeWindow('Output', 1900, 900)
        cv2.imshow('Output', frame)



def main():

    pe = pose_estimator()

    
    while pe.cap.isOpened():
        try:
            pose_results, frame = pe.estimator()
            x = pe.calculation(pose_results)
            print(x)
            pe.display(frame)
            
        except:
            break
            
        if cv2.waitKey(1) == 27: #press esc to close
            break

    pe.cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()