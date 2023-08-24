from ultralytics import YOLO

model = YOLO("yolov8x.pt")
model.train(data="data.yaml", epochs=30)