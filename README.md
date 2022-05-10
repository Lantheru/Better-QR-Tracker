## <ins>**Overview**<ins>
Opens video feed and reads for QR codes, then ports decoded data and reference points for visualization in updated frames. Source defaults to first found system camera, but can be anything readable by opencv's VideoCapture class including video streaming over a network.

___

### <ins>**Implemented**<ins>
- Dedicated video stream scans and enqueues every read frame for detection of QR codes and relevant data
- QR codes are read from each frame and decoded, forwarding a tuple for processing in another thread.
- Independent threads update each frame with tracking rectangles to visually indicate codes that are being followed and displaying them.
- Frames with processed bounding boxes are paired with their frame number and placed in a priority queue for reading by the main program
