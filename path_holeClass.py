import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import bezier as bz
from sympy import symbols
import sympy as sy
from decimal import Decimal
import math


class Hole:
    class LineB:
        """
        用于存放形成孔的单根纤维信息
        """

        def __init__(self, path: list, location):
            self.path = path
            self.location = location
            self.direction = 0  # 0,3,2,1 -> y+,x-,y-,x+
            self.startend=0

        def getDirection(self):
            return self.direction



    def __init__(self, r, location, hatchingSpace, ab=2.0, linenum=8, acc=50, line_type="b", deform_factor=0.8, wa=3.5,
                 type="half", lenOfStraight=10):
        """
        the pattern of single half hole, with several fibers
        :param r: hole radius printed(real hole, hatching space not considered)
        :param hatchingSpace: hatching space
        :param location: center of hole, coordinate
        :param ab: a/b factor
        :param linenum: half of fibers to form hole pattern
        :param acc: accuracy
        :param line_type: b for bezier
        :param deform_factor: df
        :param wa: draw a factor
        :param lenOfStraight: for s_l ,length of straight line
        """
        self.fiber = []
        self.hatchingspace = hatchingSpace
        self.r_path = r + (hatchingSpace / 2)
        self.location = location
        self.linenum = linenum
        self.line_type = line_type
        self.acc = acc
        self.df = deform_factor
        self.wa = wa
        self.ab = ab
        self.a = ab * r
        self.length = self.wa * self.a * 2
        self.c = math.sqrt(pow((self.a), 2) - pow(r, 2))
        self.type = type
        self.lenOfStraight = lenOfStraight
        # self.__generate_hole_pattern()
        for i in range(0, self.linenum):
            pat = self.__generate_hole_pattern_single(lineOrder=i)
            self.fiber.append(pat)
        if line_type == "s_h":
            self.length += self.lenOfStraight
        # if type != "half":
        #     # 再创建一半,还没写好
        #     for i in range(0, self.linenum):
        #         pat = self.__generate_hole_pattern_single(lineOrder=i)
        #         self.symmetrySingleLine(line=pat, axis="x")
        #         self.fiber.append(pat)
        self.translate(self.location[0], self.location[1])

    def __change_direction(self, line: LineB, clockwise):
        line.direction = line.direction + clockwise
        if line.direction >= 4:
            line.direction = line.direction - 4
        if line.direction < 0:
            line.direction = line.direction + 4

    # def __generate_hole_pattern(self):
    #     # 生成起点在同一位置的若干曲线
    #     for i in range(0, self.linenum):
    #         pat = self.__generate_hole_pattern_single(lineOrder=i)
    #         self.fiber.append(pat)

    def __generate_hole_pattern_single(self, lineOrder=0):
        data = []
        xx = []
        yy = []
        pointset = []
        if self.line_type == "b":
            # bezier
            P0 = (-1 * (self.length / 2), 0)
            P1 = (-1 * self.c / 2, 0)
            P2 = [0, 1]  # P2[1] will inited later
            P3 = (self.c / 2, 0)
            P4 = ((self.length / 2), 0)
            P2[1] = ((self.r_path / (pow(0.5, 4)) - P0[1] - 4 * P1[1] - 4 * P3[1] - P4[1]) / 6) * pow(self.df,
                                                                                                      lineOrder)
            x = [P0[0], P1[0], P2[0], P3[0], P4[0]]
            y = [P0[1], P1[1], P2[1], P3[1], P4[1]]
            a = np.array([x, y])
            curve = bz.Curve(a, degree=4)
            t_vals = np.linspace(0.0, 1.0, self.acc)
            data = curve.evaluate_multi(t_vals)
            # for i in range(0, len(data)):
            xx = data[0]
            yy = data[1]
            pointset = list(zip(xx, yy))
        if self.line_type == "s_h":
            # bezier
            P0 = (-1 * (self.length / 2), 0)
            P1 = (-1 * self.c / 2, 0)
            P2 = [0, 1]  # P2[1] will inited later
            P3 = (self.c / 2, 0)
            P4 = ((self.length / 2), 0)
            P2[1] = ((self.r_path / (pow(0.5, 4)) - P0[1] - 4 * P1[1] - 4 * P3[1] - P4[1]) / 6) * pow(self.df,
                                                                                                      lineOrder)
            x = [P0[0], P1[0], P2[0], P3[0], P4[0]]
            y = [P0[1], P1[1], P2[1], P3[1], P4[1]]
            a = np.array([x, y])
            curve = bz.Curve(a, degree=4)
            t_vals = np.linspace(0.0, 1.0, self.acc)
            data = curve.evaluate_multi(t_vals)
            # 直线部分
            linex = np.linspace((self.lenOfStraight / 2) * -1, (self.lenOfStraight / 2), self.acc)
            liney = np.full_like(linex, data[1][(round(np.size(data, axis=1) / 2))])
            arrayx = np.asarray(linex)
            arrayy = np.asarray(liney)
            dataline = np.vstack((arrayx, arrayy))
            data1 = data[0, 0:(round(np.size(data, axis=1) / 2))] - (self.lenOfStraight / 2)
            d1 = np.vstack((data1, data[1, 0:(round(np.size(data, axis=1) / 2))]))
            data2 = data[0, (round(np.size(data, axis=1) / 2)):] + (self.lenOfStraight / 2)
            d2 = np.vstack((data2, data[1, (round(np.size(data, axis=1) / 2)):]))
            # data = np.insert(data, [round(np.size(data, axis=1) / 2)], dataline, axis=1)
            data = np.hstack((d1, dataline))
            data = np.hstack((data, d2))
            xx = data[0]
            yy = data[1]
            pointset = list(zip(xx, yy))
        line = self.LineB(path=pointset, location=[0, 0])
        return line

    def __rotate_hole_90(self, line: LineB, center=[0, 0], clockWise=-1):
        """
        rotate hole 90 by unclockwise
        :param line: points set of hole pattern
        :param clockWise: 1 for clockwise,-1 for unclockwise
        :return:
        """
        xSet, ySet, *zSet = zip(*line.path)
        xr = []
        yr = []
        ori = [0, 0]
        for i in range(0, len(xSet)):
            xr.append(center[0] + clockWise * (ySet[i] - center[1]))
            yr.append(center[1] + (-1 * clockWise) * (xSet[i] - center[0]))
        # print(xSet)
        pointset = list(zip(xr, yr))
        ori[0] = line.location[0] + clockWise * (line.location[1] - center[1])
        ori[1] = line.location[1] + (-1 * clockWise) * (line.location[0] - center[0])
        self.__change_direction(line, clockWise)
        line.path = pointset
        line.location = ori
        return pointset, ori

    def __translate_hole(self, line: LineB, dx=0, dy=0):
        """
        move hole

        :param line: points set of hole
        :param dx: move along x ward
        :param dy: move along y ward
        :param dz: move along z ward
        :return:
        """
        xSet, ySet = zip(*line.path)
        xt = []
        yt = []
        ori = [0, 0]
        for i in range(0, len(xSet)):
            xt.append(xSet[i] + dx)
            yt.append(ySet[i] + dy)
        pointset = list(zip(xt, yt))
        ori[0] = line.location[0] + dx
        ori[1] = line.location[1] + dy
        line.path = pointset
        line.location = ori
        return pointset, ori

    def __symmetry_hole(self, line: LineB, location, axis="x"):
        xSet, ySet, *zSet = zip(*line.path)
        xs = []
        ys = []
        ori = [0, 0]
        pointset = []
        if axis == "x":
            for i in range(0, len(xSet)):
                xs.append(xSet[i])
                ys.append(2 * location[1] - ySet[i])
            pointset = list(zip(xs, ys))
            if line.direction == 0 or line.direction == 2:
                line.direction = line.direction + 2
                if line.direction >= 4:
                    line.direction = line.direction - 4
                if line.direction < 0:
                    line.direction = line.direction + 4

        if axis == "y":
            for i in range(0, len(xSet)):
                xs.append(2 * location[0] - xSet[i])
                ys.append(ySet[i])
            pointset = list(zip(xs, ys))
            if line.direction == 1 or line.direction == 3:
                line.direction = line.direction + 2
                if line.direction >= 4:
                    line.direction = line.direction - 4
                if line.direction < 0:
                    line.direction = line.direction + 4

        return pointset

    def symmetrySingleLine(self, line: LineB, axis="y"):
        line.path = self.__symmetry_hole(line, line.location, axis)
        return line.path

    def symmetry(self, center, axis="x"):
        for i in range(0, self.linenum):
            self.fiber[i].path = self.__symmetry_hole(self.fiber[i], center, axis)

    def symmetryAndReoder(self, axis="x"):
        for i in range(0, self.linenum):
            self.fiber[i].path = self.__symmetry_hole(self.fiber[i], self.fiber[i].location, axis)
        if axis == "x":
            self.fiber.reverse()

    def translate(self, dx=0, dy=0):
        for i in range(0, len(self.fiber)):
            self.__translate_hole(self.fiber[i], dx, dy)
        lx = self.fiber[0].location[0]
        ly = self.fiber[0].location[1]
        self.location = (lx, ly)

    def translateSingleLine(self, line: LineB, dx=0, dy=0):
        """
        平移某根曲线的位置
        :param line: LineB
        :param dx: x量
        :param dy: y量
        :return:
        """
        self.__translate_hole(line, dx, dy)

    def rotate90(self, center, clockwise=-1):

        for i in range(0, self.linenum):
            self.__rotate_hole_90(line=self.fiber[i], clockWise=clockwise, center=center)

    def rotate90singleLine(self, line: LineB, center=None, clockwise=-1):
        if center is None:
            center = line.location
        self.__rotate_hole_90(line=line, center=center, clockWise=clockwise)

    def getLocation(self):
        return self.location

    def getLength(self):
        return self.length

    def getTotalWideth_half(self, hatchingspace):
        return (hatchingspace * (self.linenum - 1) + self.r_path * pow(self.df, self.linenum - 1))

    def getAllPath(self):
        """将每条曲线首尾相连"""
        all_path = []
        for i in range(0, len(self.fiber)):
            all_path.extend(self.fiber[i].path)
        return all_path

    def disturbeByHatchingSpace(self, hatchingSpace, direction=1):
        for i in range(1, self.linenum):
            self.translateSingleLine(self.fiber[i], dy=hatchingSpace * i * direction)


if __name__ == '__main__':
    hl = Hole(r=3, hatchingSpace=0.5, ab=2, linenum=2, location=(0, 0), acc=100, type="half", line_type="s_h",
              lenOfStraight=10)
    hl2 = Hole(r=3, hatchingSpace=0.5, ab=2, linenum=1, location=(0, 0), acc=100, type="half", line_type="b",
               lenOfStraight=10, wa=3.5)
    # hl.symmetry(axis="y")
    # hl.symmetrySingleLine(1, axis="y")
    # hl.symmetrySingleLine(1, axis="y")
    # hl.rotate90singleLine(hl.fiber[2], clockwise=-1, center=hl.location)
    # hl.rotate90singleLine(hl.fiber[2], clockwise=-1, center=hl.location)
    # hl.symmetrySingleLine(hl.fiber[1], "x")
    # hl.symmetrySingleLine(hl.fiber[1], "y")

    # for i in range(0, hl.linenum):
    #     x, y = zip(*hl.path[i])
    #     plt.plot(x, y)
    # hl.symmetryAndReoder(axis="x")
    # hl.disturbeByHatchingSpace(0.5)
    x, y = zip(*hl2.getAllPath())
    print(hl.fiber[0].direction)
    plt.plot(x, y)
    # x, y = zip(*hl2.getAllPath())
    plt.plot(x, y)
    plt.show()
    pass
