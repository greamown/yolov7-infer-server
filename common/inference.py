from pathlib import Path
import cv2, logging, time, torch, sys, os
# import torch.backends.cudnn as cudnn
from numpy import random
sys.path.append(str(Path(__file__).resolve().parents[1]/"yolov7"))
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

class Yolov7:
    def __init__(self, weights, img_size=640, device="", trace=True):
        # Initialize
        self.imgsz = img_size
        self.img_size = img_size
        self.device = select_device(device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz  = check_img_size(self.imgsz , s=self.stride)  # check img_size

        # if trace:
        #     self.model = TracedModel(self.model, self.device, self.img_size)

        if self.half:
            self.model.half()  # to FP16

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

    def infer(self, source, url, augment=False, classes=None, agnostic=False, conf_thres=0.25, iou_thres=0.45):
        from common import SAVE_PATH
        self.conf_thres = conf_thres
        self.iou_thres  = iou_thres
        dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride)
        self.detections = {}
        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
        old_img_w = old_img_h = self.imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if self.device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=augment)[0]

            # Inference
            self.t1 = time_synchronized()
            with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
                pred = self.model(img, augment=augment)[0]
            self.t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=classes, agnostic=agnostic)
            self.t3 = time_synchronized()

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                self.save_result(path, im0s, SAVE_PATH, det, img, url)
                
        logging.info(f'Done. ({time.time() - t0:.3f}s)')

    def save_result(self, path, im0s, save_dir, det, img, url):
        p, s, im0 = path, '', im0s

        p_name = os.path.split(p)[-1]  # to Path
        save_path = os.path.join(save_dir,p_name)  # img.jpg
        
        self.detections.update({p_name:{"detections":[], "url":"{}/show_result/{}".format(url, p_name)}})
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {self.names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                # Append to detections
                result = {"x":int(xyxy[0]), "y":int(xyxy[1]), "x1":int(xyxy[2]-xyxy[0]), "y2":int(xyxy[3]-xyxy[1]), 
                                                        "confidence": float(conf), "class":int(cls), "name":self.names[int(cls)]}
                logging.info(str(result))
                self.detections[p_name]['detections'].append(result)
                # Add bbox to image
                label = f'{self.names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)], line_thickness=3)

        # Print time (inference + NMS)
        logging.info(f'{s} confidence:{det[:, 4]}, Done. ({(1E3 * (self.t2 - self.t1)):.1f}ms) Inference, ({(1E3 * (self.t3 - self.t2)):.1f}ms) NMS')
        cv2.imwrite(save_path, im0)
        logging.warn(f" The image with the result is saved in: {save_path}")
    
