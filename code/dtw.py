import csv
from numpy import array, zeros, argmin, inf, empty, float64, float16
import numpy as np
from numpy.linalg import norm
from collections import deque
from dtw import dtw
from sys import argv, exit
import matplotlib.pyplot as plt


def twoDDW(x, y, dist_func):
    """
    Computes 2-dimensional Dynamic Warping of two images.
    :param 2D-array x: N1*M1 array
    :param 2D-array y: N2*M2 array
    :param func dist: distance used as cost measure
     Returns the minimum distance, the accumulated cost matrix, and the wrap path.
    """
    N1, M1 = x.shape
    N2, M2 = y.shape
    max_value = [N1, M1, N2, M2]
    transpose_x = x.transpose()
    transpose_y = y.transpose()
    cummulative = zeros(max_value)
    order=Calculation_Order(N1, M1, N2, M2)
    for index in range(0,len(order)):
        # if index%1000==0:
        #     print(index)
        i=order[index]
        '''
        cost1 =DTW(R1, R2)+DTW(C1, C2), where R1 is the i1-th row
        in image I1 from column 1 through column i1, C1 is the j1-
        th column in image I2 from row 1 through row j1. 
        '''
        R1 = x[i[0], 0:i[0]]
        if len(R1) == 0:
            R1 = array([0])
        R2 = y[i[2], 0:i[2]]
        if len(R2) == 0:
            R2 = array([0])
        C1 = transpose_x[i[3], 0:i[3]]
        if len(C1) == 0:
            C1 = array([0])
        C2 = transpose_y[i[3], 0:i[3]]
        if len(C2) == 0:
            C2 = array([0])

        dist, cost2, acc, path = dtw(R1.reshape(-1, 1), R2.reshape(-1, 1), dist=dist_func)
        DTW_R1_R2 = dist
        dist, cost2, acc, path = dtw(C1.reshape(-1, 1), C2.reshape(-1, 1), dist=dist_func)
        DTW_C1_C2 = dist
        final_cost = inf
        if isZeros(i):
            final_cost = 0
        else:
            for num in range(15):
                new_stage = prev_stage(i, num)
                cost2 = 0
                prev_prev = prev_stage(new_stage, num)
                if verify_boundaries(prev_prev, max_value):
                    cost2 += cummulative[prev_prev]
                cost2 += cost(DTW_R1_R2, DTW_C1_C2, num)
                if verify_boundaries(new_stage, max_value):
                    if cost2 < final_cost:
                        final_cost = cost2
        cummulative[i[0], i[1], i[2], i[3]] = final_cost
    # print("***************")
    # print(" twoDDW done ")
    # print("***************")
    # print("***************")
    # print(" Traceback started ")
    # print("***************")
    return cummulative[-1, -1, -1, -1] / sum(cummulative.shape), cummulative, local_traceback(cummulative, N1, M1, N2,M2)


def local_traceback(D, N1, M1, N2, M2):
    max_value = (N1, M1, N2, M2)
    current_stage = (N1 - 1, M1 - 1, N2 - 1, M2 - 1)
    best_prev_stage = current_stage
    solution = []
    solution.append(best_prev_stage)
    while not isZeros(current_stage):
        cost = inf
        for num in range(15):
            new_stage = prev_stage(current_stage, num)
            if verify_boundaries(new_stage, max_value) and new_stage != current_stage:
                stage_cost = D[new_stage]
                if stage_cost < cost:
                    cost = stage_cost
                    best_prev_stage = new_stage
        solution.append(best_prev_stage)
        current_stage = best_prev_stage
    return solution


def isZeros(stage):
    if stage[0] == 0 and stage[1] == 0 and stage[2] == 0 and stage[3] == 0:
        return True
    return False


def cost(r1_r2, c1_c2, num):
    if num < 5 or num == 6 or num == 8 or num == 9 or num == 12:
        return r1_r2 + c1_c2
    elif num == 5 or num == 7 or num == 13:
        return r1_r2
    return c1_c2


def prev_stage(stage, num):
    permutations=[(0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)]+[(1, 0, 1, 0), (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1)]+[(1, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 0), (1, 1, 0, 1)]+[(1,1,1,1)]
    ret = [0] * 4
    for i in range(len(stage)):
        ret[i] = stage[i]
    temp = permutations[num]
    for i in range(0,4):
        ret[i]-=temp[i]*1
    return tuple(ret)


def Calculation_Order(N1, M1, N2, M2):
    # print(" ************************* ")
    # print(" Calculating order")
    # print(" ************************* ")
    max_value = (N1, M1, N2, M2)
    # print(max_value)
    Queue = deque()
    Stage_List = deque()
    added_to_queue = set()
    Current_Stage = (N1 - 1, M1 - 1, N2 - 1, M2 - 1)
    Queue.append(Current_Stage)
    while len(Queue) != 0:
        Current_Stage = Queue.pop()
        Stage_List.appendleft(Current_Stage)
        for i in previous_stage(Current_Stage):
            # Verify that the boundaries are inside of both images
            if verify_boundaries(i, max_value):
                if i not in added_to_queue:
                    Queue.append(i)
                    added_to_queue.add(i)
    # print("Number of elements")
    # print(len(Stage_List))
    return Stage_List


def verify_boundaries(stage, max_value):
    for i in range(len(stage)):
        if stage[i] < 0 or stage[i] >= max_value[i]:
            return False
    return True



def previous_stage(stage):
    previous = []
    for i in [-1, 0]:
        for j in [-1, 0]:
            for k in [-1, 0]:
                for l in [-1, 0]:
                    if not (i == 0 and j == 0 and k == 0 and l == 0):
                        previous.append((stage[0] + i, stage[1] + j, stage[2] + k, stage[3] + l))
    return previous


def ddtw(array1, array2):
    warped_array2 = zeros(array1.shape)
    warped_array1 = zeros(array2.shape)
    # plt.imshow(array1)
    # plt.show()
    # plt.imshow(array2)
    # plt.show()
    # plt.close()
    # print("Image 1 size:")
    # print(array1.shape)
    # print("Image 2 size:")
    # print(array2.shape)
    # print("Warped Image 1 size:")
    # print(warped_array1.shape)
    # print("Image 2 size:")
    # print(warped_array2.shape)
    distance, cost,path = twoDDW(array1, array2, dist_func=lambda x, y: norm(x - y, ord=None))
    # print("Distance:")
    # print(distance)
    return distance
