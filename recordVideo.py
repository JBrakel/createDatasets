import cv2
import os

def record_video(output_filename, duration, fps=30.0, frame_size=(640, 480)):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)
    num_frames = int(duration * fps)

    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        out.write(frame)
        cv2.imshow('Recording', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Video saved as {output_filename}")



output_filename = ...
record_video(output_filename, duration=15, fps=30.0, frame_size=(640, 480))