import cv2

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam successfully opened.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
