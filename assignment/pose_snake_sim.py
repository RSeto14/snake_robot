from pose_estimator import pose_estimator
from snake_controller import controller
import cv2

ctrl = controller()
pe = pose_estimator()

def main():

    time_steps = ctrl.set_snake()

    for time_step in range(time_steps):

        if time_step % 100 ==0: #update alpha and capture every 50step

            pose_results, frame = pe.estimator()
            x = pe.calculation(pose_results)
            pe.display(frame)

        obs = ctrl.control(time_step)

    pe.cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()