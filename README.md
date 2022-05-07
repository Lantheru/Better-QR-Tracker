## <ins>**Overview**<ins>
Opens video feed and reads for QR codes, then ports decoded data and reference points for visualization in updated frames

#### <ins>**Note**<ins> 
Incomplete code, ongoing project for learning aspects of computer visualization and asynchronous execution for viability with live video feed 

___

### <ins>**Implemented**<ins>
- Dedicated video stream scans and enqueues every read frame for detection of QR codes and relevant data



### <ins>**To Do**<ins>

- QR detection and storage of relevant data.
- Logic to track constant list of tracked QR codes, their data, and append relevant metadata for parsing in other programs
- When codes have not been read from a frame for a fixed period of time, data for tracked QRs are dropped 
- Return view of video updated with visual indicators of codes being tracked

