import cv2, time, pandas
from datetime import datetime

first_frame = None

video = cv2.VideoCapture(0)

status_list = [None, None]
times = []

df = pandas.DataFrame(columns=["Start", "End"])

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame = cv2.absdiff(first_frame, gray)
    
    thresh_delth = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    
    thresh_delth = cv2.dilate(thresh_delth, None, iterations=2)
    
    (cnts,_) = cv2.findContours(thresh_delth.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    status_list.append(status)
    
    
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    
    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta", delta_frame)
    cv2.imshow("Threshold", thresh_delth)
    cv2.imshow("Color Frame", frame)
    
    key = cv2.waitKey(1)
    #time.sleep(0.015) #60fps
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
    print(status)

print(status_list)
print(times)

rows = []
for i in range(0, len(times)-1, 2):
    rows.append({"Start": times[i], "End": times[i + 1]})

df = pandas.DataFrame(rows)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()