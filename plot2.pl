set yr[1:0]
set xl "relative x"
set yl "relative y"
p "all_gaze_data" using 2:3 w lp ti "Eyes' track"
set term png
set out "plot2.png"
rep
quit
