from threading import Thread
import cv2 as cv
import time
import queue


#Runs dedicated thread for reading from capture and enqueues for further processing.

class Vidstream:
    feed = queue.Queue()
    def __init__(self, source=0):
        self.framecount = 0
        self.capture = cv.VideoCapture(source)
        self.reader = Thread(target=self._update, args=(), daemon=True)
        self.reader.start()
       

    def _update(self):
        while True:
            (self.status, self.frame) = self.capture.read()
            if self.status == True:
                self.feed.put(self.frame)
                self.framecount += 1
                time.sleep(.01)
            else:
                print("Done reading video")
                break
                 


    def test(self):
        while True:
            try:
                current = self.feed.get(block=True, timeout=2)
                cv.imshow('feed', current)
                key = cv.waitKey(1)
                if key == ord('q'):
                    vid.capture.release()
                    cv.destroyAllWindows()
                    exit()
                if key == ord('p'):
                    cv.waitKey(0)
                    continue
                time.sleep(.01)
                
            except queue.Empty:
                print('Ran out of frames, exiting')
                vid.capture.release()
                cv.destroyAllWindows()
                exit()

if __name__ == '__main__':
    vid = Vidstream('qrtest.MOV')
    vid.test()
    
