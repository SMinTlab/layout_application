# -*- coding: utf-8 -*-
import tobii_research as tr
import time
import copy
import numpy as np

class Test:
    tracks = []
    lines = []
    width, height = 0, 0
    eyetracker = None
    gaze_data = []
    epsilon = 0.05
    lap_times = []
    passed = 0
    errors = []

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def set_track_relative(self, begin, end):
        track = (begin, end)
        self.tracks.append(track)
        a = end[1] - begin[1]
        b = begin[0] - end[0]
        c = begin[1] * end[0] - begin[0] * end[1]
        print("a = {}, b = {}, c = {}".format(a,b,c))
        line_ex = (a,b,c)
        self.lines.append(line_ex)

    def set_track(self, begin, end):
        b = (begin[0]/self.width,begin/self.height)
        e = (end[0]/self.width, end/self.height)
        self.set_track_relative(b,e)

    def gaze_data_callback(self,gaze_data):
        if gaze_data["left_gaze_point_validity"]+gaze_data["right_gaze_point_validity"] is 2:
            #print("left(x, y) = {}".format(gaze_data["left_gaze_point_on_display_area"]))
            #print("right(x, y) = {}".format(gaze_data["right_gaze_point_on_display_area"]))
            self.gaze_data.append([gaze_data["left_gaze_point_on_display_area"],gaze_data["right_gaze_point_on_display_area"]])

    def sq_dist(self, x, y):
        if self.passed / 2  < len(self.lines):
            line = self.lines[int(self.passed / 2)]
            return pow(line[0] * x + line[1] * y + line[2], 2) / (pow(line[0], 2) + pow(line[1], 2))
        return 0

    def sum_all_gaze_error(self,err):
        for data in self.gaze_data:
            err[0] += self.sq_dist(*(data[0]))
            err[1] += self.sq_dist(*(data[1]))
        return err

    def in_sight(self, x, y):
        for data in self.gaze_data:
            for side in data:
                if abs(x - side[0]) < self.epsilon and abs(y - side[1]) < self.epsilon:
                    return True
        return False

    def run(self):
        if self.eyetracker is None:
            et = tr.find_all_eyetrackers()
            if len(et) > 0:
                self.eyetracker = et[0]
            else:
                print("No eyetracker was found.")
                return
        print("running...")
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
        navigation = True
        start = time.time()
        end = start
        b = False
        self.passed = 0
        err = np.zeros(2, dtype=np.float)
        check = self.tracks[0][0]
        while self.passed < 2*len(self.tracks):
            time.sleep(1/60)
            self.sum_all_gaze_error(err)
            if navigation:
                print("Checking {}.".format(self.tracks[int(self.passed /2)][int(self.passed % 2)]))
                navigation = False
            for i, track in enumerate(self.tracks):
                if navigation:
                    break
                for j, point in enumerate(track):
                    if (j % 2 is 0 and self.passed - 1 <= 2 * i + j) or self.passed <= 2 * i + j:
                        skip = 2 * i + j - self.passed
                        if self.in_sight(*point):
                            print("In sight {}".format(self.tracks[i][j]))
                            if j % 2 is 0 and skip <= 0:
                                start = time.time()
                                err.fill(0)
                                check = self.tracks[i][j]
                            else:
                                transfer_time = start - end
                                end = time.time()
                                elapsed_time = end - start
                                for l in range(skip):
                                    self.lap_times.append(0)
                                self.lap_times.append(transfer_time)
                                self.lap_times.append(elapsed_time)
                                self.errors.append(list(err))
                                err = np.zeros(2, dtype=np.float)
                                start = end
                                print("passed {} -> {} in {}[sec]".format(check,self.tracks[i][j],elapsed_time))
                            self.gaze_data.clear()
                            navigation = True
                            self.passed += skip + 1
                            print("passed = {}".format(self.passed))

        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
        print("finished.")
        print("epsilon = {}".format(self.epsilon))
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

def main():
    t = Test(1440,878)
    t.set_track_relative((0,0),(1,0))
    t.set_track_relative((1,0),(0,1))
    t.set_track_relative((0,1),(1,1))
    t.run()

if __name__ == "__main__":
    main();
