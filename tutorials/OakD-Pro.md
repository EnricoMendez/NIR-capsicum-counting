
# Recording Video with Python and the Oak-D Pro Camera

This documentation provides a complete guide to recording video from an Oak-D Pro camera using Python.

## 1. Introduction

The Oak-D Pro by Luxonis is a powerful depth camera equipped with:

- A 12MP RGB sensor (IMX378)
- Two monochrome sensors (OV9282)

This guide focuses on capturing **RGB and mono streams as video files** using Python and the [DepthAI SDK](https://docs.luxonis.com/).

---

## 2. Requirements

### Hardware
- Oak-D Pro camera
- USB3 cable
- PC (Windows/Linux/macOS)

### Software
- Python ≥ 3.7
- [DepthAI SDK](https://github.com/luxonis/depthai-python)
- OpenCV (`cv2`)

### Installation

```bash
pip install depthai opencv-python
```

---

## 3. Understanding the Oak-D Pro Camera

| Sensor | Model    | Type         |
|--------|----------|--------------|
| CAM_A  | IMX378   | RGB (color)  |
| CAM_B  | OV9282   | Mono (left)  |
| CAM_C  | OV9282   | Mono (right) | 

In this setup, we use:
- RGB camera for standard video
- Left mono camera for NIR capture

---

## 4. DepthAI Pipeline Overview

To interact with the Oak-D Pro, DepthAI uses a pipeline architecture:

1. **Create a pipeline**
2. **Define camera nodes**
3. **Define XLinkOut nodes to send data to host**
4. **Link camera outputs to streams**
5. **Run the pipeline on the device**
6. **Receive and process frames on the host**

---

## 5. Creating the Video Capture Script

### Step 1: Set Up the Pipeline

```python
pipeline = dai.Pipeline()
```

### Step 2: Configure RGB and Mono Cameras

```python
# RGB
cam_rgb = pipeline.createColorCamera()
cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

# Mono (left)
mono_left = pipeline.createMonoCamera()
mono_left.setBoardSocket(dai.CameraBoardSocket.CAM_B)
mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
```

### Step 3: Create XLink Outputs

```python
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("video_rgb")
cam_rgb.video.link(xout_rgb.input)

xout_mono = pipeline.createXLinkOut()
xout_mono.setStreamName("video_mono")
mono_left.out.link(xout_mono.input)
```

### Step 4: Start Device and Process Streams

```python
with dai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("video_rgb", maxSize=60, blocking=False)
    q_mono = device.getOutputQueue("video_mono", maxSize=60, blocking=False)

    while True:
        frame_rgb = q_rgb.get().getCvFrame()
        frame_mono = q_mono.get().getCvFrame()
        # Save or display
```

---

## 6. Saving the Video with OpenCV

```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_rgb = cv2.VideoWriter('rgb_video.mp4', fourcc, 30.0, (1920, 1080))
out_mono = cv2.VideoWriter('mono_video.mp4', fourcc, 30.0, (1280, 720), isColor=False)

out_rgb.write(frame_rgb)
out_mono.write(frame_mono)
```

Use `.release()` at the end to close the files safely.

---

## 7. References

- [DepthAI SDK Documentation](https://docs.luxonis.com/)
- [Luxonis Oak-D Pro](https://docs.luxonis.com/projects/hardware/en/latest/pages/DM9095.html)
