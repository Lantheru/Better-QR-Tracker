## <ins>**Overview**<ins>
Opens video feed and reads for QR codes, then ports decoded data and reference points for visualization in updated frames

#### <ins>**Note**<ins> 
Incomplete code, ongoing project for learning aspects of computer visualization and asynchronous execution for viability with live video feed 

___

### <ins>**Implemented**<ins>
- Dedicated video stream scans and enqueues every read frame for detection of QR codes and relevant data
- QR codes are read from each frame and decoded, updating a dictionary to store their data. When a code isn't read for a number of frames (note to implement actual timeout period later), it is deleted from the tracked QR codes.
- Independent threads update each frame with tracking rectangles to visually indicate codes that are being followed and displaying them.



### <ins>**To Do**<ins>
- Separate threads still need to by synced, likely attaching priorities to the frames so they are read in proper sequence. Drawing lines over each frame, per code, takes a considerable amount of time and needs to be optimized.
