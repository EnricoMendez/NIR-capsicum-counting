# Author: Enrico Mendez
# Date: 04 Abril 2025
# Description: This script counts the number of objects in a video 
#              using a custom object counter class from Ultralytics
#              library.

# Import necessary libraries
import cv2
from ultralytics import solutions

# CustomCounter class that inherits from solutions.ObjectCounter
class CustomCounter(solutions.ObjectCounter):
    def extract_tracks(self, im0):
        
        """
        Applies object tracking and extracts tracks from an input image or frame.

        Args:
            im0 (ndarray): The input image or frame.

        Examples:
            >>> solution = BaseSolution()
            >>> frame = cv2.imread("path/to/image.jpg")
            >>> solution.extract_tracks(frame)
        """
        self.tracks = self.model.track(source=im0, persist=True, classes=self.CFG["classes"],tracker = 'tracker.yaml',device = 'mps')

        # Extract tracks for OBB or object detection
        self.track_data = self.tracks[0].obb or self.tracks[0].boxes


        if self.track_data and self.track_data.id is not None:
            self.boxes = self.track_data.xyxy.cpu()
            self.clss = self.track_data.cls.cpu().tolist()
            self.track_ids = self.track_data.id.int().cpu().tolist()
        else:
            # LOGGER.warning("WARNING ⚠️ no tracks found!")
            self.boxes, self.clss, self.track_ids = [], [], []

### Setup constants
model_path = r"Models/v18n.pt"                      # Path to the YOLO model
input_video_path = r"Input videos/nir.mp4"          # Path to the input video
output_video_path = r"Output videos/nir_count.mp4"  # Path to the output video

"""Count specific classes of objects in a video."""
cap = cv2.VideoCapture(input_video_path)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

limit1 = int(w/3)
limit2 = int(3*w/4)
line_points = [(limit1, 0), (limit1, h)]
box_points = [(limit1,0),(limit1,h),(limit2, h),(limit2,0)]
full_points = [(0,0),(w,0),(w,h),(0,h)]
counter = CustomCounter(show=False, region=box_points, model=model_path)
# If you want to use line counting, use the following line instead:
# counter = CustomCounter(show=False, region=line_points, model=model_path)
# If you want to use full counting, use the following line instead:
# counter = CustomCounter(show=False, region=full_points, model=model_path)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = counter.count(im0)
    video_writer.write(im0)
cap.release()
video_writer.release()
cv2.destroyAllWindows()

print(f"Inward count: {counter.in_count}, Outward count: {counter.out_count}")
