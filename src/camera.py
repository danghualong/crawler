import cv2
import time

camera=cv2.VideoCapture(0)
fW=camera.get(cv2.CAP_PROP_FRAME_WIDTH)
fH=camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,240)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,160)
fH2=camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
while(camera.isOpened()):
    ret,frame=camera.read()
    cv2.imshow("cap",frame)
    k=cv2.waitKey(1)
    if(k==ord('q')):
        break
    elif(k==ord('s')):
        uid=int(time.time())
        cv2.imwrite('D:/images/{0}.jpg'.format(uid),frame)
camera.release()
cv2.destroyAllWindows()