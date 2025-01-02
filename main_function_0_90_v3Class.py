from path_generation_zigzag_v3class import Zigzag
from path_holeClass import Hole
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# import path_generation_zigzag_v2 as zig
from togcode import *
from matplotlib.widgets import Slider, Button, RadioButtons


def showHoleLocation(hole: Hole, zigzag: Zigzag):
    x = hole.location[0]
    y = hole.location[1]
    z = zigzag.zarray[0]
    s = str("x:" + "%.1f" % x + " y:" + "%.1f" % y)
    plt.plot(x, y, z, c="y", marker="+")


def auto_rotate_zig(zig_begin: Zigzag, zig_end: Zigzag):
    """
    魔法函数，自动调整纤维方向，我也不知道什么原理，就是能用
    :param zig_begin: 前一层
    :param zig_end: 后一层
    :return:
    """
    if zig_begin.hole.line_type == "b" or zig_end.hole.line_type == "b":
        if zig_begin.getDirection() == zig_end.getDirection():
            zig_end.symmetry(axis=str("center" + zig_begin.getDirection()))
            for i in zig_end.hole_list:
                for j in range(0, len(i)):
                    i[j].symmetry(center=zig_end.center, axis=zig_begin.getDirection())
            zig_end.reversed()

    if zig_begin.hole.line_type == "s_h" and zig_end.hole.line_type == "s_h":
        zig_end.reversed()

    while zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]:
        zig_end.rotate90(clockwise=-1, center=zig_end.center)
        for i in zig_end.hole_list:
            for j in range(0, len(i)):
                i[j].rotate90(clockwise=-1, center=zig_end.center)

    if zig_begin.hole.line_type == "s_h" and zig_end.hole.line_type == "s_h":
        if zig_begin.getDirection() != zig_end.getDirection():
            zig_end.rotate90(clockwise=-1, center=zig_end.center)
            for i in zig_end.hole_list:
                for j in range(0, len(i)):
                    i[j].rotate90(clockwise=-1, center=zig_end.center)
        pass

    if zig_begin.hole.line_type == "s_h" and zig_end.hole.line_type == "s_h":
        if zig_begin.getDirection() == zig_end.getDirection():
            time = 0
            while (zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]) and time <= 2:
                time += 1
                zig_end.reversed()
            if time >= 2:
                while zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]:
                    zig_end.rotate90(clockwise=-1, center=zig_end.center)
                    for i in zig_end.hole_list:
                        for j in range(0, len(i)):
                            i[j].rotate90(clockwise=-1, center=zig_end.center)
                while (zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]):
                    zig_end.reversed()
                # if zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]:
                #     zig_end.reversed()
            pass

    if zig_begin.hole.line_type == "b" or zig_end.hole.line_type == "b":
        if zig_begin.getDirection() == zig_end.getDirection():
            zig_end.reversed()
            while zig_begin.path[len(zig_begin.path) - 1] != zig_end.path[0]:
                zig_end.rotate90(clockwise=-1, center=zig_end.center)
                for i in zig_end.hole_list:
                    for j in range(0, len(i)):
                        i[j].rotate90(clockwise=-1, center=zig_end.center)


def auto_rotate_zig_all():
    for i in range(1, len(all_path_list)):
        auto_rotate_zig(all_path_list[i - 1], all_path_list[i])


if __name__ == '__main__':
    """目前用到的参数"""
    # Parameters
    length = 55  # multiple times of hatching_space ,along-fiber-ward
    width = 55  # vertical fiber ward
    hatching_space = 1
    num = 50
    acc = 20  # hole
    ab = 3.5
    wa = 2
    all_path = []  # 整体路径
    all_path_list = []

    """暂时没用到的参数"""
    # influ = 6  # Out-of-plane channel
    # space = 2  # In-plane channel
    # n = 0
    # jump = 0.5
    # shift_distance = 1.5
    # evalues = []
    layer_height = 0.2
    output_file = "speed_"+"ab"+str(ab)+"_wa"+str(wa)+"_Aniso_Gcode_Class.gcode"

    """初始化plt"""
    fig = plt.figure(figsize=(12, 10))
    ax3 = Axes3D(fig)

    # 步骤
    # 1、创建孔对象 linenum需要与r相适应，过少的linenum会使纤维交叠 （path.__findEdge导致的）
    # 2、创建层对象（此时层轨迹中已经含有孔）
    # 3、移动变换调整层对象
    # 4、其他
    """创建孔对象"""
    """r 考虑了 hatchingSpace"""
    """location 是魔法数字，需要看着结果填"""
    # 厚度大概两毫米 10层
    # 大概两三层面内通道，T型+y型
    # T型
    hl1 = Hole(r=1, linenum=7, location=(27.5, 27.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa,
               type="half")
    hl2 = Hole(r=1, linenum=7, lenOfStraight=30, location=(27.5, 27.5), hatchingSpace=hatching_space, ab=ab, acc=acc,
               line_type="s_h", deform_factor=0.8, wa=wa, type="half")
    # # Y型
    # # 厚度通道
    # # 3 4一对 与5 6配合
    hl3 = Hole(r=1, linenum=7, location=(27.5, 12.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa,
               type="half")
    hl4 = Hole(r=1, linenum=7, location=(27.5, 42.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa,
               type="half")
    # 5 6一对
    hl5 = Hole(r=1, linenum=7, location=(12.5, 27.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa,
               type="half")
    hl6 = Hole(r=1, linenum=7, location=(42.5, 27.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa,
               type="half")
    # # 面内通道
    hl7 = Hole(r=1, linenum=7, lenOfStraight=30, location=(27.5, 12.5), hatchingSpace=hatching_space, ab=ab, acc=acc,
               line_type="s_h", deform_factor=0.8, wa=wa, type="half")
    hl8 = Hole(r=1, linenum=7, lenOfStraight=30, location=(27.5, 42.5), hatchingSpace=hatching_space, ab=ab, acc=acc,
               line_type="s_h", deform_factor=0.8, wa=wa, type="half")
    # # 厚度通道
    hl9 = Hole(r=1, linenum=7, location=(12.5, 42.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
               deform_factor=0.8, wa=wa, type="half")
    hl10 = Hole(r=1, linenum=7, location=(42.5, 42.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
                deform_factor=0.8, wa=wa, type="half")
    hl11 = Hole(r=1, linenum=7, location=(12.5, 12.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
                deform_factor=0.8, wa=wa, type="half")
    hl12 = Hole(r=1, linenum=7, location=(42.5, 12.5), hatchingSpace=hatching_space, ab=ab, acc=acc, line_type="b",
                deform_factor=0.8, wa=wa, type="half")
    #
    # hl19 = Hole(r=1, linenum=7, location=(37.5, 10.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl20 = Hole(r=1, linenum=7, location=(11.5, 10.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl21 = Hole(r=1, linenum=7, location=(11.5, 37.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    #
    # hl22 = Hole(r=1, linenum=7, location=(38.5, 37.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl23 = Hole(r=1, linenum=7, location=(38.5, 11.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl24 = Hole(r=1, linenum=7, location=(11.5, 11.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    #
    # hl25 = Hole(r=1, linenum=7, location=(37.5, 38.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl26 = Hole(r=1, linenum=7, location=(11.5, 38.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")
    # hl27 = Hole(r=1, linenum=7, location=(37.5, 11.5), hatchingSpace=hatching_space, ab=2, acc=acc, line_type="b",
    #             deform_factor=0.8, wa=3.5, type="half")

    """创建单层纤维路径对象及插入孔"""
    # 厚度通道
    path1 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=1,
                   hole=hl1)
    path2 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=2,
                   hole=hl1)
    path3 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=3,
                   hole=hl1)
    path4 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=4,
                   hole=hl1)
    path5 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=5,
                   hole=hl1)
    path6 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=6,
                   hole=hl1)
    path7 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=7,
                   hole=hl1)
    path8 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=8,
                   hole=hl1)
    path9 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=9,
                   hole=hl1)
    path10 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=10,
                    hole=hl1)
    # # 面内通道
    path11 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=11,
                    hole=hl2)
    path12 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=12,
                    hole=hl2)
    # # 第二层Y
    # # 厚度通道 4层一周期
    path13 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=13,
                    hole=hl3)
    path13.insertHole(hl4)

    path14 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=14,
                    hole=hl5)
    path14.insertHole(hl6)

    path15 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=15,
                    hole=hl3)
    path15.insertHole(hl4)

    path16 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=16,
                    hole=hl5)
    path16.insertHole(hl6)

    path17 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=17,
                    hole=hl3)
    path17.insertHole(hl4)

    path18 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=18,
                    hole=hl5)
    path18.insertHole(hl6)

    path19 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=19,
                    hole=hl3)
    path19.insertHole(hl4)

    path20 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=20,
                    hole=hl5)
    path20.insertHole(hl6)

    path21 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=21,
                    hole=hl3)
    path21.insertHole(hl4)

    path22 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=22,
                    hole=hl5)
    path22.insertHole(hl6)
    # # 面内通道
    path23 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=23,
                    hole=hl7)
    path23.insertHole(hl8)
    path24 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=24,
                    hole=hl7)
    path24.insertHole(hl8)
    # # 厚度通道
    path25 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=25,
                    hole=hl9)
    path25.insertHole(hl10)
    path25.insertHole(hl11)
    path25.insertHole(hl12)
    path26 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=26,
                    hole=hl9)
    path26.insertHole(hl10)
    path26.insertHole(hl11)
    path26.insertHole(hl12)
    path27 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=27,
                    hole=hl9)
    path27.insertHole(hl10)
    path27.insertHole(hl11)
    path27.insertHole(hl12)
    path28 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=28,
                    hole=hl9)
    path28.insertHole(hl10)
    path28.insertHole(hl11)
    path28.insertHole(hl12)
    path29 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=29,
                    hole=hl9)
    path29.insertHole(hl10)
    path29.insertHole(hl11)
    path29.insertHole(hl12)
    path30 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=30,
                    hole=hl9)
    path30.insertHole(hl10)
    path30.insertHole(hl11)
    path30.insertHole(hl12)
    path31 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=31,
                    hole=hl9)
    path31.insertHole(hl10)
    path31.insertHole(hl11)
    path31.insertHole(hl12)
    path32 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=32,
                    hole=hl9)
    path32.insertHole(hl10)
    path32.insertHole(hl11)
    path32.insertHole(hl12)
    path33 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=33,
                    hole=hl9)
    path33.insertHole(hl10)
    path33.insertHole(hl11)
    path33.insertHole(hl12)
    path34 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=34,
                    hole=hl9)
    path34.insertHole(hl10)
    path34.insertHole(hl11)
    path34.insertHole(hl12)
    path35 = Zigzag(length=length, width=width, hatching_space=hatching_space, num=num, originPoint=(0, 0), z=35,
                    hole=hl9)
    path35.insertHole(hl10)
    path35.insertHole(hl11)
    path35.insertHole(hl12)

    all_path_list.append(path1)
    all_path_list.append(path2)
    all_path_list.append(path3)
    all_path_list.append(path4)
    all_path_list.append(path5)
    all_path_list.append(path6)
    all_path_list.append(path7)
    all_path_list.append(path8)
    all_path_list.append(path9)
    all_path_list.append(path10)
    all_path_list.append(path11)
    all_path_list.append(path12)
    all_path_list.append(path13)
    all_path_list.append(path14)
    all_path_list.append(path15)
    all_path_list.append(path16)
    all_path_list.append(path17)
    all_path_list.append(path18)
    all_path_list.append(path19)
    all_path_list.append(path20)
    all_path_list.append(path21)
    all_path_list.append(path22)
    all_path_list.append(path23)
    all_path_list.append(path24)
    all_path_list.append(path25)
    all_path_list.append(path26)
    all_path_list.append(path27)
    all_path_list.append(path28)
    all_path_list.append(path29)
    all_path_list.append(path30)
    all_path_list.append(path31)
    all_path_list.append(path32)
    all_path_list.append(path33)
    all_path_list.append(path34)
    all_path_list.append(path35)

    """进行变换"""
    auto_rotate_zig_all()
    """将单层路径首尾相连"""
    for index in range(0, len(all_path_list)):
        i = all_path_list[index]
        all_path.extend(i.get_path_z())
    print(len(all_path))
    # xa, ya, za = zip(*path35.get_path_z())
    # ax3.plot(xa, ya, za, c="y")
    """减少数据点"""
    all_path = reduce_points(all_path)
    """gcode"""
    result = points_to_G1(all_path, layer_height=layer_height, speedcontrol=True, minspeed=100,maxspeed=300, brakespace=3)
    # 当layer_height有值时，path的z就是序号 ,speedcontrol=false时，后面参数不好使
    write_gcode_to_file(result, output_file)
    """绘图"""
    x, y, z = zip(*all_path)
    # gcode = zig.output_gcode(all_path)
    # ax3.plot(*zip(all_path), c="b")
    ax3.plot(x, y, z, c="k", alpha=0.5, linewidth=1)

    for i in all_path_list:
        for j in i.hole_list:
            hx, hy = zip(*j[0].fiber[0].path)
            z = i.z
            ax3.plot(hx, hy, z, c="g")
            hx, hy = zip(*j[1].fiber[len(j[1].fiber) - 1].path)
            z = i.z
            ax3.plot(hx, hy, z, c="g")

    # print("path2 hole")
    # print(path2.holeLocation)
    # plt.subplots_adjust(bottom=.25)

    plt.show()
