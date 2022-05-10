import queue
from threading import Thread
from cv2 import imshow
from reader import Vidstream
from pyzbar.pyzbar import decode
import numpy as np
import cv2 as cv
from colors import GREEN, RED, YELLOW



def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)


update_q = queue.PriorityQueue()
processed = queue.PriorityQueue()


def track():

    while True:
        tracking = {}
        try:
            (count,original, grayframe) = vid.feed.get(block=True, timeout = 2)

            for code in decode(grayframe):
                dstring = code.data.decode('utf-8')
                (x,y,w,h) = code.rect
                bbox = ((x,y), (x+w, y+h))
                if dstring not in tracking:
                    tracking[dstring] = (code.data,bbox)
                    print(f'added {dstring} to .tracking')


            
            print(tracking)
            update_q.put((count, original, tracking))



        except queue.Empty:
            print('Ran out of frames, exiting')
            return




def process_frame():
    while True:
        try:
            (count, original, tracking) = (update_q.get(timeout=2))
            for decoded in tracking:
                print(tracking[decoded])
                (pt1, pt2) = tracking[decoded][1]
                original = cv.rectangle(original,pt1, pt2, color=GREEN, thickness= 4)

            frame = ResizeWithAspectRatio(original, height=800)

            processed.put((count,frame))
            key = cv.waitKey(1)
            if key == ord('q'):
                        vid.capture.release()
                        cv.destroyAllWindows()
                        exit()
        except queue.Empty:
            print('Ran out of frames, exiting')
            return


if __name__ == '__main__':
    src='qrtest.MOV'
    vid = Vidstream(src)
    
    [Thread(target=track).start() for _ in range(4)]
    [Thread(target=process_frame).start() for _ in range(4)]



    
    while True:
        try:
            (count, frame) = processed.get(timeout=2)
            imshow('processed', frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                vid.capture.release()
                cv.destroyAllWindows()
                exit()
        except queue.Empty:
            print('Main out of frames, exiting')
            vid.capture.release()
            cv.destroyAllWindows()
            exit()
            

