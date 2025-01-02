import math

import numpy as np
from path_holeClass import Hole
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import copy
from scipy.spatial import KDTree

"""默认生成0，0为角，整体在x+，y+区域内的zigzag"""


class Zigzag:
    def __init__(self, length=50, width=50, hatching_space=1, num=50, originPoint=(0, 0), z=0.0, hole: Hole = None):
        # Parameters
        self.length = length  # multiple times of hatching_space ,along-fiber-ward
        self.width = width  # vertical fiber ward
        self.hatching_space = hatching_space
        self.hatching_space_in_real = hatching_space  # will be changed in generate
        self.num = num
        self.originPoint = originPoint
        self.threePoint = []
        self.path, self.originPoint = self.__generate_base_zigzag(self.length, self.width, self.hatching_space,
                                                                  self.num, self.originPoint)
        self.hole_list = []
        self.hole = hole
        self.holeLocation = None
        self.hole_Locations = []
        self.center = [self.originPoint[0] + (self.length / 2), self.originPoint[1] + (self.width / 2)]
        self.insertHole(hole1=self.hole)
        self.x, self.y = zip(*self.path)
        self.z = z
        self.zarray = np.full_like(self.x, z)

        # about hole

    def insertHole(self, hole1: Hole):
        if hole1 is not None:
            """改"""
            hole2 = copy.deepcopy(hole1)
            hole = copy.deepcopy(hole1)
            hole.disturbeByHatchingSpace(hatchingSpace=self.hatching_space_in_real, direction=1)

            self.__insertHole(hole=hole, direction=1)
            hole2.symmetryAndReoder(axis="x")
            hole2.disturbeByHatchingSpace(hatchingSpace=self.hatching_space_in_real, direction=-1)

            self.__insertHole(hole=hole2, direction=-1)
            self.holeLocation = list(hole.location)
            self.hole_Locations.append(hole.location)
            self.hole_list.append([hole, hole2])

    def __preFind(self, hole: Hole = None, direction=1):
        if hole is None:
            return
        else:
            # 查找区域边缘
            p0 = [0, 0]
            p1 = [0, 0]
            p2 = [0, 0]
            p3 = [0, 0]
            # 预搜索 仅搜索该方向第一根纤维，用于调整add

            # p3                     p2 ^y
            # p0 ~~~hole.location~~~ p1 |
            # ------------------->x     |
            # p0 ~~~hole.location~~~ p1 |
            # p3                     p2 |
            isLastPointInArea = 0
            areaInIndex = []
            areaOutIndex = []
            if hole.type == "half":
                p0[0] = hole.location[0] - hole.length / 2
                p0[1] = hole.location[1]
                p1[0] = hole.location[0] + hole.length / 2
                p1[1] = hole.location[1]
                p2[0] = p1[0]
                p2[1] = p1[1] + self.hatching_space_in_real * direction
                p3[0] = p0[0]
                p3[1] = p2[1]

                for i in range(0, len(self.path)):
                    isThisPointInArea = 0  # 每次循环中初始化
                    newpoint = self.path[i]
                    if direction == -1:
                        if p0[0] <= self.path[i][0] <= p1[0]:
                            if p3[1] <= self.path[i][1] <= p0[1]:
                                # 在区域内
                                isThisPointInArea = 1
                                if isLastPointInArea == 0:  # 刚进区域
                                    areaInIndex.append(i)
                                    isLastPointInArea = 1
                        # 不在区域内
                        if isLastPointInArea == 1 and isThisPointInArea == 0:  # 刚出区域
                            areaOutIndex.append(i)
                            isLastPointInArea = 0
                    if direction == 1:
                        if p0[0] <= self.path[i][0] <= p1[0]:
                            if p0[1] <= self.path[i][1] <= p3[1]:
                                # 在区域内
                                isThisPointInArea = 1
                                if isLastPointInArea == 0:  # 刚进区域
                                    areaInIndex.append(i)
                                    isLastPointInArea = 1
                        # 不在区域内
                        if isLastPointInArea == 1 and isThisPointInArea == 0:  # 刚出区域
                            areaOutIndex.append(i)
                            isLastPointInArea = 0

            add = self.path[areaInIndex[0]][1] - hole.location[1]
            return add

    def __findEdge(self, hole: Hole = None, direction=1, add=0):
        if hole is None:
            return
        else:
            # 查找区域边缘
            p0 = [0, 0]
            p1 = [0, 0]
            p2 = [0, 0]
            p3 = [0, 0]
            # 预搜索 仅搜索该方向第一根纤维，用于调整add
            add = self.__preFind(hole=hole, direction=direction)
            # p3                     p2 ^y
            # p0 ~~~hole.location~~~ p1 |
            # ------------------->x     |
            # p0 ~~~hole.location~~~ p1 |
            # p3                     p2 |
            isLastPointInArea = 0
            areaInIndex = []
            areaOutIndex = []
            if hole.type == "half":
                p0[0] = hole.location[0] - hole.length / 2
                p0[1] = hole.location[1]
                p1[0] = hole.location[0] + hole.length / 2
                p1[1] = hole.location[1]
                p2[0] = p1[0]
                p2[1] = p1[1] + hole.getTotalWideth_half(self.hatching_space_in_real) * direction
                p3[0] = p0[0]
                p3[1] = p2[1]
                self.threePoint.append(p0)
                self.threePoint.append(p1)
                self.threePoint.append(p2)
                self.threePoint.append(p3)

                for i in range(0, len(self.path)):
                    isThisPointInArea = 0  # 每次循环中初始化
                    newpoint = self.path[i]
                    if direction == -1:
                        if p0[0] <= self.path[i][0] <= p1[0]:
                            if p3[1] + add <= self.path[i][1] <= p0[1]:
                                # 在区域内
                                isThisPointInArea = 1
                                if isLastPointInArea == 0:  # 刚进区域
                                    areaInIndex.append(i)
                                    isLastPointInArea = 1
                        # 不在区域内
                        if isLastPointInArea == 1 and isThisPointInArea == 0:  # 刚出区域
                            areaOutIndex.append(i)
                            isLastPointInArea = 0
                    if direction == 1:
                        if p0[0] <= self.path[i][0] <= p1[0]:
                            if p0[1] <= self.path[i][1] <= p3[1] + add:
                                # 在区域内
                                isThisPointInArea = 1
                                if isLastPointInArea == 0:  # 刚进区域
                                    areaInIndex.append(i)
                                    isLastPointInArea = 1
                        # 不在区域内
                        if isLastPointInArea == 1 and isThisPointInArea == 0:  # 刚出区域
                            areaOutIndex.append(i)
                            isLastPointInArea = 0

                return areaInIndex, areaOutIndex

    def __insertHole(self, hole: Hole = None, direction=1):
        if hole is None:
            return 0
        else:
            areaInIndex, areaOutIndex = self.__findEdge(hole=hole, direction=direction)
            # 倒序删除并替换
            for j in range(0, hole.linenum):
                i = hole.linenum - j - 1
                dy = self.path[areaInIndex[i]][1] - hole.fiber[i].location[1]
                # hole.translate(dx=0, dy=dy)
                # 调整曲线方向
                if (self.path[areaInIndex[i]][0] - self.path[areaOutIndex[i]][0]) * (
                        hole.fiber[i].path[0][0] - hole.fiber[i].path[len(hole.fiber[i].path) - 1][0]) < 0:  # 方向相反
                    hole.symmetrySingleLine(hole.fiber[i], axis="y")
                # 将曲线和直线对齐
                hole.translateSingleLine(hole.fiber[i], dy=dy)
                # 删除多余直线
                self.path[areaInIndex[i]:areaOutIndex[i]] = []
                # 将曲线插入直线中
                for k in range(0, len(hole.fiber[i].path)):
                    self.path.insert(areaInIndex[i] + k, hole.fiber[i].path[k])
                    a = self.path[len(self.path) - 1]

    def __generate_base_zigzag(self, length, width, hatching_space, num, originPoint=(0, 0)):
        """
        generate zigzag
        :param length: along fiber
        :param width: vertical to fiber
        :param hatching_space: fiber width
        :param num: acceleration
        :param originPoint: the origin
        :return: points of zigzag, origin
        """
        points = []
        num_lines = int(width / hatching_space)  # need 'num-lines' fibers to reach width
        hatching_space = width / num_lines  # re-generate hatching_space by 'num-lines'
        self.hatching_space_in_real = hatching_space
        for i in range(num_lines + 1):
            if i % 2 == 0:  # i from 0 to num_lines-1 , odd fibers,even i
                x_points = np.linspace(0 + originPoint[0], length + originPoint[0], num=num)
                x_points = np.round(x_points, 2)
            else:
                x_points = np.linspace(length + originPoint[0], 0 + originPoint[0], num=num)
            y_points = np.full_like(x_points, (i * hatching_space) + originPoint[1])
            y_points = np.round(y_points)
            points.extend(list(zip(x_points, y_points)))
        self.path = points
        return points, originPoint

    def __rotate_zigzag_90(self, zig: list, oriPoint=[0, 0], clockWise=-1, center=[0, 0]):
        """
        rotate zigzag 90 by unclockwise
        :param zig: points set of zigzag
        :param oriPoint: origin point
        :param clockWise: 1 for clockwise,-1 for unclockwise
        :return:
        """
        xSet, ySet, *zSet = zip(*zig)
        xr = []
        yr = []
        ori = [0, 0]
        for i in range(0, len(xSet)):
            xr.append(center[0] + clockWise * (ySet[i] - center[1]))
            yr.append(center[1] + (-1 * clockWise) * (xSet[i] - center[0]))
        # print(xSet)
        pointset = list(zip(xr, yr))
        if not self.holeLocation is None:
            self.holeLocation[0] = center[0] + clockWise * (self.holeLocation[1] - center[1])
            self.holeLocation[1] = center[1] + (-1 * clockWise) * (self.holeLocation[0] - center[0])
        ori[0] = center[0] + clockWise * (oriPoint[1] - center[1])
        ori[1] = center[1] + (-1 * clockWise) * (oriPoint[0] - center[0])
        self.center[0] = center[0] + clockWise * (self.center[1] - center[1])
        self.center[1] = center[1] + (-1 * clockWise) * (self.center[0] - center[0])
        self.path = pointset
        self.originPoint = ori
        return pointset, ori

    def __translate_zigzag(self, zig: list, oriPoint=[0, 0], dx=0, dy=0):
        """
        move zigzag

        :param zig: points set of zigzag
        :param oriPoint: the origin
        :param dx: move along x ward
        :param dy: move along y ward
        :param dz: move along z ward
        :return:
        """
        xSet, ySet, *zSet = zip(*zig)
        xt = []
        yt = []
        ori = [0, 0]
        for i in range(0, len(xSet)):
            xt.append(xSet[i] + dx)
            yt.append(ySet[i] + dy)
        pointset = list(zip(xt, yt))
        if not self.holeLocation is None:
            self.holeLocation[0] = dx + self.holeLocation[0]
            self.holeLocation[1] = dy + self.holeLocation[1]
        ori[0] = oriPoint[0] + dx
        ori[1] = oriPoint[1] + dy
        self.path = pointset
        self.originPoint = ori
        self.center[0] += self.center[0] + dx
        self.center[1] += self.center[1] + dy
        return pointset, ori

    def __symmetry_zigzag(self, zig: list, oriPoint=[0, 0], axis="x"):
        xSet, ySet, *zSet = zip(*zig)
        xs = []
        ys = []
        ori = [0, 0]
        if axis == "x":
            for i in range(0, len(xSet)):
                xs.append(xSet[i])
                ys.append(ySet[i] * -1)
            pointset = list(zip(xs, ys))
            ori[0] = oriPoint[0]
            ori[1] = oriPoint[1] * -1
            self.center[0] = self.center[0]
            self.center[1] = self.center[1] * -1
        if axis == "y":
            for i in range(0, len(xSet)):
                xs.append(xSet[i] * -1)
                ys.append(ySet[i])
            pointset = list(zip(xs, ys))
            ori[0] = oriPoint[0] * -1
            ori[1] = oriPoint[1]
            self.center[1] = self.center[1]
            self.center[0] = self.center[0] * -1
        if axis == "centerx":
            for i in range(0, len(xSet)):
                xs.append(xSet[i])
                ys.append(2 * self.center[1] - ySet[i])
            pointset = list(zip(xs, ys))
            ori[0] = oriPoint[0]
            ori[1] = 2 * self.center[1] - oriPoint[1]
        if axis == "centery":
            for i in range(0, len(xSet)):
                xs.append(2 * self.center[0] - xSet[i])
                ys.append(ySet[i])
            pointset = list(zip(xs, ys))
            ori[0] = 2 * self.center[1] - oriPoint[0]
            ori[1] = oriPoint[1]
        self.path = pointset
        self.originPoint = ori

        return pointset, ori

    def rotate90(self, clockwise=-1, center=[0, 0]):
        self.path, self.originPoint = self.__rotate_zigzag_90(self.path, self.originPoint, clockwise, center)

    def translate(self, dx=0, dy=0):
        self.__translate_zigzag(self.path, self.originPoint, dx, dy)

    def symmetry(self, axis="x"):
        self.__symmetry_zigzag(self.path, self.originPoint, axis)

    def reversed(self):
        self.path.reverse()

    def refreshxyz(self):
        self.x, self.y = zip(*self.path)
        self.set_z(self.zarray[0])
        return self.x, self.y, self.zarray

    def get_path_z(self):
        """
        不推荐使用
        :return:
        """
        self.refreshxyz()
        x, y = zip(*self.path)
        self.set_z(self.zarray[0])
        path_z = list(zip(x, y, self.zarray))
        return path_z

    def set_z(self, z):
        self.zarray = np.full_like(self.x, z)

    def getHoleLocation(self):
        if not self.hole is None:
            return self.holeLocation

    def getDirection(self):
        if self.path[0][0] - self.path[1][0] != 0:
            return "x"
        else:
            return "y"

    def insertHoleByAbsoluteCoordinate(self, hl1: Hole):
        path = self.path
        linenum = hl1.linenum
        hole_point = list(hl1.location)
        direction = self.getDirection()
        # 此处纤维是x方向的
        hl2 = copy.deepcopy(hl1)
        hl1.disturbeByHatchingSpace(hatchingSpace=self.hatching_space_in_real, direction=1)
        hl2.disturbeByHatchingSpace(hatchingSpace=self.hatching_space_in_real, direction=1)
        hl2.rotate90(clockwise=1, center=hl2.location)
        hl2.rotate90(clockwise=1, center=hl2.location)

        if direction == "y":
            hl1.rotate90(clockwise=-1, center=hl1.location)
            hl2.rotate90(clockwise=-1, center=hl2.location)

        # 与方向无关
        def delete_all_line_by_endlist(path, end_pair_list):
            patha = path

            def delete_line_by_end(path, end1, end2):
                begin = min(end1, end2)
                end = max(end1, end2)
                del path[begin + 1:end]
                return path, begin, begin + 1

            new_end_pair_list = []
            for i in range(0, len(end_pair_list)):
                patha, begin, end = delete_line_by_end(patha, end_pair_list[i][0], end_pair_list[i][1])
                new_end_pair_list.append([begin, end])
                number = end_pair_list[i][1] - end_pair_list[i][0] - 1
                for j in range(0, len(end_pair_list)):
                    if end_pair_list[j][0] > begin:
                        end_pair_list[j][0] -= number
                    if end_pair_list[j][1] > begin:
                        end_pair_list[j][1] -= number
            return patha, new_end_pair_list

        # 与方向有关，已处理
        def detect_line_end_by_holelength(path, hole_point, hl1: Hole):
            kdtree = KDTree(data=path)
            distance, index = kdtree.query(hole_point, k=[1])
            index = index[0]
            x0 = 0
            y0 = 0
            if self.getDirection() == "x":
                x0 = hole_point[0]
                y0 = path[index][1]
            if self.getDirection() == "y":
                x0 = path[index][0]
                y0 = hole_point[1]
            end1 = 0
            end2 = 0
            for i_ in range(index, len(path)):
                x = path[i_][0]
                y = path[i_][1]
                dx = x - x0
                dy = y - y0
                d = math.sqrt(dx ** 2 + dy ** 2)
                if d > hl1.length / 2:
                    end1 = i_
                    plt.plot(x, y, c="k", marker="v")
                    break
            for j in range(0, index + 1):
                ij = index - j
                x = path[ij][0]
                y = path[ij][1]
                dx = x - x0
                dy = y - y0
                d = math.sqrt(dx ** 2 + dy ** 2)
                if d > hl1.length / 2:
                    end2 = ij
                    plt.plot(x, y, c="k", marker="^")
                    break

            return min(end1, end2), max(end1, end2), distance[0]

        def detect_all_line_end_by_holelength(path, hole_point, hl1: Hole, fiberward):

            endPairList = []
            if fiberward == "x":
                # 预处理，先靠近上半
                kdtree = KDTree(data=path)
                distance, index = kdtree.query(hole_point, k=[1, 2])
                if path[index[0]][1] < path[index[1]][1]:  # 如果更靠近下半
                    hole_point[1] = hole_point[1] - distance[0] + (2 * hatching_space) / 3
                    hl2.translate(dy=-1 * distance[0])
                    hl1.translate(dy=distance[1])
                if path[index[0]][1] == path[index[1]][1]:  # 如果相等
                    hole_point[1] = hole_point[1] + hatching_space / 3
                    hl2.translate(dy=-1 * distance[0])
                    hl1.translate(dy=distance[1])
                else:
                    hl2.translate(dy=-1 * distance[1])
                    hl1.translate(dy=distance[0])
                # 上半
                for i in range(0, linenum):
                    holePoint = [hole_point[0], hole_point[1] + hatching_space * i]
                    plt.plot(holePoint[0], holePoint[1], marker="+")
                    end1, end2, dis = detect_line_end_by_holelength(path, holePoint, hl1)
                    endPairList.append([end1, end2])
                # 下半
                for i in range(0, linenum):
                    holePoint = [hole_point[0], hole_point[1] - hatching_space / 2 - hatching_space * i]
                    plt.plot(holePoint[0], holePoint[1], marker="+")
                    end1, end2, dis = detect_line_end_by_holelength(path, holePoint, hl1)
                    endPairList.append([end1, end2])
            if fiberward == "y":
                kdtree = KDTree(data=path)
                distance, index = kdtree.query(hole_point, k=[1, 2])
                if path[index[0]][0] >= path[index[1]][0]:  # 如果更靠近右半
                    hole_point[0] = hole_point[0] - distance[0]
                    hl2.translate(dx=distance[0])
                    hl1.translate(dx=-1 * distance[1])
                else:
                    hl2.translate(dx=distance[1])
                    hl1.translate(dx=-1 * distance[0])
                # 左半
                for i in range(0, linenum):
                    holePoint = [hole_point[0] - hatching_space * i, hole_point[1]]
                    end1, end2 = detect_line_end_by_holelength(path, holePoint, hl1)
                    endPairList.append([end1, end2])
                # 右半
                for i in range(0, linenum):
                    holePoint = [hole_point[0] - hatching_space / 2 - hatching_space * i, hole_point[1]]
                    end1, end2 = detect_line_end_by_holelength(path, holePoint, hl1)
                    endPairList.append([end1, end2])
            return endPairList

        # 与方向有关,已处理
        def insert_all_hole_by_two_holes(path, hl1, hl2, end_pair_list):
            def adjust_hole_line_direction(path, hl: Hole, lineindex, endPair):
                ln = hl.fiber[lineindex]
                if direction == "x":
                    # 判断zigzag line方向
                    while (path[endPair[0]][0] - path[endPair[1]][0]) * \
                            (ln.path[0][0] - ln.path[len(ln.path) - 1][0]) < 0:  # 反向
                        ln.path.reverse()
                    dy = path[endPair[0]][1] - ln.path[0][1]
                    ln.startend = endPair[0]
                    hl.translateSingleLine(line=ln, dy=dy)
                if direction == "y":
                    # 判断zigzag line方向
                    while (path[endPair[0]][1] - path[endPair[1]][1]) * \
                            (ln.path[0][1] - ln.path[len(ln.path) - 1][1]) < 0:  # 反向
                        ln.path.reverse()
                    dx = path[endPair[0]][0] - ln.path[0][0]
                    ln.startend = endPair[0]
                    hl.translateSingleLine(line=ln, dx=dx)

            new_path = path
            holefiber = []
            endpairforhl1 = end_pair_list[:linenum]
            endpairforhl2 = end_pair_list[linenum:]
            for i in range(0, len(endpairforhl1)):
                adjust_hole_line_direction(path=path, hl=hl1, lineindex=i, endPair=endpairforhl1[i])
            for i in range(0, len(endpairforhl2)):
                adjust_hole_line_direction(path=path, hl=hl2, lineindex=i, endPair=endpairforhl2[i])
            h1 = []
            h2 = []
            # 比较大小
            for ind in range(0, len(hl1.fiber)):
                h1.append(hl1.fiber[ind].startend)
            for ind in range(0, len(hl2.fiber)):
                h2.append(hl2.fiber[ind].startend)
            h1max = max(h1)
            h2max = max(h2)
            offset = 0
            print(h1max)
            plt.plot(path[1608][0], path[1608][1], c="b", marker="o")
            if h2max > h1max:  # h2大，先从h2开始插入
                while len(h2) != 0:
                    maxe = max(h2)
                    for fiber in hl2.fiber:
                        if maxe == fiber.startend:
                            maxe4 = maxe + offset
                            path[maxe4:maxe4 + 1] = fiber.path
                            h2.remove(maxe)
                while len(h1) != 0:
                    maxe = max(h1)
                    for fiber in hl1.fiber:
                        if maxe == fiber.startend:
                            maxe4 = maxe + offset
                            path[maxe4:maxe4 + 1] = fiber.path
                            h1.remove(maxe)
            if h2max < h1max:  # h2大，先从h2开始插入
                while len(h1) != 0:
                    maxe = max(h1)
                    for fiber in hl1.fiber:
                        if maxe == fiber.startend:
                            maxe4 = maxe + offset
                            path[maxe4:maxe4 + 1] = fiber.path
                            h1.remove(maxe)
                while len(h2) != 0:
                    maxe = max(h2)
                    for fiber in hl2.fiber:
                        if maxe == fiber.startend:
                            maxe4 = maxe + offset
                            path[maxe4:maxe4 + 1] = fiber.path
                            h2.remove(maxe)
            return path

        endpairlist = detect_all_line_end_by_holelength(path, hole_point, hl1, direction)
        path, endpairlist = delete_all_line_by_endlist(path, endpairlist)
        path = insert_all_hole_by_two_holes(path, hl1, hl2, endpairlist)
        return path


if __name__ == '__main__':
    # Parameters
    length = 55  # multiple times of hatching_space ,along-fiber-ward
    width = 55  # vertical fiber ward
    hatching_space = 1
    num = 50
    influ = 6  # Out-of-plane channel
    space = 2  # In-plane channel
    n = 0
    layer_height = 0.25
    jump = 0.5
    shift_distance = 1.5
    evalues = []
    output_file = "Aniso_Gcode_no_holes.gcode"

    fig = plt.figure()
    ax3 = Axes3D(fig)
    all_path = []
    """创建孔对象"""
    # 注意孔的位置不能在纤维上
    hl1 = Hole(r=1, hatchingSpace=hatching_space, ab=2, linenum=6, location=(27.5, 27.5), acc=100, type="half",
               line_type="b",
               lenOfStraight=5)
    hl2 = Hole(r=1, linenum=6, deform_factor=0.8, location=(25.5, 25.5), hatchingSpace=hatching_space, line_type="s_h",
               lenOfStraight=5)
    """创建单层纤维路径对象"""
    path1 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=50, originPoint=(0, 0), z=0)
    # path1.rotate90(clockwise=1, center=path1.center)
    path1.path = path1.insertHoleByAbsoluteCoordinate(hl1)

    # path1.insertHole(hl2)
    # path2 = Zigzag(length=51, width=51, hatching_space=1, num=50, originPoint=(0, 0), z=1, hole=hl1)
    # path3 = Zigzag(length=51, width=51, hatching_space=1, num=50, originPoint=(0, 0), z=2, hole=hl1)

    # path2.insertHole(hl2)
    """进行变换"""
    # path2.symmetry(axis="centery")
    # path2.rotate90(clockwise=-1, center=path2.center)
    # print(path3.getDirection())

    """将单层路径首尾相连"""
    all_path.extend(path1.get_path_z())
    # all_path.extend(path2.get_path_z())
    # all_path.extend(path3.get_path_z())

    x, y, z = zip(*all_path)
    # ax3.plot(*zip(all_path), c="b")
    ax3.plot(x, y, z, c="b", marker="+")

    # hx, hy = path2.hole_Locations[1]
    xx = []
    yy = []
    for i in range(0, len(path1.threePoint)):
        xx.append(path1.threePoint[i][0])
        yy.append(path1.threePoint[i][1])
    ax3.plot(xx, yy, np.full_like(xx, 0), c="y", marker="+")
    # print(path2.originPoint)
    plt.show()
