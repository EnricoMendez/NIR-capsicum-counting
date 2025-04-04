#!/usr/bin/env python3

# Author: Enrico Mendez
# Date: 03 April 2025
# Description: This script records video streams from RGB and mono 
#              cameras on a DepthAI device, saving them as separate 
#              MP4 files.

import os
import time
import depthai as dai
import cv2

# Function to find the next available number for video files
def get_next_filename(base_name, extension):
    i = 1
    while os.path.exists(f"{base_name}{i}{extension}"):
        i += 1
    return f"{base_name}{i}{extension}"

# Create pipeline
pipeline = dai.Pipeline()

# Configuration for the color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
cam_rgb.setInterleaved(False)

# Configuration for the mono (grayscale) camera
mono_left = pipeline.createMonoCamera()
mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
mono_left.setBoardSocket(dai.CameraBoardSocket.CAM_B)

# XLinkOut node to send color camera frames to the host
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("video_rgb")
cam_rgb.video.link(xout_rgb.input)

# XLinkOut node to send mono camera frames to the host
xout_mono = pipeline.createXLinkOut()
xout_mono.setStreamName("video_mono")
mono_left.out.link(xout_mono.input)

# Initialize the device and the pipeline
with dai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue(name="video_rgb", maxSize=60, blocking=False)
    q_mono = device.getOutputQueue(name="video_mono", maxSize=60, blocking=False)

    # Create video files to save the frames
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_rgb = cv2.VideoWriter(get_next_filename('rgb_video', '.mp4'), fourcc, 30.0, (1920, 1080))
    out_mono = cv2.VideoWriter(get_next_filename('mono_video', '.mp4'), fourcc, 30.0, (1280, 720), isColor=False)

    print("Recording videos. Press Ctrl+C to stop.")

    try:
        while True:
            frame_rgb = q_rgb.get().getCvFrame()
            frame_mono = q_mono.get().getCvFrame()

            out_rgb.write(frame_rgb)
            out_mono.write(frame_mono)

            # Display the images (optional)
            # cv2.imshow("RGB Stream", frame_rgb)
            # cv2.imshow("Mono Stream", frame_mono)

            if cv2.waitKey(1) == ord('q'):
                break

    except KeyboardInterrupt:
        pass

    finally:
        out_rgb.release()
        out_mono.release()
        cv2.destroyAllWindows()
