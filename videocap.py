#import os.path
import cv2
import datetime
def videorec():
    cap=cv2.VideoCapture(0) #open webcam,use 0 for laptop
    rec=cv2.VideoWriter_fourcc(*'XVID')
    vidname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    a=vidname+".avi"
    out=cv2.VideoWriter(a,rec,20.0,(640,480))#20.0 is frame rate  #640,480 are window dimensions
    print(cap.isOpened())
    while cap.isOpened():
        ret,frame=cap.read()  #the method returns two values
        out.write(frame)
        cv2.imshow("VideoCapture",frame)
        if cv2.waitKey(1) & 0xFF==ord('q'): #press q to exit
            break
    cap.release()
    cv2.destroyAllWindows()
    return a
x=videorec()
print(x)

