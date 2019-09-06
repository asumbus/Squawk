import datetime

busstops = {

    # Definition of function
    # Stopname: (stop_north, stop_east, stop_heading, circle_size, delay_time, 'stop_name', 'mp3')

    "UC": (272795.00, 5194222.00, 207, 20, 60, 'UC', 'uc'),
    "Science": (272422.99, 5193611.66, 270, 20, 60, 'Science', 'foo'),
    "Dornblaser": (271683.60, 5192717.74, 270, 20, 60, 'Dornblaser Out', 'dorn'),
    "Dornblaser_Inbound": (271683.60, 5192717.74, 90, 20, 60, 'Dornblaser IN', 'dorn'),
    "LC": (271482.00, 5192322.00, 120, 10, 60, 'L&C', 'lc'),
    "LC_Gold": (271558.00, 5192094.00, 15, 20, 60, 'L&C Gold', 'lcg'),
    "Miller": (272146.6, 5193673.59,  0, 20, 60, 'Miller Hall', 'miller'),
    "Music": (272274.55, 5194166.35, 90, 20, 60, 'Music', 'music'),
    "Downtown_Transfer": (271802.00, 5195520.00, 200, 20, 60, 'Downtown Transfer', 'downtown'),
    "Missoula_College": (273223.73, 5194499.81, 220, 20, 60, 'Missoula College', 'mc'),
    "5th_and_Orange": (728391.34, 5194522.77, 275, 40, 180, '5th & Orange', '5th'),
    "Russel_and_Dakota": (727207.93, 5195130.11, 180, 20, 60, 'Russel & Dakota', 'russell'),
    "6th_and_Chestnut": (728413.82, 5194415.27, 85, 20, 60, '6th & Chestnut', '6th'),
    "Garage": (272933.21, 5194323.15, 250, 20, 60, 'Garage', 'garage'),
}


#########################
# PSA Section #

date1 = datetime.datetime(2016, 3, 10, 7, 00)
date2 = datetime.datetime(2016, 3, 10, 19, 00)

psastops = {

    # Definition of function
    # Stopname: (stop_north, stop_east, stop_heading, circle_size, delay_time, 'stop_name', 'mp3')

    "PSA1": (272119.36, 5192900.83, 0, 20, 60, 'PSA', 'psa'),
}



