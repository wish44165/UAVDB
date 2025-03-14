# UAVDB: Trajectory-Guided Adaptable Bounding Boxes for UAV Detection


This repository introduces the Patch Intensity Convergence (PIC) technique, a trajectory-guided method for generating high-fidelity UAV detection bounding boxes without manual labeling. It also serves as the foundation for [UAVDB](https://zenodo.org/records/14534940), a dedicated database for UAV detection. More details are presented in the [paper](https://arxiv.org/abs/2409.06490).


<img src="https://github.com/wish44165/UAVDB/blob/main/assets/overview.png" alt="overview" width="97%">


## 1. Environment Setup


<details><summary>Hardware Information</summary>

### Laptop

- CPU: Intel® Core™ i7-12650H
- GPU: NVIDIA GeForce RTX 4050 Laptop GPU (6GB)
- RAM: 23734MiB

### HPC

- GPU: Spartan gpu-a100 (80GB)
  
</details>


<details><summary>Folder Structure</summary>

```
UAVDB/
├── assets/
├── logfile/
├── src/PIC.py
├── data/
│   ├── videos/d1c0.txt, d1c1.txt, ...
│   └── detections/d1c0.mp4, d1c1.mp4, ...
├── datasets/
│   ├── train/d1c0_0.jpg, d1c0_0.txt, ...
│   ├── val/d1c1_0.jpg, d1c1_0.txt, ...
│   └── test/d1c3_0.jpg, d1c3_0.txt, ...
└── weights/
    ├── yolov8n.pt
    ├── yolov8s.pt
    ├── yolov9t.pt
    ├── yolov9s.pt
    ├── yolo10n.pt
    ├── yolo10s.pt
    ├── yolo11n.pt
    ├── yolo11s.pt
    ├── yolov12n.pt
    └── yolov12s.pt
```

</details>


<details><summary>Conda Environments</summary>

```bash
# PIC
$ conda create -n pic python=3.10 -y
$ conda activate pic
$ conda install -c conda-forge cupy
$ pip install scipy opencv-python opencv-contrib-python matplotlib numba


# YOLOv8 & YOLO11
$ conda create -n ultralytics python=3.10 -y
$ conda activate ultralytics
$ pip install ultralytics seaborn
$ git clone https://github.com/ultralytics/ultralytics.git
$ cd ultralytics/

# download pretrained weights
$ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
$ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt
$ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt
$ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11l.pt
$ wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt


# YOLOv9
$ conda create -n yolov9 python=3.10 -y
$ conda activate yolov9
$ git clone https://github.com/WongKinYiu/yolov9.git
$ cd yolov9/
$ pip install -r requirements.txt
$ pip install Pillow==9.5.0

# download pretrained weights
$ wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-t-converted.pt
$ wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-s-converted.pt
$ wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-m-converted.pt
$ wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c-converted.pt
$ wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e-converted.pt


# YOLOv10
# setup
$ conda create -n yolov10 python=3.10 -y
$ conda activate yolov10
$ git clone https://github.com/THU-MIG/yolov10.git
$ cd yolov10/
$ pip install -r requirements.txt
$ pip install -e .

# download pretrained weights
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10n.pt
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10s.pt
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10m.pt
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10b.pt
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10l.pt
$ wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10x.pt


# YOLOv12
# setup
$ conda create -n yolov12 python=3.11 -y
$ conda activate yolov12
$ git clone https://github.com/sunsmarterjie/yolov12.git
$ cd yolov12/
$ wget https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.3/flash_attn-2.7.3+cu11torch2.2cxx11abiFALSE-cp311-cp311-linux_x86_64.whl
$ pip install -r requirements.txt
$ pip install -e .

# download pretrained weights
$ wget https://github.com/sunsmarterjie/yolov12/releases/download/v1.0/yolov12n.pt
$ wget https://github.com/sunsmarterjie/yolov12/releases/download/v1.0/yolov12s.pt
$ wget https://github.com/sunsmarterjie/yolov12/releases/download/v1.0/yolov12m.pt
$ wget https://github.com/sunsmarterjie/yolov12/releases/download/v1.0/yolov12l.pt
$ wget https://github.com/sunsmarterjie/yolov12/releases/download/v1.0/yolov12x.pt
```

</details>




## 2. Dataset Description


<details><summary>Multi-view drone tracking datasets</summary>

Summary of dataset characteristics in [Multi-view drone tracking datasets](https://github.com/CenekAlbl/drone-tracking-datasets). The table displays the number of frames and resolution for each camera across different datasets. Each cell lists the number of frames followed by the resolution in pixels.

| Camera $$\backslash$$ Dataset | 1                  | 2                  | 3                   | 4                   | 5                   | 
| ----------------------------- | ------------------ | ------------------ | ------------------- | ------------------- | ------------------- |
| 0                             | 5334 / 1920×1080   | 4377 / 1920×1080   | 33875 / 1920×1080   | 31075 / 1920×1080   | 20970 / 1920×1080   |
| 1                             | 4941 / 1920×1080   | 4749 / 1920×1080   | 19960 / 1920×1080   | 15409 / 1920×1080   | 28047 / 1920×1080   |
| 2                             | 8016 / 1920×1080   | 8688 / 1920×1080   | 17166 / 3840×2160   | 15678 / 1920×1080   | 31860 / 2704×2028   |
| 3                             | 4080 / 1920×1080   | 4332 / 1920×1080   | 14196 / 1440×1080   | 10933 / 3840×2160   | 31992 / 1920×1080   |
| 4                             | --                 | --                 | 18900 / 1920×1080   | 17640 / 1920×1080   | 21523 / 2288×1080   |
| 5                             | --                 | --                 | 28080 / 1920×1080   | 32016 / 1920×1080   | 17550 / 1920×1080   |
| 6                             | --                 | --                 | --                  | 11292 / 1440×1080   | --                  |
  
</details>


<details><summary>UAVDB</summary>

Overview of UAVDB constructed using the PIC approach, showing the distribution of 10,763 training, 2,720 validation, and 4,578 test images (18,061 total) across datasets and camera configurations.

| Camera $$\backslash$$ Dataset | 1           | 2           | 3            | 4            |
| ----------------------------- | ----------- | ----------- | ------------ | ------------ |
| 0                             | train / 291 | test  / 237 | train / 3190 | train / 2355 |
| 1                             | valid / 303 | train / 343 | train / 841  | test  / 416  |
| 2                             | train / 394 | train / 809 | valid / 1067 | train / 701  |
| 3                             | test  / 348 | valid / 426 | train / 638  | train / 727  |
| 4                             | --          | --          | test  / 1253 | valid / 924  |
| 5                             | --          | --          | train / 1303 | train / 1110 |
| 6                             | --          | --          | --           | test  / 385  |

</details>




## 3. Demonstration


<details><summary>Patch Intensity Convergence (PIC)</summary>

<img src="https://github.com/wish44165/UAVDB/blob/main/assets/PIC.png" alt="PIC" width="97%">

</details>


<details><summary>Validation Performance</summary>

<img src="https://github.com/wish44165/UAVDB/blob/main/assets/valid_performance.jpg" alt="Valid" width="97%">

</details>


<details><summary>Inference Results</summary>

<img src="https://github.com/wish44165/UAVDB/blob/main/assets/inference.png" alt="Inference" width="97%">

</details>




## 4. UAVDB Benchmark Results


| Model                                                                           | image size | batch size | $$AP^{val}_{50}$$ | $$AP^{val}_{50-95}$$ | $$AP^{test}_{50}$$ | $$AP^{test}_{50-95}$$ |
| ------------------------------------------------------------------------------- | ---------- | ---------- | ----------------- | -------------------- | ------------------ | --------------------- |
| [yolov8n.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov8n.pt)   | 640        | 32         | 0.829             | 0.522                | 0.789              | 0.450                 |
| [yolov8s.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov8s.pt)   | 640        | 32         | 0.814             | 0.545                | 0.796              | 0.450                 |
| [yolov9t.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov9t.pt)   | 640        | 32         | 0.839             | 0.501                | 0.848              | 0.508                 |
| [yolov9s.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov9s.pt)   | 640        | 32         | 0.819             | 0.517                | 0.834              | 0.484                 |
| [yolo10n.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov10n.pt)  | 640        | 32         | 0.764             | 0.492                | 0.731              | 0.417                 |
| [yolo10s.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov10s.pt)  | 640        | 32         | 0.817             | 0.530                | 0.823              | 0.516                 |
| [yolo11n.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolo11n.pt)   | 640        | 32         | 0.847             | 0.527                | 0.856              | 0.539                 |
| [yolo11s.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolo11s.pt)   | 640        | 32         | 0.826             | 0.553                | 0.885              | 0.578                 |
| [yolov12n.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov12n.pt) | 640        | 32         | 0.857             | 0.544                | 0.848              | 0.531                 |
| [yolov12s.pt](https://github.com/wish44165/UAVDB/blob/main/weights/yolov12s.pt) | 640        | 32         | 0.869             | 0.566                | 0.882              | 0.565                 |




## Citation

If you find this project helpful for your research or applications, we would appreciate it if you could give it a star and cite the paper.

```
@article{chen2024uavdb,
  title={UAVDB: Trajectory-Guided Adaptable Bounding Boxes for UAV Detection},
  author={Chen, Yu-Hsi},
  journal={arXiv preprint arXiv:2409.06490},
  year={2024}
}
```




## Acknowledgment

The data and evaluation codes based on the [Multi-view Drone Tracking Datasets](https://github.com/CenekAlbl/drone-tracking-datasets), [YOLOv8, YOLO11](https://github.com/ultralytics/ultralytics), [YOLOv9](https://github.com/WongKinYiu/yolov9), [YOLO10](https://github.com/THU-MIG/yolov10), and [YOLOv12](https://github.com/sunsmarterjie/yolov12) and greatly appreciate their excellent works.