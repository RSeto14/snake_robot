from pose_estimator import pose_estimator
from snake_controller import controller
import cv2

ctrl = controller()
pe = pose_estimator()

def main():

    obs, alpha, time_steps, w, theta_max = ctrl.set_snake()

    for time_step in range(time_steps):

        if time_step % 100 ==0: #update alpha and capture every 50step

            pose_results, frame = pe.estimator()
            R_theta, L_theta= pe.calculation(pose_results)
            alpha = pe.coefficient(R_theta,L_theta,alpha)
            pe.display(frame,R_theta,L_theta,alpha)

        obs = ctrl.control(alpha, time_step, w, theta_max)

    pe.cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()