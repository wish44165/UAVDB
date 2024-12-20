import os
import re
import cv2
import copy
import time
import numpy as np
import matplotlib.pyplot as plt

# parameters
ALPHA = 8    # initial size
DELTA = 5    # extend unit
THRES = 4    # threshold
interval = 10    # extract one frame every #interval frame


videoPath = './data/videos/'
videoList = os.listdir(videoPath)
videoList = sorted(videoList)

txtPath = './data/detections/'

datasetPath = './datasets/'
train_dstPath = './datasets/train/'
val_dstPath = './datasets/val/'
test_dstPath = './datasets/test/'
os.makedirs(datasetPath, exist_ok=True)
os.makedirs(train_dstPath, exist_ok=True)
os.makedirs(val_dstPath, exist_ok=True)
os.makedirs(test_dstPath, exist_ok=True)

trainVideos = ['d1c0.mp4', 'd1c2.mp4', 'd2c1.mp4', 'd2c2.mp4', 'd3c0.mp4', 'd3c1.mp4', 'd3c3.mp4', 'd3c5.mp4', 'd4c1.mp4', 'd4c2.mp4', 'd4c3.mp4', 'd4c5.mp4']
valVideos = ['d1c1.mp4', 'd2c3.mp4', 'd3c2.mp4', 'd4c4.mp4']
testVideos = ['d1c3.mp4', 'd2c0.mp4', 'd3c4.mp4', 'd4c0.mp4', 'd4c6.mp4']

print('train videos:', trainVideos)
print('valid videos:', valVideos)
print('test videos:', testVideos)

for vn in videoList:

    if vn in set(trainVideos):
        print('==== ' + vn + ' in train ====')
        dstPath = train_dstPath
        PICFlag = 1

    elif vn in set(valVideos):
        print('==== ' + vn + ' in val ====')
        dstPath = val_dstPath
        PICFlag = 1

    elif vn in set(testVideos):
        print('==== ' + vn + ' in test ====')
        dstPath = test_dstPath
        PICFlag = 1
    
    else:
        print('==== ' + vn + ' X ====')
        PICFlag = 0


    if PICFlag == 1:

        vp = videoPath + vn
        cap = cv2.VideoCapture(vp)
        H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        tp = txtPath + vn[:-3] + 'txt'

        frame_count = 0

        # read txt
        with open(tp, encoding='utf8') as f:
            for line in f:
                l = re.findall("\d+\.\d+", line)
                ll = [float(li) for li in l]

                if len(ll) == 3:
                    ct, x, y = ll
                    ct, x, y = int(ct), int(x), int(y)

                    ret, frame = cap.read()
                    image = copy.deepcopy(frame)    # frame.shape = (h, w, c)

                    if ct % interval == 1:

                        if x + y != 0:
                            L = []
                            D = []
                            for i in range(40):

                                leftUp, rightDown = [x-(ALPHA+DELTA*i)//2, y-(ALPHA+DELTA*i)//2], [x+(ALPHA+DELTA*i)//2, y+(ALPHA+DELTA*i)//2]

                                if W > 1920:
                                    leftUp, rightDown = [x-(ALPHA*2+DELTA*2*i)//2, y-(ALPHA*2+DELTA*2*i)//2], [x+(ALPHA*2+DELTA*2*i)//2, y+(ALPHA*2+DELTA*2*i)//2]

                                ## avoid on the edge or outside
                                if leftUp[0] < 1:
                                    leftUp[0] = 1
                                if leftUp[1] < 1:
                                    leftUp[1] = 1
                                if leftUp[0] > W:
                                    leftU[0] = W
                                if leftUp[1] > H:
                                    leftUp[1] = H

                                if rightDown[0] < 1:
                                    rightDown[0] = 1
                                if rightDown[1] < 1:
                                    rightDown[1] = 1
                                if rightDown[0] > W:
                                    rightDown[0] = W
                                if rightDown[1] > H:
                                    rightDown[1] = H

                                imageCrop = image[leftUp[1]:rightDown[1], leftUp[0]:rightDown[0]]
                                imageCrop = cv2.cvtColor(imageCrop, cv2.COLOR_BGR2GRAY)
                                L.append(np.average(imageCrop))
                                if i > 1:
                                    D = L[-1] - L[-2]
                                    if D < THRES:
                                        bboxW, bboxH = rightDown[0] - leftUp[0], rightDown[1] - leftUp[1]
                                        break
                            
                            # save image
                            cv2.imwrite(dstPath + vn[:-4] + '_' + str(frame_count) + '.jpg', frame)

                            # write txt
                            with open(dstPath + vn[:-4] + '_' + str(frame_count) + '.txt', 'w') as wf:
                                wf.write('0 ' + str(x / W) + ' ' + str(y / H) + ' ' + str(bboxW / W) + ' ' + str(bboxH / H) + '\n')

                            frame_count += 1
            

        # release
        cap.release()
        cv2.destroyAllWindows()