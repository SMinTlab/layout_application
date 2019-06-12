# -*- coding: utf-8 -*-
import tobii_research as tr
import sys
import time
import numpy as np
import cv2
import subprocess
import re
import datetime
import schedule

class EyeTracking:
    wh=(1440,878)
    img=np.zeros((wh[1],wh[0],3), dtype=np.uint8)
    prev_xy=(0,0)
    save_img_path=''
    save_gaze_path=''
    freq=1/60
    color=(255,255,255)
    eyetracker=None
    millsec = [0,0]

    def __init__(self,wh,save_img_path,save_gaze_path):
        if wh[0]>1440:
            self.wh=(wh[0]-1440,wh[1])
        else:
            self.wh=wh
        self.save_img_path=save_img_path
        self.save_gaze_path=save_gaze_path
        self.img=np.zeros((self.wh[1],self.wh[0],3), dtype=np.uint8)
        eyetrackers = tr.find_all_eyetrackers()
        if len(eyetrackers) >= 1 :
            self.eyetracker = eyetrackers[0]
        else:
            print("Error: Not Found EyeTracker")
            #sys.exit()
        print("Address: " + self.eyetracker.address)
        print("Model: " + self.eyetracker.model)
        print("Name (It's OK if this is empty): " + self.eyetracker.device_name)
        print("Serial number: " + self.eyetracker.serial_number)
        self.freq=self.eyetracker.get_gaze_output_frequency()
        print("Freqency:"+str(int(self.freq)))

    def gaze_data_callback(self,gaze_data):
        time_stamp = gaze_data.device_time_stamp
        left_point = gaze_data.left_eye.gaze_point.position_on_display_area
        right_point = gaze_data.right_eye.gaze_point.position_on_display_area
        now_xy=tuple([int(((left_point[i] + right_point[i]) / 2) * self.wh[i]) for i in range(2)])
        self.img = cv2.line(self.img, self.prev_xy,now_xy,self.color)
        self.prev_xy=now_xy
        now=datetime.datetime.now()
        with open(self.save_gaze_path+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second),mode='w') as f:
            f.write(str(time_stamp)+'\n'+str(left_point)+'\n'+str(right_point)+'\n')



    def exec_calibration(self):
        calibration=tr.ScreenBasedCalibration(self.eyetracker)
        calibration.enter_validation_mode()
        points=[(0.5,0.5),(0.1,0.1),(0.1,0.9),(0.9,0.1),(0.9,0.9)]

        for point in points:
            print("Show a point on screen at {0}.".format(point))
            time.sleep(0.7)
            if calibration.compute_and_apply().status!=tr.CALIBRATION_STATUS_SUCCESS:
                calibration.collect_data(point[0],point[1])
        print("Apply calibration.")
        result=calibration.compute()
        print("result:{}".format(result.status))
        calibration.leave_validation_mode()
        print("Completed calibration.")


    def start(self):
        if self.eyetracker is None:
            print('No EyeTracker found.')
        else:
            cv2.namedWindow("MyEyeTrack", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("MyEyeTrack",self.img)
            self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=False)
            i=0
            while(True):
                key=cv2.waitKey(int(1.0/self.freq*1000))
                cv2.imshow("MyEyeTrack",self.img)
                if i%self.freq==0:
                    if cv2.imwrite(self.save_img_path+'img'+str(int(i/self.freq))+'.jpg',self.img) is not True:
                        print('OpenCV::imwrite() failed to save image at '+self.save_img_path)
                    else:
                        print(datetime.datetime.today())
                i+=1
                if key==27:
                    self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
                    cv2.destroyAllWindows()
                    sys.exit()
    def job(self):
        now = datetime.datetime.now()
        self.millsec[1] = self.millsec[0]
        split = str(now).split(".")
        self.millsec[0] = split[0].split(":")[-1]+"."+split[1]
        diff = float(self.millsec[0])-float(self.millsec[1])
        if diff < 0:
            diff = float("60." + split[1])-float(self.millsec[1])
        print(str(now)+" "+str(diff))

    def mainloop(self):
        if False and self.eyetracker is None:
            print('No EyeTracker found.')
        else:
            schedule.every(self.freq).seconds.do(self.job)
            while True:
                schedule.run_pending()
                time.sleep(0.001)


def main():
    cmd=['xrandr']
    cmd2=['grep','*']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
    p2=subprocess.Popen(cmd2,stdin=p.stdout,stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string,junk=p2.communicate()
    resolution=resolution_string.split()[0]
    wh=str(resolution).split('x')
    pat=r"\D"
    wh[0]=int(re.sub(pat,"",wh[0]))
    wh[1]=int(re.sub(pat,"",wh[1]))
    #EyeTracking(tuple(wh),'../pics/','../data/').mainloop()
    EyeTracking(tuple(wh),'pics/','data/').exec_calibration()


if __name__=="__main__":
    main()
