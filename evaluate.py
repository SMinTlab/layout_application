# -*- coding: utf-8 -*-
import tobii_research as tr
import time
import copy
import numpy as np
from operator import mul
from operator import add
from functools import reduce
import sys

MICROSEC = 0.000001

class Test:
    tracks = []
    lines = []
    width, height = 0, 0
    eyetracker = None
    gaze_data = []
    gaze_data_buffer = []
    epsilon = 0.01
    lap_times = []
    passed = 0
    errors = []
    error_buffer = None
    navi = True
    all_gaze = []
    all_err = []

    def __init__(self, width, height, start):
        self.width = width
        self.height = height
        self.tracks.append(start)

    def add_track_relative(self, next):
        r = reduce(mul,next)
        if r < 0 or r > 1:
            raise Exception("Out of screen.")
        prev = self.tracks[-1]
        a = next[1] - prev[1]
        b = prev[0] - next[0]
        c = prev[1] * next[0] - prev[0] * next[1]
        print("a = {}, b = {}, c = {}".format(a,b,c))
        line = (a,b,c)
        self.lines.append(line)
        self.tracks.append(next)

    def add_track(self, next):
        _next = (next[0]/self.width, next[1]/self.height)
        self.add_track_relative(_next)

    def gaze_data_callback(self,gaze_data):
        if gaze_data["left_gaze_point_validity"]+gaze_data["right_gaze_point_validity"] is 2:
            g = (gaze_data["left_gaze_point_on_display_area"], gaze_data["right_gaze_point_on_display_area"], gaze_data["device_time_stamp"])
            self.all_gaze.append(g)
            ave = self.gaze_to_ave(g)
            self.all_err.append(self.sq_dist_pl(ave[0],ave[1],self.lines[self.passed]))
            if len(self.gaze_data) % 2 is 1:
                if not self.in_sight(self.tracks[self.passed - 1],g):
                    print("Start from {}".format(self.tracks[self.passed - 1]))
                    self.gaze_data.append(g)
            else:
                for i,p in enumerate(self.tracks):
                    if i >= self.passed - 1:
                        if self.in_sight(p,g):
                            skip = i - self.passed
                            if skip < 0:
                                print("Back to {}".format(p))
                                self.gaze_data.pop(-1)
                                self.gaze_data_buffer.clear()
                                self.error_buffer[self.passed - 1].fill(0.0)
                            else:
                                print("In sight. {}, skip={}".format(p,skip))
                                for j in range(skip):
                                    try:
                                        nearest = self.nearest_from(self.tracks[self.passed + j])
                                        self.gaze_data.append(nearest)
                                        self.gaze_data.append(nearest)
                                        self.errors.append(self.error_buffer[self.passed + j - 1])

                                    except Exception as e:
                                        print(e)
                                        sys.exit(1)

                                self.gaze_data.append(g)
                                self.errors.append(list(self.error_buffer[self.passed-1]))
                                self.navi = True
                                self.passed += skip + 1
                                self.gaze_data_buffer.clear()
                        else:
                            self.gaze_data_buffer.append(g)
                            self.acc_err(g)

    def acc_err(self, gaze_data):
        dists = [[],[]]
        for l in self.lines:
            dists[0].append(self.sq_dist_pl(gaze_data[0][0],gaze_data[0][1],l))
            dists[1].append(self.sq_dist_pl(gaze_data[1][0],gaze_data[1][1],l))
        min_idx = dists[0].index(min(dists[0]))
        self.error_buffer[self.passed-1][0] += dists[0][min_idx]
        self.error_buffer[self.passed-1][1] += dists[1][min_idx]

    def nearest_from(self,point):
        if len(self.gaze_data_buffer) <= 0:
            raise Exception("No buffer.")
        nearest = self.gaze_data_buffer[0]
        for g in self.gaze_data_buffer:
            if self.sq_dist_pp(self.gaze_to_ave(nearest), point) > self.sq_dist_pp(self.gaze_to_ave(g),point):
                nearest = g
        return nearest

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
        self.error_buffer = np.zeros((len(self.lines),2) , dtype=np.float)
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
        while self.passed < len(self.tracks):
            time.sleep(1/60)
            if self.navi and self.passed < len(self.tracks):
                print("Checking {}.".format(self.tracks[self.passed]))
                self.navi = False

        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
        print("finished.")
        print("epsilon = {}".format(self.epsilon))
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
        with open('./all_gaze_data',mode='a') as f:
            for i,g in enumerate(self.all_gaze):
                ave = self.gaze_to_ave(g)
                f.write("{} {} {} {}\n".format(i,ave[0],ave[1],self.all_err[i]))
def main():
    t = Test(1440,878,(0,0))
    try:
        t.add_track((25,25))
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
        t.add_track((1369,25))
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
        t.add_track((1369,809))
        t.add_track((25,137))
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
        t.add_track((1257,137))
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
        t.add_track((1257,809))
        t.add_track((25,249))
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
        t.add_track((1145,249))
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
        t.add_track((1145,809))
        t.run()
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main();
