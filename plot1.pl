p "all_gaze_data" using 1:2 w lp ti "relative x"
rep "all_gaze_data" using 1:3 w lp ti "relative y"
rep "all_gaze_data" using 1:4 w lp ti "relative error"
set xl "time[60fps]"
set yl "relative size 0-1 of screen"
set term png
set out "plot1.png"
rep
quit
