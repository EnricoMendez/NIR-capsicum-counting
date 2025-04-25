# Near-Infrared-Based Capsicum Counting Algorithm Using YOLO11

This repository contains a complete pipeline for capsicum detection and counting using YOLO11. It includes training scripts, custom object-tracking configurations, and video input processing for tracker testing.

## Overview

The project aims to provide an end-to-end solution for counting fruits in RGB and NIR video sequences using a custom-trained YOLOv5 model. It supports object tracking and detection on video frames and provides sample input data for testing.

---

## Project Structure

```
├── Train_yolo11.ipynb         # Notebook for training the YOLOv5 model
├── custom_counter.py          # Custom counting logic implementation
├── video_recording.py         # Script to process input videos
├── customized_tracker.yaml    # Custom tracking parameters for detections
├── Models/
│   ├── v14_yolo11n.pt         # Trained YOLO11 model with NIR dataset
│   ├── color_n.pt             # Trained YOLO11 model with RGB dataset
├── Input videos/
│   ├── color.mp4              # RGB input video
│   └── nir.mp4                # NIR input video
├── requirements.txt           # Python dependencies
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/EnricoMendez/NIR-capsicum-counting.git
cd NIR-capsicum-counting
```

### 2. Create and activate a virtual environment
```bash
conda create -n fruit-env python=3.11.11
conda activate fruit-env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Note: If using GPU acceleration, make sure PyTorch is installed with CUDA support.

Install cuda from download page:  [CUDA Toolkit 11.7 Downloads](https://developer.nvidia.com/cuda-11-7-0-download-archive).

Or install other version from here: [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive).

Then install a torch version compatible with the installed cuda from the installation page: [torch installation page](https://pytorch.org).


---

## Usage

### Run detection and counting
```bash
python custom_counter.py
```

This script processes the input videos and runs object detection using the pre-trained YOLOv5 model. It tracks and counts detected objects (e.g., fruits).

### Train a new model
Use the provided notebook:
```bash
jupyter notebook Train_yolo11.ipynb
```

---

## Sample Data

The ' Input videos/' folder includes example videos (`color.mp4`, `nir.mp4`) to test the pipeline with different spectrum inputs. Additional videos collected can be found in this [link](https://tecmx.sharepoint.com/:f:/r/sites/AiRLabArtificialIntelligenceandRoboticsLaboratory-MaestraEnrico/Shared%20Documents/2025%20Maestr%C3%ADa%20Enrico/NIR%20counting%20capsicums?csf=1&web=1&e=3egYrJ).

---

## Models

The model used is a YOLO11 (nano variant) trained on a custom fruit dataset. The weights file `v14_yolo11n.pt` is a YOLO11 nano model trained with NIR capsicum images, and `color_n.pt` is a YOLO11 nano model trained with RGB images.

---

## Author

Developed by **Enrico Mendez**, Mechatronics Engineer, as part of his MSc thesis at Tecnológico de Monterrey. 


