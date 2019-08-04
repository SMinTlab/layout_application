# -*- coding: utf-8 -*-
import time
import copy
from operator import mul
from operator import add
from functools import reduce
import sys
import numpy as np
import tobii_research as tr

MICROSEC = 0.000001

class MyGazeData:
    left = None
    right = None
    time = 0

    def __init__(self, gaze_data):
        self.left = gaze_data["left_gaze_point_on_display_area"]
        self.right = gaze_data["right_gaze_point_on_display_area"] 
        self.time = gaze_data["device_time_stamp"]

    def __str__(self):
        return '(left: ' + str(self.left) + ', right: ' + str(self.right) + ') at ' + self.time

    def __repr__(self):
        this = {"left_gaze_point_on_display_area" : str(self.left), "right_gaze_point_on_display_area" : str(self.right), "device_time_stamp" : self.time}
        return 'MyGazeData(' + str(this) + ')'

    def to_point(self):
        x = (self.left[0] + self.right[0]) / 2
        y = (self.left[1] + self.right[1]) / 2
        return (x, y)

class Test:
    tracks = []
    lines = []
    width, height = 0, 0
    eyetracker = None
    gaze_data = []
    epsilon = 0.01
    lap_times = []
    passed = 0
    errors = []
    navi = False
    gazing_point = None
    f_sacc_idxes = []
    b_sacc_idxes = []
    f_sacc_buf = []
    b_sacc_buf =[]

    def __init__(self, width, height, start):
        self.width = width
        self.height = height
        self.tracks.append(start)

    def add_track_relative(self, next_point):
        r = reduce(mul,next_point)
        if r < 0 or r > 1:
            raise Exception("Out of screen.")
        prev = self.tracks[-1]
        a = next_point[1] - prev[1]
        b = prev[0] - next_point[0]
        c = prev[1] * next_point[0] - prev[0] * next_point[1]
        print("a = {}, b = {}, c = {}".format(a,b,c))
        line = (a,b,c)
        self.lines.append(line)
        self.tracks.append(next_point)

    def add_track(self, next_point):
        next_ = (next_point[0]/self.width, next_point[1]/self.height)
        self.add_track_relative(next_)

    def gaze_data_callback(self,gaze_data):
        if gaze_data["left_gaze_point_validity"]+gaze_data["right_gaze_point_validity"] is 2: # gaze data vaildity check
            mgd = MyGazeData(gaze_data)
            self.gaze_data.append(mgd) # collect all of vaild gaze data here
            nearest = self.nearest_point_and_distance(mgd)
            if nearest[1] < self.epsilon:
                self.gazing_point = nearest[0] # set gazing point now
                idx = self.tracks.index(nearest[0])
                if self.passed < idx + 1:
                    print("Forwarding saccade {} to {}".format(self.tracks[self.passed],self.tracks[idx]))
                    if len(self.b_sacc_buf) != 0:
                        self.b_sacc_idxes.append(self.b_sacc_buf)
                        self.b_sacc_buf.clear()
                    self.f_sacc_buf.append(len(self.gaze_data)-1)
                elif self.passed == idx + 1:
                    print("Insight point {}".format(self.tracks[self.passed]))
                else:
                    print("Backward saccade {} to {}".format(self.tracks[self.passed],self.tracks[idx]))
                    if len(self.f_sacc_buf) != 0:
                        self.f_sacc_idxes.append(self.f_sacc_buf)
                        self.f_sacc_buf.clear()
                    self.b_sacc_idxes.append(len(self.gaze_data)-1)
                self.passed = idx + 1


    def acc_err(self, gaze_data):
        dists = [[],[]]
        for l in self.lines:
            dists[0].append(self.sq_dist_pl(gaze_data[0][0],gaze_data[0][1],l))
            dists[1].append(self.sq_dist_pl(gaze_data[1][0],gaze_data[1][1],l))
        min_idx = dists[0].index(min(dists[0]))
        self.error_buffer[self.passed-1][0] += dists[0][min_idx]
        self.error_buffer[self.passed-1][1] += dists[1][min_idx]

    def nearest_point_and_distance(self,mgd):
        min_dist = self.sq_dist_pp(self.tracks[0], mgd.to_point())
        np = self.tracks[0]
        for point in self.tracks:
           dist = self.sq_dist_pp(point, mgd.to_point())
           if dist < min_dist:
               min_dist = dist
               np = point
        return (np, min_dist)

    def gaze_to_ave(self,gaze_data):
        return ((gaze_data[0][0]+gaze_data[1][0])/2,(gaze_data[0][1]+gaze_data[1][1])/2)

    def sq_dist_pp(self, point1, point2):
        d = pow(point2[0]-point1[0],2)+pow(point2[1]-point1[1],2)
        return d

    def sq_dist_pl(self, x, y, line):
        return pow(line[0] * x + line[1] * y + line[2], 2) / (pow(line[0], 2) + pow(line[1], 2))

    def in_sight(self, point, gaze_data):
        if (abs(point[0] - gaze_data[0][0]) < self.epsilon and abs(point[1] - gaze_data[0][1]) < self.epsilon) or (abs(point[0] - gaze_data[1][0]) < self.epsilon and abs(point[1] - gaze_data[1][1]) < self.epsilon):
            return True
        return False

    def run(self):
        et = tr.find_all_eyetrackers()
        if len(et) > 0:
            self.eyetracker = et[0]
        else:
            raise Exception("None of the eyetracker was found.")
        print("running...")
        self.passed = 0
        for _ in self.tracks:
            self.gaze_data.append(0)
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
        while self.passed < len(self.tracks):
            time.sleep(1/60)
            if self.navi and self.passed < len(self.tracks):
                print("Checking {}.".format(self.tracks[self.passed]))
                self.navi = False

        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
        print("finished.")
        print("epsilon = {}".format(self.epsilon))
        if len(self.f_sacc_buf) != 0:
            self.f_sacc_idxes.append(self.f_sacc_buf)
        if len(self.b_sacc_buf) != 0:
            self.b_sacc_idxes.append(self.b_sacc_buf)
        print("Forward saccades = {}".format([self.gaze_data[x] for list_x in self.f_sacc_idxes for x in list_x]))
        for i in range(len(self.gaze_data)):
            if i > 0:
                self.lap_times.append((self.gaze_data[i][2] - self.gaze_data[i-1][2])*MICROSEC)
        print(self.lap_times)
        sum = 0
        for t in self.lap_times:
            sum += t
        print("sum = {}".format(sum))
        sum = [0,0]
        for e in self.errors:
            sum[0] += e[0]
            sum[1] += e[1]
        print(self.errors)
        print("sum = {}".format(sum))
        print("output all gaze data.")
        with open('./all_gaze_data',mode='w') as f:
            for i,g in enumerate(self.all_gaze):
                ave = self.gaze_to_ave(g)
                f.write("{} {} {} {}\n".format(i,ave[0],ave[1],self.all_err[i]))
def main():
    t = Test(1440,878,(0,0))
    try:
        #t.add_track((25,25))
        """
        t.add_track((81,25))
        t.add_track((137,25))
        t.add_track((193,25))
        t.add_track((249,25))
        t.add_track((305,25))
        t.add_track((361,25))
        t.add_track((417,25))
        t.add_track((473,25))
        t.add_track((529,25))
        t.add_track((585,25))
        t.add_track((641,25))
        t.add_track((697,25))
        t.add_track((753,25))
        t.add_track((809,25))
        t.add_track((865,25))
        t.add_track((921,25))
        t.add_track((977,25))
        t.add_track((1033,25))
        t.add_track((1089,25))
        t.add_track((1145,25))
        t.add_track((1201,25))
        t.add_track((1257,25))
        t.add_track((1313,25))
        """
        #t.add_track((1369,25))
        """
        t.add_track((1369,81))
        t.add_track((1369,137))
        t.add_track((1369,193))
        t.add_track((1369,249))
        t.add_track((1369,305))
        t.add_track((1369,361))
        t.add_track((1369,417))
        t.add_track((1369,473))
        t.add_track((1369,529))
        t.add_track((1369,585))
        t.add_track((1369,641))
        t.add_track((1369,697))
        t.add_track((1369,753))
        """
        #t.add_track((1369,809))
        #t.add_track((25,137))
        """
        t.add_track((81,137))
        t.add_track((137,137))
        t.add_track((193,137))
        t.add_track((249,137))
        t.add_track((305,137))
        t.add_track((361,137))
        t.add_track((417,137))
        t.add_track((473,137))
        t.add_track((529,137))
        t.add_track((585,137))
        t.add_track((641,137))
        t.add_track((697,137))
        t.add_track((753,137))
        t.add_track((809,137))
        t.add_track((865,137))
        t.add_track((921,137))
        t.add_track((977,137))
        t.add_track((1033,137))
        t.add_track((1089,137))
        t.add_track((1145,137))
        t.add_track((1201,137))
        """
        #t.add_track((1257,137))
        """
        t.add_track((1257,193))
        t.add_track((1257,249))
        t.add_track((1257,305))
        t.add_track((1257,361))
        t.add_track((1257,417))
        t.add_track((1257,473))
        t.add_track((1257,529))
        t.add_track((1257,585))
        t.add_track((1257,641))
        t.add_track((1257,697))
        t.add_track((1257,753))
        """
        #t.add_track((1257,809))
        #t.add_track((25,249))
        """
        t.add_track((81,249))
        t.add_track((137,249))
        t.add_track((193,249))
        t.add_track((249,249))
        t.add_track((305,249))
        t.add_track((361,249))
        t.add_track((417,249))
        t.add_track((473,249))
        t.add_track((529,249))
        t.add_track((585,249))
        t.add_track((641,249))
        t.add_track((697,249))
        t.add_track((753,249))
        t.add_track((809,249))
        t.add_track((865,249))
        t.add_track((921,249))
        t.add_track((977,249))
        t.add_track((1033,249))
        t.add_track((1089,249))
        """
        #t.add_track((1145,249))
        """
        t.add_track((1145,305))
        t.add_track((1145,361))
        t.add_track((1145,417))
        t.add_track((1145,473))
        t.add_track((1145,529))
        t.add_track((1145,585))
        t.add_track((1145,641))
        t.add_track((1145,697))
        t.add_track((1145,753))
        """
        #t.add_track((1145,809))
        t.add_track_relative((1,0))
        t.add_track_relative((0,1))
        t.add_track_relative((1,1))
        t.run()
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main();
