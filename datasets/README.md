## UAVDB

Overview of [UAVDB](https://zenodo.org/records/14534940) constructed using the PIC approach, showing the distribution of 10,763 training, 2,720 validation, and 4,578 test images (18,061 total) across datasets and camera configurations.

```
datasets/
├── train/d1c0_0.jpg, d1c0_0.txt, ...
├── val/d1c1_0.jpg, d1c1_0.txt, ...
└── test/d1c3_0.jpg, d1c3_0.txt, ...
```

| Camera $$\backslash$$ Dataset | 1           | 2           | 3            | 4            |
| ----------------------------- | ----------- | ----------- | ------------ | ------------ |
| 0                             | train / 291 | test  / 237 | train / 3190 | train / 2355 |
| 1                             | valid / 303 | train / 343 | train / 841  | test  / 416  |
| 2                             | train / 394 | train / 809 | valid / 1067 | train / 701  |
| 3                             | test  / 348 | valid / 426 | train / 638  | train / 727  |
| 4                             | --          | --          | test  / 1253 | valid / 924  |
| 5                             | --          | --          | train / 1303 | train / 1110 |
| 6                             | --          | --          | --           | test  / 385  |