import ntcore
from magicbot import tunable
from april_constants import AprilConstants


class Vision:
    nt = ntcore.NetworkTableInstance.getDefault().getTable('limelight')
    
    april_constants : AprilConstants

    def setup(self):
        self.tx = 0
        self.ty = 0
        self.area = 0
        self.distance = 0
        self.tag_ct = 0
        self.tag_offset_angle = 0
        self.tag_offset_pos = 0
        # self.tag_offset_distance = 0

    def execute(self):
        pass
        # self.dataList = self.nt.getNumberArray('botpose_wpiblue', [-1.0] * 10)
        # self.pixelList = self.nt.getNumberArray('rawfiducials', [-1.0] * 10)
        # # forward/backward
        # self.tx = self.getData(0)
        # # side/side
        # self.ty = self.getData(1)
        # self.area = self.getData(10)
        # self.distance = self.getData(9)
        # self.tag_ct = self.getData(11)
        # self.tag_offset_angle = self.getData(5)
        # self.tag_offset_pos = self.getData(12)
        # self.bs_tag_diff = self.getData(13)
        # self.pixel_offset = self.getPixelData(1)
        # # self.tag_offset_distance = self.getData(15)
        
    # def getData(self, point):
    #     if len(self.dataList) > point:
    #         return self.dataList[point]
    #     else:
    #         return 0
    
    # def getPixelData(self, point):
    #     if len(self.pixelList) > point:
    #         return self.pixelList[point]
    #     else:
    #         return 0
        
    # def getClosestTag(self):
    #     temp_data = self.dataList
    #     total_tags = (len(temp_data) - 10) / 7
    #     closest_tag = 0
    #     if total_tags <= 0:
    #         return 0
    #     elif total_tags == 1:
    #         return self.tag_ct
    #     elif total_tags > 1:
    #         tag_dist_list = []
    #         tag_id_list = []
            
            # for tag in range(int(total_tags)):
            #     tag_id_list.append(temp_data[11 + (tag * 7)])
            #     #ERM fix this
            #     tag_dist_list.append(temp_data[14 + (tag * 7)])
            # closest_tag = tag_id_list[tag_dist_list.index(max(tag_dist_list))]
            # return closest_tag
            
        #     robot_pos = self.ty
        #     for tag in range(int(total_tags)):
        #         tag_id_list.append(temp_data[11 + (tag * 7)])
        #         #ERM fix this
        #         tag_dist_list.append(abs(self.april_constants.tagy[round(tag_id_list[tag])] - robot_pos))
        #     closest_tag = tag_id_list[tag_dist_list.index(min(tag_dist_list))]
        #     return closest_tag
            
        # else:
        #     return 0
                
        
    # def blind(self):
    #     return len(self.dataList) < 11
    
    def getArea(self) -> float:
        return self.area

    def getX(self) -> float:
        return self.tx

    def getY(self) -> float:
        return self.ty

    def getDistance(self) -> float:
        return self.distance
    
    def getAngleOffset(self) -> float:
        return self.tag_offset_angle
    
    def getOffsetPosition(self) -> float:
        return self.tag_offset_pos
    
    def foundTag(self, tag) -> bool:
        if tag == self.tag_ct:
            return self.getArea() > 0
        else:
            return False
        
    def AlignedTag(self, tag) -> bool:
        err = 0.2
        if tag == self.tag_ct:
            return abs(self.getOffsetPosition()) < err
        else:
            return False
    
    