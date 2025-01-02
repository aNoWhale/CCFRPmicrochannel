from gcodeparser import GcodeParser
import matplotlib.pyplot as plt
import numpy as np


# open gcode file and store contents as variable

def gcode2pointsets(filename, startline=0, endline=10000):
    with open(filename, 'r', encoding='utf-8') as f:
        gcode = f.read()
    line_list = GcodeParser(gcode, include_comments=True).lines  # get parsed gcode lines
    i = 0
    xset = []
    yset = []
    zset = []
    xset.append(0)
    yset.append(0)
    zset.append(0)
    for line in line_list:
        i += 1
        if startline <= i <= endline:
            if line.command_str == "G1":
                if "X" in line.params:
                    xset.append(line.params["X"])
                else:
                    xset.append(xset[len(xset) - 1])
                if "Y" in line.params:
                    yset.append(line.params["Y"])
                else:
                    yset.append(yset[len(yset) - 1])
                if "Z" in line.params:
                    zset.append(line.params["Z"])
                else:
                    zset.append(zset[len(zset) - 1])
    pointset = list(zip(xset, yset, zset))

    del xset[0]
    del yset[0]
    del zset[0]
    return xset, yset


def interpolation(pointset, num):
    leng = len(pointset)
    num = num + 2
    for i in range(1, leng):
        last = len(pointset) - i
        prelast = last - 1
        inter = np.linspace(pointset[prelast], pointset[prelast], num)
        inter = np.delete(inter, num - 1)
        inter = inter.tolist()
        pointset[prelast:last] = inter


if __name__ == "__main__":
    filepath = "tensile_test_sample_05.gcode"
    x, y = gcode2pointsets(filepath, 25, 200)
    interpolation(x, 50)
    interpolation(y, 50)
    fig = plt.figure()
    plt.plot(x, y)
    plt.show()
