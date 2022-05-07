from threading import Thread
import cv2 as cv
from numpy import mat
from pyzbar.pyzbar import decode,ZBarSymbol
import time
import queue
import asyncio

#Runs dedicated thread for reading 

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
                current = vid.feed.get(block=True, timeout=2)
                cv.imshow('feed', current)
                key = cv.waitKey(1)
                if key == ord('q'):
                    vid.capture.release()
                    cv.destroyAllWindows()
                    exit()
                if key == ord('p'):
                    cv.waitKey(0)
                    continue
                # else:
                #     cv.destroyAllWindows()
                #     exit()
                time.sleep(.01)
            except queue.Empty:
                print('Ran out of frames')
                vid.capture.release()
                cv.destroyAllWindows()
                exit()

if __name__ == '__main__':
    vid = Vidstream('qrtest.MOV')
    vid.test()
    

#     async def show_gray(self):
#         cv.imshow('gray', self.gray_buffer.get())
#         key = cv.waitKey(1)
#         if key == ord('q'):
#             self.capture.release()
#             cv.destroyAllWindows()
#             exit()

#     async def feed_gray(self):
#         yield self.gray_frame

# if __name__ == '__main__':
#     video_stream = Vidstream(source = 'qrtest.MOV' )
#     print(type(video_stream.get_raw()))
#     # while True:
#     #     try:
#     #         frame = cv.cvtColor(video_stream.get_raw(), cv.COLOR_BGR2GRAY)
#     #         cv.imshow('frame', frame)
#     #         cv.imshow('raw', video_stream.get_raw())
#     #         # video_stream.show_raw()
#     #         # video_stream.show_gray()
#     #         key = cv.waitKey(1)
#     #         if key == ord('q'):
#     #             video_stream.capture.release()
#     #             cv.destroyAllWindows()
#     #             exit()
#     #     except AttributeError:
#     #         pass