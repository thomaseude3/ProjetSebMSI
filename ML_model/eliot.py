import numpy
from ultralytics import YOLO

# load a pretrained YOLOv8n model
model = YOLO('best.pt', "v8")

# predict on an image
detection_output = model.predict(source="2023-11-14_14-36-03.png", conf=0.25, save=True)

# Display tensor array
print(detection_output)

# Display numpy array
print(detection_output[0].numpy())