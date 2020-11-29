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
            # color_solution_i_t = get_np_array_color_solution()
            t, conflict_pairs[i] = get_one_color_set_conflict(graph, np.array(color_solution[i]))
            count += t
        except KeyError:
            print("随机生成的解没有覆盖所有颜色,重新运行生成随机解！")
            exit(-1)
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


def iteration(graph, color_solution, T):
    current_conflict_num, current_conflict_pairs = get_conflict_count(graph, color_solution)
    best_num = current_conflict_num
    best_solution = color_solution
    # print("冲突数：", current_conflict_num, "\n当前解：", color_solution, "\n冲突对:", current_conflict_pairs)  # *****
    neighbors = get_neighbors(color_solution, current_conflict_pairs)
    # print("邻居：",len(neighbors))
    for i in neighbors:
        # print("当前解：",i) #!!!!!
        num, conflict_pairs = get_conflict_count(graph, i)
        delta = num - best_num
        if delta < 0 or np.exp(-delta / T) > np.random.rand(1):
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
    # min = 999
    # not_change_count = 0
    T = 100
    count = 1
    alpha = 0.98
    city_list = list(map(int, list(graph.keys())))
    color_solution = get_random_solution(color_num, city_list)
    while len(color_solution) < color_num:
        print("随机生成的解没有覆盖所有颜色,重新运行生成随机解！")
        color_solution = get_random_solution(color_num, city_list)

    print("random color solution: ", color_solution)

    graph = graph_to_mat(graph)
    while T > 0.01:
        for i in range(iter_num):
            # print("当前第", i + 1, "轮，迭代开始：")  # ******
            conflict_num, color_solution = iteration(graph, color_solution, T)
            if conflict_num == 0:
                print("!!!最佳解：", color_solution)
                return True
            # if conflict_num < min:
            #     min = conflict_num
            # else:
            #     not_change_count += 1
            # if not_change_count == conflict_num * color_num * 2 + 1:
            #     print("最小冲突数：", min, " 目前无解，提前结束。")
            #     return False
        T = T * alpha
        count += 1
        print("------------第", count, "次降温：", T)
    return False


if __name__ == '__main__':
    g = get_graph(r'data.txt')
    iter_num = 200
    color_num = 3
    flag = False
    l1 = []
    # while flag==False:

    for run_count in range(1, 2):
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
