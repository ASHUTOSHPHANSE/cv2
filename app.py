import streamlit as st
import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def main():
    st.title("Exercise Recognition with Streamlit")

    cap = cv2.VideoCapture(0)

    up = False
    counter = 0
    count = 0
    counter_pushups = 0
    pushup_up, pushup_down = False, False
    position = None
    counter_bench_press = 0
    bench_press_up = False
    bench_press_down = False
    counter_legs = 0
    legs_up = False
    legs_down = False
    counter_curl = 0
    curl_up = False
    curl_down = False
    counter_triceps = 0
    triceps_up = False
    triceps_down = False

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                points[id] = (cx, cy)

            # Your existing exercise recognition code here
           


            cv2.circle(img, points[12], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255,0,0), cv2.FILLED)
            cv2.circle(img, points[13], 15, (255,0,0), cv2.FILLED)
            
            # push ups
            if points[11][1] < points[23][1] and points[12][1] < points[24][1] and points[12][0] < points[11][0]:
                        if not pushup_up:
                            print("Push-up Up")
                            pushup_up = True
                            pushup_down = False
                            counter_pushups += 1
            elif points[11][1] > points[23][1] and points[12][1] > points[24][1] and points[12][0] > points[11][0]:
                        if not pushup_down:
                            print("Push-up Down")
                            pushup_up = False
                            pushup_down = True

            
            #sholder
            if not up and points[14][1] + 40 < points[12][1]:
                print("UP")
                up = True
                counter += 1
            if not up and points[12][1] and points[11][1] >= points[14][1] and points[13][1]:
                print("UP")
                up = True
                counter += 1    
            elif points[14][1] > points[12][1]:
                print("Down")
                up = False
                
            elif points[12][1] and points[11][1] <= points[14][1] and points[13][1]:
                print("Down")
                up = False
            #bench press
            
            
            if points[11][1] < points[13][1] and points[15][1] > points[23][1]:
                if not bench_press_up:
                    print("Bench Press Up")
                    bench_press_up = True
                    bench_press_down = False
                    counter_bench_press += 1
            elif points[11][1] > points[13][1] and points[15][1] < points[23][1]:
                if not bench_press_down:
                    print("Bench Press Down")
                    bench_press_up = False
                    bench_press_down = True
                    
            # Leg Exercise (Assuming squat by checking knee positions)
            if points[25][1] < points[23][1] and points[27][1] < points[24][1]:
                if not legs_up:
                    print("Legs Exercise Up")
                    legs_up = True
                    legs_down = False
                    counter_legs += 1
            elif points[25][1] > points[23][1] and points[27][1] > points[24][1]:
                if not legs_down:
                    print("Legs Exercise Down")
                    legs_up = False
                    legs_down = True
                    
            # Bicep Curl
            if points[11][1] < points[13][1] and points[13][1] < points[15][1]:
                if not curl_up:
                    print("Bicep Curl Up")
                    curl_up = True
                    curl_down = False
                    counter_curl += 1
            elif points[11][1] > points[13][1] and points[13][1] > points[15][1]:
                if not curl_down:
                    print("Bicep Curl Down")
                    curl_up = False
                    curl_down = True   
                
            # Triceps Extension
            if points[11][1] > points[13][1] and points[13][1] > points[15][1]:
                if not triceps_up:
                    print("Triceps Extension Up")
                    triceps_up = False
                    triceps_down = True
                    counter_triceps += 1
            elif points[11][1] < points[13][1] and points[13][1] < points[15][1]:
                if not triceps_down:
                    print("Triceps Extension Down")
                    triceps_up = True
                    triceps_down = False            
        
        cv2.putText(img,f"Curl: {counter_curl} | Pushup: {count} | Sholder: {counter} |Triceps: {counter_triceps} | Bench Press: {counter_bench_press} | Legs: {counter_legs}", (100,150),cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,255),2)


        
        cv2.imshow("img",img)
        cv2.waitKey(1)
        if key == 27 :
            break                
        st.image(img, channels="BGR", use_column_width=True)

if __name__ == "__main__":
    main()
