import re
import xml.etree.ElementTree as ET
import copy
import numpy as np

"""Modul untuk mengkonversi d attribute di file svg ke koordinat kartesius x, y"""


class GetPathAttribute:
    def __init__(self, filename):
        self.filename = filename

    def path_tag(self, root):
        ans = {}

        if "path" in root.tag:
            ans = copy.deepcopy(root.attrib)
        else:
            for childs in root:
                ans = copy.deepcopy(self.path_tag(childs))

        return ans

    def pathAttribKV(self):
        han = ET.parse(self.filename)
        han_root = han.getroot()
        path_attrib = copy.deepcopy(self.path_tag(han_root))
        return path_attrib


class CommandToPath:

    def __init__(self, dattrib):
        self.dattrib = dattrib

    def xyList(self):
        p0 = []

        commands = re.findall("[AaMmCcZzHhVvLlQqSsTt][\\W\\d+.,e]*", self.dattrib)

        if self.dattrib.startswith('M'):
            p0 = self.path_M(commands[0])
        elif self.dattrib.startswith('m'):
            p0 = self.path_m(commands[0])

        xytemp = copy.deepcopy(self.yourPaths(commands, p0))

        xy_list = []
        for val in xytemp.values():
            xy_list += val

        return xy_list

    def strToFloat(self, line):
        lines = line.split(',')
        ttx = float(lines[0])
        tty = float(lines[1])
        return ttx, tty

    def path_M(self, lines):

        xy = []
        if lines.startswith('M'):
            line = lines.split()
            for lin in line:
                if lin == 'M':
                    continue
                else:
                    lin = lin.strip()
                    x, y = self.strToFloat(lin)
                    xy.append([x, y])
                    return xy
        else:
            print("Masukan salah!!!!")
            quit()

    def path_C(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('C'):
            line = lines.split()
            for lin in line:
                if lin == 'C':
                    continue
                else:
                    lin = lin.strip()
                    xn, yn = self.strToFloat(lin)
                    xy.append((xn, yn))
        else:
            print("Masukan salah!!!!")
            quit()

        m = len(xy)
        xys = []
        btx = lambda t, p, p1, p2, p3: ((1-t)**3)*p[0] + 3*((1-t)**2)*t*p1[0] + 3*(1-t)*(t**2)*p2[0] + (t**3)*p3[0]
        bty = lambda t, p, p1, p2, p3: ((1-t)**3)*p[1] + 3*((1-t)**2)*t*p1[1] + 3*(1-t)*(t**2)*p2[1] + (t**3)*p3[1]

        b = p0
        for ik in range(0, (m-2), 3):
            b1 = xy[ik]
            b2 = xy[ik+1]
            b3 = xy[ik+2]

            for tn in np.arange(0.05, 1.05, 0.05):
                x = btx(tn, b, b1, b2, b3)
                y = bty(tn, b, b1, b2, b3)
                xys.append([x, y])

            b = b3

        return xys

    def path_c(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('c'):
            line = lines.split()
            for lin in line:
                if lin == 'c':
                    continue
                else:
                    lin = lin.strip()
                    xn, yn = self.strToFloat(lin)
                    xy.append((xn,yn))
        else:
            print("Masukan salah!!!!")
            quit()

        m = len(xy)
        xys = []
        btx = lambda t, p, p1, p2, p3: ((1-t)**3)*p[0] + 3*((1-t)**2)*t*p1[0] + 3*(1-t)*(t**2)*p2[0] + (t**3)*p3[0]
        bty = lambda t, p, p1, p2, p3: ((1-t)**3)*p[1] + 3*((1-t)**2)*t*p1[1] + 3*(1-t)*(t**2)*p2[1] + (t**3)*p3[1]

        b = p0
        for ik in range(0, (m-2), 3):
            (dx1, dy1) = xy[ik]
            (dx2, dy2) = xy[ik+1]
            (dx3, dy3) = xy[ik+2]

            b1 = ((b[0]+dx1), (b[1]+dy1))
            b2 = ((b[0]+dx2), (b[1]+dy2))
            b3 = ((b[0]+dx3), (b[1]+dy3))

            for tn in np.arange(0.05, 1.05, 0.05):
                x = btx(tn, b, b1, b2, b3)
                y = bty(tn, b, b1, b2, b3)
                xys.append([x, y])

            b = b3

        return xys

    def path_l(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('l'):
            line = lines.split()
            for lin in line:
                if lin == 'l':
                    continue
                else:
                    lin = lin.strip()
                    xn, yn = self.strToFloat(lin)
                    xy.append((xn, yn))
        else:
            print("Masukan salah!!!!")
            quit()

        xys = []
        m = len(xy)

        b = p0
        for i in range(m):
            [dx, dy] = xy[i]
            bt = [(b[0]+dx), (b[1]+dy)]
            xys.append(bt)
            b = bt

        return xys

    def path_L(self, lines):

        xy = []
        if lines.startswith('L'):
            line = lines.split()
            for lin in line:
                if lin == 'L':
                    continue
                else:
                    lin = lin.strip()
                    xn, yn = self.strToFloat(lin)
                    xy.append([xn, yn])
        else:
            print("Masukan salah!!!!")
            quit()

        return xy

    def path_m(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('m'):
            line = lines.split()
            for lin in line:
                if lin == 'm':
                    continue
                else:
                    lin = lin.strip()
                    xn, yn = self.strToFloat(lin)
                    xy.append([xn, yn])
        else:
            print("Masukan salah!!!!")
            quit()

        xys = []
        m = len(xy)

        b = p0
        for i in range(m):
            [dx, dy] = xy[i]

            bt = [(b[0]+dx), (b[1]+dy)]
            xys.append(bt)
            b = bt

        return xys

    def path_h(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('h'):
            line = lines.split()
            for lin in line:
                if lin == 'h':
                    continue
                else:
                    lin = lin.strip()
                    dxn = float(lin)
                    xy.append(dxn)
        else:
            print("Masukan salah!!!!")
            quit()

        m = len(xy)
        xys = []

        b = p0
        for i in range(m):
            bt = [(b[0]+xy[i]), b[1]]
            xys.append(bt)
            b = bt

        return xys

    def path_H(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('H'):
            line = lines.split()
            for lin in line:
                if lin == 'H':
                    continue
                else:
                    lin = lin.strip()
                    xn = float(lin)
                    xy.append(xn)
        else:
            print("Masukan salah!!!!")
            quit()

        m = len(xy)
        xys = []

        b = p0
        for i in range(m):
            bt = [xy[i], b[1]]
            xys.append(bt)
            b = bt

        return xys

    def path_v(self, lines, p0=[0., 0.]):

        xy = []
        if lines.startswith('v'):
            line = lines.split()
            for lin in line:
                if lin == 'v':
                    continue
                else:
                    lin = lin.strip()
                    dyn = float(lin)
                    xy.append(dyn)
        else:
            print("Masukan salah!!!!")
            quit()

        m = len(xy)
        xys = []

        b = p0
        for i in range(m):
            bt = [b[0], (b[1]+xy[i])]
            xys.append(bt)
            b = bt

        return xys

    def yourPaths(self, lines, initp0=[[0., 0.]]):
        N = len(lines)
        j = 0
        points = dict()
        points[0] = initp0.copy()
        for k in range(1, N):
            if lines[k].startswith('M'):
                points[k] = copy.deepcopy(self.path_M(lines[k]))
            elif lines[k].startswith('C'):
                points[k] = copy.deepcopy(self.path_C(lines[k], points[k-1][-1]))
            elif lines[k].startswith('L'):
                points[k] = copy.deepcopy(self.path_L(lines[k]))
            elif lines[k].startswith('H'):
                points[k] = copy.deepcopy(self.path_H(lines[k], points[k-1][-1]))
            elif lines[k].startswith('m'):
                points[k] = copy.deepcopy(self.path_m(lines[k], points[k-1][-1]))
            elif lines[k].startswith('c'):
                points[k] = copy.deepcopy(self.path_c(lines[k], points[k-1][-1]))
            elif lines[k].startswith('l'):
                points[k] = copy.deepcopy(self.path_l(lines[k], points[k-1][-1]))
            elif lines[k].startswith('h'):
                points[k] = copy.deepcopy(self.path_h(lines[k], points[k-1][-1]))
            elif lines[k].startswith('v'):
                points[k] = copy.deepcopy(self.path_v(lines[k], points[k-1][-1]))
            elif lines[k].startswith('z') or lines[k].startswith('Z'):
                points[k] = copy.deepcopy([points[j][0]])
                j = k + 1

        return points


def simpanXYList(fname, xylist=[]):

    with open(fname, 'w') as fo:
        fo.write("Points_list = " + str(xylist))

        fo.close()


attrib = GetPathAttribute("kupu2.svg")
baris = attrib.pathAttribKV()
input("Tekan Enter atau tobol lainnya!!!")
command = CommandToPath(baris['d'])
lines = command.xyList()
input("Tekan Enter atau tobol lainnya!!!")
simpanXYList("kupu2_path.py", lines)