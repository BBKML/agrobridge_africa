#!/usr/bin/env python3
"""Simple utility to blur faces in a video using OpenCV Haar cascades.

Usage:
    python tools/blur_faces.py input.mp4 output.mp4 --blur 25

Notes:
 - This is a best-effort tool that detects faces with Haar cascades and applies a Gaussian blur
   to each detected face region for every frame.
 - For production/video-grade anonymization you may want to use a tracking+blur approach
   (this script is a straightforward per-frame detector + blur).
"""
import cv2
import sys
import argparse


def blur_faces_in_video(input_path, output_path, blur_strength=25):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    idx = 0
    print(f"Processing {frame_count} frames...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # extract ROI and apply blur
            roi = frame[y:y+h, x:x+w]
            k = max(1, (blur_strength // 2) * 2 + 1)
            blurred = cv2.GaussianBlur(roi, (k, k), 0)
            frame[y:y+h, x:x+w] = blurred

        out.write(frame)
        idx += 1
        if idx % 50 == 0:
            print(f"Processed {idx}/{frame_count} frames")

    cap.release()
    out.release()
    print(f"Saved blurred video to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video path')
    parser.add_argument('output', help='Output video path')
    parser.add_argument('--blur', type=int, default=25, help='Blur strength (odd integer recommended)')
    args = parser.parse_args()

    blur_faces_in_video(args.input, args.output, blur_strength=args.blur)


if __name__ == '__main__':
    main()
