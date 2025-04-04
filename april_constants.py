import math

class AprilConstants:
    pass

    def execute(self):
        lr_offset = 0.3556
        righty_x = lr_offset * math.cos(math.radians(30))
        righty_y = lr_offset * math.sin(math.radians(30))
        
        #Tag 1
        tag1x = 16.687292
        tag1y = 0.628142
        tag1t = 54
        
        #Tag 2
        tag2x = 16.687292
        tag2y = 7.414259999999999
        tag2t = -54
        
        #Tag 3
        tag3x = 11.49096
        tag3y = 8.031733999999998
        tag3t = -90
        
        #Tag 4
        tag4x = 9.276079999999999
        tag4y = 6.132575999999999
        tag4t = 180
        
        #Tag 5
        tag5x = 9.276079999999999
        tag5y = 1.9098259999999998
        tag5t = 180
        
        #Tag 6
        tag6x = 13.474446
        tag6y = 3.3012379999999997
        tag6xr = tag6x + righty_x
        tag6yr = tag6y + righty_y
        tag6t = -150
        
        #Tag 7
        tag7x = 13.890498
        tag7y = 4.0208200000000005
        tag7xr = tag7x
        tag7yr = tag7y + lr_offset
        tag7t = 180
        
        #Tag 8
        tag8x = 13.474446
        tag8y = 4.740402
        tag8xr = tag8x - righty_x
        tag8yr = tag8y + righty_y
        tag8t = 150
        
        #Tag 9
        tag9x = 12.643358
        tag9y = 4.740402
        tag9xr = tag9x - righty_x
        tag9yr = tag9y - righty_y
        tag9t = 60
        
        #Tag 10
        tag10x = 12.227305999999999
        tag10y = 4.0208200000000005
        tag10xr = tag10x
        tag10yr = tag10y - lr_offset
        tag10t = 0
        
        #Tag 11
        tag11x = 12.643358
        tag11y = 3.3012379999999997
        tag11xr = tag11x + righty_x
        tag11yr = tag11y - righty_y
        tag11t = -60
        
        #Tag 12
        tag12x = 0.8613139999999999
        tag12y = 0.628142
        tag12t = 126

        #Tag 13
        tag13x = 0.8613139999999999
        tag13y = 7.414259999999999
        tag13t = -126
        
        #Tag 14
        tag14x = 8.272272
        tag14y = 6.132575999999999
        tag14t = 0
        
        #Tag 15
        tag15x = 8.272272
        tag15y = 1.9098259999999998
        tag15t = 0
        
        #Tag 16
        tag16x = 6.057646
        tag16y = 0.010667999999999999
        tag16t = 90
        
        #Tag 17
        tag17x = 4.073905999999999
        tag17y = 3.3012379999999997
        tag17xr = tag17x + righty_x
        tag17yr = tag17y - righty_y
        tag17t = -60
        
        #Tag 18
        tag18x = 3.6576
        tag18y = 4.0208200000000005
        tag18xr = tag18x
        tag18yr = tag18y - lr_offset
        tag18t = 0
        
        #Tag 19
        tag19x = 4.073905999999999
        tag19y = 4.740402
        tag19xr = tag19x - righty_x
        tag19yr = tag19y - righty_y
        tag19t = 60
        
        #Tag 20
        tag20x = 4.904739999999999
        tag20y = 4.740402
        tag20xr = tag20x - righty_x
        tag20yr = tag20y + righty_y
        tag20t = 150
        
        #Tag 21
        tag21x = 5.321046
        tag21y = 4.0208200000000005
        tag21xr = tag21x
        tag21yr = tag21y + lr_offset
        tag21t = 180
        
        #Tag 22
        tag22x = 4.904739999999999
        tag22y = 3.3012379999999997
        tag22xr = tag22x + righty_x
        tag22yr = tag22y + righty_y
        tag22t = -150
        
        self.tagx = [0, tag1x, tag2x, tag3x, tag4x, tag5x, tag6x, tag7x, tag8x, tag9x, tag10x, tag11x, tag12x, tag13x, tag14x, tag15x, tag16x, tag17x, tag18x, tag19x, tag20x, tag21x, tag22x]
        self.tagy = [0, tag1y, tag2y, tag3y, tag4y, tag5y, tag6y, tag7y, tag8y, tag9y, tag10y, tag11y, tag12y, tag13y, tag14y, tag15y, tag16y, tag17y, tag18y, tag19y, tag20y, tag21y, tag22y]
        self.tagxr = [0, tag1x, tag2x, tag3x, tag4x, tag5x, tag6xr, tag7xr, tag8xr, tag9xr, tag10xr, tag11xr, tag12x, tag13x, tag14x, tag15x, tag16x, tag17xr, tag18xr, tag19xr, tag20xr, tag21xr, tag22xr]
        self.tagyr = [0, tag1y, tag2y, tag3y, tag4y, tag5y, tag6yr, tag7yr, tag8yr, tag9yr, tag10yr, tag11yr, tag12y, tag13y, tag14y, tag15y, tag16y, tag17yr, tag18yr, tag19yr, tag20yr, tag21yr, tag22yr]
        self.tagt = [0, tag1t, tag2t, tag3t, tag4t, tag5t, tag6t, tag7t, tag8t, tag9t, tag10t, tag11t, tag12t, tag13t, tag14t, tag15t, tag16t, tag17t, tag18t, tag19t, tag20t, tag21t, tag22t]
        