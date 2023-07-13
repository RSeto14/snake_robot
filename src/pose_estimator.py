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

        if pose_results.pose_landmarks != None:
            RShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
            RElbow = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y)
            RHip = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y) 
            RSE = math.sqrt((RShoulder[0] - RElbow[0])*(RShoulder[0] - RElbow[0]) + (RShoulder[1] - RElbow[1])*(RShoulder[1] - RElbow[1]))
            REH = math.sqrt((RElbow[0] - RHip[0])*(RElbow[0] - RHip[0]) + (RElbow[1] - RHip[1])*(RElbow[1] - RHip[1]))
            RHS = math.sqrt((RHip[0] - RShoulder[0])*(RHip[0] - RShoulder[0]) + (RHip[1] - RShoulder[1])*(RHip[1] - RShoulder[1]))
            RCOS = (RSE*RSE + RHS*RHS - REH*REH) / (2*RSE*RHS)
            LShoulder = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)
            LElbow = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y)
            LHip = (pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)
            LSE = math.sqrt((LShoulder[0] - LElbow[0])*(LShoulder[0] - LElbow[0]) + (LShoulder[1] - LElbow[1])*(LShoulder[1] - LElbow[1]))
            LEH = math.sqrt((LElbow[0] - LHip[0])*(LElbow[0] - LHip[0]) + (LElbow[1] - LHip[1])*(LElbow[1] - LHip[1]))
            LHS = math.sqrt((LHip[0] - LShoulder[0])*(LHip[0] - LShoulder[0]) + (LHip[1] - LShoulder[1])*(LHip[1] - LShoulder[1]))
            LCOS = (LSE*LSE + LHS*LHS - LEH*LEH) / (2*LSE*LHS)

            R_theta = math.acos(RCOS)
            L_theta = math.acos(LCOS)

        else:
            R_theta = 0
            L_theta = 0


        return R_theta,L_theta
    
    def coefficient(self,R_theta,L_theta,alpha):

        new_alpha = math.sin(R_theta/2) - math.sin(L_theta/2)

        if new_alpha - alpha > 0.2:
            alpha = alpha + 0.2
        elif new_alpha - alpha < -0.2:
            alpha = alpha -0.2
        else:
            alpha = new_alpha
        
        return round(alpha,4)

    
    def display(self,frame,R_theta,L_theta,alpha):

        font = cv2.FONT_HERSHEY_SIMPLEX

        L_angle = round(math.degrees(L_theta),2)
        R_angle = round(math.degrees(R_theta),2)
        #文字（黒淵）
        cv2.putText(frame,"left angle:" + str(L_angle),(10,60), font, 2,(0,0,0),3,cv2.LINE_AA)
        cv2.putText(frame,"right angle:" + str(R_angle),(10,120), font, 2,(0,0,0),3,cv2.LINE_AA)
        cv2.putText(frame,"alpha:" + str(alpha),(10,180), font, 2,(0,0,0),3,cv2.LINE_AA)
        #文字（白）
        cv2.putText(frame,"left angle:" + str(L_angle),(10,60), font, 2,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"right angle:" + str(R_angle),(10,120), font, 2,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,"alpha:" + str(alpha),(10,180), font, 2,(255,255,255),2,cv2.LINE_AA)

        # display the frame
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Output', 900, 500)
        #cv2.resizeWindow('Output', 1900, 900)
        cv2.imshow('Output', frame)



def main():

    pe = pose_estimator()

    alpha = 0
    
    while pe.cap.isOpened():
        try:
            pose_results, frame = pe.estimator()
            R_theta, L_theta= pe.calculation(pose_results)
            alpha = pe.coefficient(R_theta,L_theta,alpha)
            pe.display(frame,R_theta,L_theta,alpha)
            
        except:
            break
            
        if cv2.waitKey(1) == 27: #press esc to close
            break

    pe.cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()