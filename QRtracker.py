from cmath import rect
import queue
from threading import Thread
from cv2 import FILLED, imshow
from matplotlib.patches import Polygon
from pyparsing import col
from reader import Vidstream
from pyzbar.pyzbar import decode
import numpy as np
import cv2 as cv
from colors import GREEN, RED, YELLOW
import time

track_show = queue.Queue()

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


class QRtracker(Vidstream):
    def __init__(self, source=0):
        super().__init__(source)
        self.tracking = {}
        self.timeout = {}
        self.update_q = queue.Queue()

    def track(self):
    
        while True:
            try:
                current = self.feed.get()
        
                for code in decode(current):
                    dstring = code.data.decode('utf-8')
                    if dstring not in self.tracking:
                        self.tracking[dstring] = code
                        self.timeout[dstring] = 0
                        print(f'added {dstring} to self.tracking')
                        # print(type(self.tracking[dstring]))

                    if dstring in self.tracking:
                        self.timeout[dstring] = 0
                        # print(f'{dstring} refreshed')

                for key in self.timeout:
                    if self.timeout[key] > 10:
                        if key in self.tracking:
                            print(f'{key} not found for 10 frames, removing')
                            del self.tracking[key]
                            self.timeout[key] = 0

                self.timeout.update([(key,value+1) for key,value in self.timeout.items()])
                self.update_q.put((current,self.tracking))

                # key = cv.waitKey(1)
                # if key == ord('q'):
                #     self.capture.release()
                #     cv.destroyAllWindows()
                #     exit()


            except AttributeError:
                pass

    def update_frame(self):
        while True:
            try:
                frame, codes = self.update_q.get(block=True, timeout=2)
                for decoded in codes:
                    (x,y,w,h) = self.tracking[decoded].rect
                    pt1, pt2 = (x,y), (x+w, y+h)
                    frame = cv.rectangle(frame,pt1, pt2, color=GREEN, thickness= 4)
                print('processing done')
                frame = ResizeWithAspectRatio(frame, height=800)
                cv.imshow('marked', frame)
                cv.waitKey(1)
                key = cv.waitKey(1)
                if key == ord('q'):
                            self.capture.release()
                            cv.destroyAllWindows()
                            exit()
            except queue.Empty:
                print('Ran out of frames, exiting')
                self.capture.release()
                cv.destroyAllWindows()
                exit()

if __name__ == '__main__':
    src='qrtest.MOV'
    thing = QRtracker(source=src)
    Thread(target=thing.track,daemon=True).start()
    while True:
        t = [Thread(target=thing.update_frame) for _ in range(4)]
        for thread in t:
            thread.start()
        for thread in t:
            thread.join()
# while True:
    # print([thing.tracking[key].rect for key in thing.tracking])
