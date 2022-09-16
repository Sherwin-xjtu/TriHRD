#!/usr/bin/python
# coding=utf-8
# *****************对label进行编码********************************
import copy
import math
import itertools
from sklearn import preprocessing
import numpy as np

# lon和lat分别是要插值的点的x,y
# lst是已有数据的数组，结构为：[[x1，y1，z1]，[x2，y2，z2]，...]
# 返回值是插值点的高程

class InverseDistanceWeight:

    def __init__(self):
        pass

    # 计算两点间的距离
    def distance(self, p, pi):
        dis = (p[0] - pi[0]) * (p[0] - pi[0]) + (p[1] - pi[1]) * (p[1] - pi[1])
        m_result = math.sqrt(dis)
        return m_result
    def interpolation(self, CP, lst, P):

        p0 = CP
        lon = CP[0]
        lat = CP[1]
        sum0 = 0
        sum1 = 0
        temp = []
        # 遍历获取该点距离所有采样点的距离
        for point in lst:
            if lon == point[0] and lat == point[1]:
                return point[2]
            Di = self.distance(p0, point)
            # new出来一个对象，不然会改变原来lst的值
            ptn = copy.deepcopy(point)
            ptn = ptn.tolist()
            ptn.append(Di)
            temp.append(ptn)

        # 根据上面ptn.append（）的值由小到大排序
        temp1 = sorted(temp, key=lambda point: point[3])
        # 遍历排序的前15个点，根据公式求出sum0 and sum1

        for point in temp1:
            sum0 += 100*point[2] / math.pow(point[3], P)
            sum1 += 1 / math.pow(point[3], P)
        return sum0 / sum1


    def bit_product_sum(self, x, y):
        return sum([item[0] * item[1] for item in zip(x, y)])

    def cosine_similarity(self, x, y, norm=True):
        """ 计算两个向量x和y的余弦相似度 """

        assert len(x) == len(y), "len(x) != len(y)"
        zero_list = [0] * len(x)

        if x == zero_list or y == zero_list:
            return float(1) if x == y else float(0)

        # method 1
        res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
        cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

        # method 2
        # cos = bit_product_sum(x, y) / (np.sqrt(bit_product_sum(x, x)) * np.sqrt(bit_product_sum(y, y)))

        # method 3
        # dot_product, square_sum_x, square_sum_y = 0, 0, 0
        # for i in range(len(x)):
        #     dot_product += x[i] * y[i]
        #     square_sum_x += x[i] * x[i]
        #     square_sum_y += y[i] * y[i]
        # cos = dot_product / (np.sqrt(square_sum_x) * np.sqrt(square_sum_y))

        return cos
        # return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内
    def EuclideanDistance(self,x,y):
        sum = 0
        for i in range(len(x)):
            if i ==2:
                sum = sum + np.square((x[i] - y[i]))
            else:
                sum = sum + np.square(x[i] - y[i])
        return np.sqrt(sum)

    def main(self,ls,CandidatePoint,P):

        ls.append(CandidatePoint)

        X = np.array(ls)
        X_ = X[:,:-1]
        min_max_scaler = preprocessing.MinMaxScaler()
        X_minMax = min_max_scaler.fit_transform(X_)

        b = X[:,2:]
        b = map(list, zip(*b))
        d = np.insert(X_minMax, 2, values=b, axis=1)
        CP = d[-1]
        # print CP[:-1],d[:-1]

        EstimatedValue = self.interpolation(CP[:-1], d[:-1], P)

        tt = CP.tolist()
        EV = copy.deepcopy(CP[:-1])
        EV = EV.tolist()
        EV.append(EstimatedValue)
        result = self.cosine_similarity(EV, tt)
        result = self.EuclideanDistance(EV, tt)
        print tt,EV,result
        # print tt,EV,result


if __name__ == '__main__':
    ls = [[0.7, 0.3, 0.497000008821], [0.8, 0.4, 0.532000005245], [0.5, 0.2, 0.321000009775],
          [0.4, 0.7, 0.418000012636]]
    X = np.array(ls)

    #
    # CandidatePoint = [0.6, 0.8, 0.43]
    # P = 2
    # IDW = InverseDistanceWeight()
    # IDW.main(ls,CandidatePoint,P)
