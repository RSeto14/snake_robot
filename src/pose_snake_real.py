from pose_estimator import pose_estimator
from snake_controller import controller
import cv2
import time

##アドレス登録
from socket import socket,AF_INET,SOCK_DGRAM
HOST=""
PORT=5000
SERVER="192.168.0.112"
sock=socket(AF_INET,SOCK_DGRAM)
sock.bind((HOST,PORT))
## 

ctrl = controller()
pe = pose_estimator()

def main():

    ctrl_time_step = 0.15 #[s]

    alpha = ctrl.alpha
    w = ctrl.w
    t = 0
    theta_max = ctrl.theta_max
    

    
    while pe.cap.isOpened():
        try:
            pose_results, frame = pe.estimator()
            R_theta, L_theta= pe.calculation(pose_results)
            alpha = pe.coefficient(R_theta,L_theta,alpha)
            pe.display(frame,R_theta,L_theta,alpha)

            action = ctrl.action(alpha, w, t, theta_max)
            #print("action",action)
            t = t + ctrl_time_step 
            print(t)
            ##送信
            msg=f"{action[0]},{action[1]},{action[2]},{action[3]},{action[4]},{action[5]},{action[6]},{action[7]},{action[8]},{action[9]},{action[10]},{action[11]}"
            sock.sendto(msg.encode(),(SERVER,PORT))

            print("msg",msg)

            
        except:
            break
            
        if cv2.waitKey(1) == 27: #press esc to close
            break

    pe.cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()