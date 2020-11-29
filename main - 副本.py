import random
import time
import numba as nb
import numpy as np


def get_graph(path):
    g = {}
    f = open(path, 'r')
    f.readline()
    data = f.readlines()
    for i in data:
        i = i.split()
        node = int(i.pop(0)[:-1])
        i = list(map(int, i))
        # print(node[:-1],i)
        g[node] = i
    # print(g)
    return g


def get_random_solution(color_num, city_list):
    c = {}
    city_num = len(city_list)
    random_color_list = [random.randrange(0, color_num) for i in range(city_list[0], city_list[-1] + 1)]
    for i in range(city_num):
        c.setdefault(random_color_list[i], [])
        c[random_color_list[i]].append(city_list[i])
    # print(c)
    return c


def get_one_color_set_conflict1(graph, color_set):  # 检查当前颜色集合中各个城市之间的冲突
    color_size = len(color_set)
    conflict_pairs = []
    count = 0
    for i in range(color_size - 1):
        g_list = graph[color_set[i]]
        # print(g_list)
        # g_list=np.array(g_list)
        # print(g_list)
        for j in range(i + 1, color_size):
            if color_set[j] in g_list:
                conflict_pairs.append([color_set[i], color_set[j]])
                count += 1
                # print(color_set[i],color_set[j])
    return count, conflict_pairs

@nb.njit()
def get_one_color_set_conflict(graph, color_set):  # 检查当前颜色集合中各个城市之间的冲突
    color_size = len(color_set)
    conflict_pairs = []
    count = 0
    for i in range(color_size - 1):
        for j in range(i + 1, color_size):
            if graph[color_set[i], color_set[j]] == 1:
                conflict_pairs.append([color_set[i], color_set[j]])
                count += 1
                # print(color_set[i],color_set[j])
    return count, conflict_pairs


def get_conflict_count(graph, color_solution):  # 对每个颜色解决方案判断冲突
    conflict_pairs = {}
    count = 0
    # print("conflict pairs: ")  #!!!!!
    for i in range(len(color_solution)):
        try:
            t, conflict_pairs[i] = get_one_color_set_conflict(graph, np.array(color_solution[i]))
            count += t
        except KeyError:
            print("随机生成的解没有覆盖所有颜色,重新运行生成随机解！")
            return -1,None
    # print(count,"对冲突：",conflict_pairs) #!!!!!
    return count, conflict_pairs


def get_neighbors(color_solution, conflict_pairs):
    color_num = len(color_solution)
    neighbors_set = []
    count = 0
    for k, v in conflict_pairs.items():
        # print(k,v)
        for i in v:
            other_color_list = [m for m in range(color_num)]
            other_color_list.remove(k)
            for m in other_color_list:
                for j in range(2):
                    # neighbor = copy.deepcopy(color_solution)
                    neighbor = {}
                    for x, y in color_solution.items():
                        neighbor[x] = y[:]
                    neighbor[k].remove(i[j])
                    neighbor[m].append(i[j])
                    # print(neighbor)
                    count += 1
                    neighbors_set.append(neighbor)
    # print(count,neighbors_set)    #!!!!!
    return neighbors_set


def iteration(graph, color_solution):
    current_conflict_num, current_conflict_pairs = get_conflict_count(graph, color_solution)
    if current_conflict_num==-1:
        return -1,{}
    best_num = current_conflict_num
    best_solution = color_solution
    # print("冲突数：", current_conflict_num, "\n当前解：", color_solution, "\n冲突对:", current_conflict_pairs)  #*****
    neighbors = get_neighbors(color_solution, current_conflict_pairs)
    # print("邻居：",neighbors)
    for i in neighbors:
        # print("当前解：",i) #!!!!!
        num, conflict_pairs = get_conflict_count(graph, i)
        if num < best_num or num == 0:
            best_num = num
            best_solution = i
    # print("best: ",best_num,best_solution)    #!!!!!
    return best_num, best_solution


def graph_to_mat(graph):
    city_num = len(graph) + 1
    m = np.zeros((city_num, city_num))
    for k, v in graph.items():
        for i in v:
            m[k, i] = 1

    # print(m[498,:])

    return m


def run(graph, color_num):
    min = 999
    not_change_count = 0
    city_list = list(map(int, list(graph.keys())))
    # color_solution = get_random_solution(color_num, city_list)
    color_solution={
	1: [3, 4, 13, 15, 21, 26, 29, 30, 31, 32, 34, 36, 37, 38, 43, 44, 49, 52, 53, 56, 58, 65, 67, 69, 71, 72, 73, 82, 84, 85, 89, 94, 97, 107, 108, 112, 116, 117, 119, 120, 121, 122, 124, 140, 145, 146, 150, 152, 153, 154, 158, 162, 166, 168, 176, 181, 188, 190, 192, 193, 194, 196, 201, 209, 212, 215, 218, 222, 226, 227, 229, 230, 232, 236, 241, 242, 250, 253, 254, 261, 263, 265, 268, 272, 277, 284, 287, 291, 292, 298, 299, 311, 313, 315, 317, 323, 331, 332, 335, 345, 349, 351, 365, 370, 371, 378, 380, 382, 386, 388, 394, 403, 405, 407, 414, 416, 420, 435, 436, 441, 443, 450, 457, 459, 464, 468, 473, 484, 489, 490, 493, 497, 18, 14, 66, 27, 329, 449, 470, 10, 101, 164, 334, 440, 278, 475, 455, 276, 200, 204, 214, 219, 225, 427, 318, 322, 325, 390, 461, 368, 111, 149, 147, 381],
	2: [7, 9, 20, 23, 33, 35, 39, 41, 47, 50, 51, 55, 74, 76, 77, 79, 81, 88, 93, 99, 102, 103, 105, 123, 127, 129, 136, 137, 138, 141, 142, 148, 151, 160, 171, 180, 182, 184, 185, 191, 195, 197, 199, 208, 213, 216, 223, 235, 238, 240, 244, 247, 251, 252, 256, 258, 269, 270, 271, 275, 281, 282, 285, 286, 289, 290, 295, 297, 302, 303, 304, 309, 310, 312, 327, 336, 338, 339, 341, 348, 354, 363, 379, 383, 389, 392, 393, 395, 401, 402, 404, 408, 409, 419, 421, 424, 426, 431, 434, 438, 439, 445, 446, 447, 448, 451, 453, 460, 465, 466, 469, 472, 474, 477, 481, 483, 485, 486, 488, 491, 495, 496, 499, 0, 169, 45, 186, 170, 224, 91, 257, 163],
	0: [5, 6, 8, 11, 12, 16, 17, 24, 28, 46, 54, 57, 59, 61, 62, 63, 64, 70, 75, 78, 80, 86, 87, 90, 92, 95, 98, 100, 113, 118, 126, 131, 132, 133, 139, 143, 155, 173, 175, 177, 178, 183, 187, 189, 202, 203, 205, 206, 207, 210, 217, 221, 228, 233, 234, 237, 243, 245, 246, 255, 259, 260, 262, 267, 273, 274, 279, 293, 294, 296, 300, 301, 308, 314, 316, 320, 326, 328, 330, 337, 342, 343, 344, 346, 347, 350, 352, 353, 355, 357, 358, 359, 360, 361, 364, 366, 369, 372, 374, 376, 377, 391, 396, 397, 399, 410, 411, 412, 413, 417, 425, 428, 429, 430, 437, 442, 444, 452, 454, 456, 458, 462, 463, 467, 471, 476, 478, 482, 492, 494, 498, 1, 110, 22, 319, 19, 40, 161, 306, 2, 106, 167, 367, 418, 248, 249, 400, 220, 25, 406, 340, 125, 385, 423, 144, 135, 231, 134, 432, 288, 128, 198, 159, 172, 333, 239, 387, 307, 305, 487, 384, 479, 433, 174, 165, 280, 283, 42, 130, 266, 48, 415, 321, 60, 68, 157, 83, 96, 104, 109, 114, 115, 398, 156, 179, 211, 264, 324, 356, 362, 480, 373, 375, 422]
}

    print("random color solution: ", color_solution)

    graph = graph_to_mat(graph)
    for i in range(iter_num):
        # print("当前第", i + 1, "轮，迭代开始：") #******
        conflict_num, color_solution = iteration(graph, color_solution)
        if conflict_num == -1:
            return False
        if conflict_num == 0:
            print("!!!最佳解：", color_solution)
            return True
        if conflict_num < min:
            min = conflict_num
        else:
            not_change_count += 1
        if not_change_count == conflict_num * color_num * 2 + 1:
            print("目前无解，提前结束。")
            return False
    return False


if __name__ == '__main__':
    g = get_graph(r'data.txt')
    iter_num = 200
    color_num = 3
    flag = False
    l1 = []
    # while flag==False:

    for run_count in range(1, 888):
        t1 = time.time()
        flag = run(g, color_num)
        t2 = time.time()
        l1.append(t2 - t1)
        print("第", run_count, "次用时：", l1[run_count - 1])
        print("当前已使用时间：", l1, "总用时：", sum(l1))

        if flag:
            break
        else:
            print("重启，第", run_count + 1, "次启动，重新选择初始解。")
