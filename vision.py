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
        #forward/backward
        # self.tx = self.getData(0)
        #side/side
        # self.ty = self.getData(1)
        # self.area = self.getData(10)
        # self.distance = self.getData(9)
        # self.tag_ct = self.getData(11)
        # self.tag_offset_angle = self.getData(5)
        # self.tag_offset_pos = self.getData(12)
        # self.tag_offset_distance = self.getData(15)
        
    def getData(self, point):
        if len(self.nt.getNumberArray('botpose_wpiblue', [-1.0] * 11)) >= 11:
            return self.nt.getNumberArray('botpose_wpiblue', [-1.0] * 11)[point]
        else:
            return 0
    
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
    
    