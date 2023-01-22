from src.preprocess import build_transaction_table_and_oneitemset
from src.fp_tree import Tree_node, insert_node
from itertools import combinations # for creating subsets
from src.apriori import rule_generation
from src.utils import timer

def second_elem(List):
    return List[1]

@timer
def fp_growth(input_data, min_sup, min_conf):
    total_transaction = [1]
    transaction_table = {}
    C_1 = {}
    build_transaction_table_and_oneitemset(input_data, transaction_table, C_1, total_transaction)

    # 將sup >= min_sup的item移到L_1，L_1[0]是item，L_1[1]是count，L_1[2]是sup
    L_1 = []
    for item in C_1:
        if C_1[item] / total_transaction[0] >= min_sup:
            L_1.append([item, C_1[item], C_1[item]/total_transaction[0]])
    
    # 依照count排序，並且由大排到小
    L_1.sort(key=second_elem, reverse=True)
    # L_1就可以當做header table
    
    for_sort_purpose = []
    for item in L_1:
        for_sort_purpose.append(item[0])

    # update transaction table
    # 將 < min_sup的item移除，並且每一transaction的item都依照count排序
    new_transaction_tb = {}
    for key in transaction_table:
        item_list = []
        for item in transaction_table[key]:
            is_in_L1 = False
            for L1_item in L_1:
                if item == L1_item[0]:
                    is_in_L1 = True
            if is_in_L1 == True:
                item_list.append(item)
        output = []
        for item in for_sort_purpose:
            if item in item_list:
                output.append(item)
        new_transaction_tb[key] = tuple(output)
    
    # count_table用來記錄某item是否已加入fp_tree
    # count_table是dictionary，key是item，value都初始化成0
    count_table = {}
    for item in L_1:
        count_table[item[0]] = 0

    root = Tree_node('root', None)
    # 建立tree和更新header table(也就是L_1)
    for transaction in new_transaction_tb:
        insert_node(root, new_transaction_tb[transaction], L_1, count_table)

    set_collection = {}
    for sublist in L_1:
        set_collection[sublist[0]] = sublist[1]
        ptr = sublist[3]
        end_item = set()
        end_item.add(ptr.item)
        path_dict = {}
        path_list = []
        while ptr != None:
            path_count = ptr.count
            prefix_path = []
            # index 0存這條path的count
            prefix_path.append(path_count)
            ptr2 = ptr
            while ptr2.item != 'root':
                if ptr2.item != ptr.item:
                    prefix_path.append(ptr2.item)
                    if ptr2.item in path_dict:
                        path_dict[ptr2.item] += path_count
                    else:
                        path_dict[ptr2.item] = path_count 
                ptr2 = ptr2.parent
            path_list.append(prefix_path)
            # print(prefix_path)
            ptr = ptr.next_node
        less_than_sup_item = []
        for k in path_dict:
            if path_dict[k]/total_transaction[0] < min_sup:
                less_than_sup_item.append(k)
        # new_path_list = []
        for sublist in path_list:
            # new_list = []
            new_path = set()
            for i in range(1, len(sublist), 1):
                if sublist[i] not in less_than_sup_item:
                    new_path.add(sublist[i])
            if len(new_path) > 0:
                prefix_path_list = [set(k) for l in range(len(new_path)) for k in combinations(new_path, l+1)]
                for path in prefix_path_list:
                    path = tuple(sorted(path.union(end_item)))
                    if path in set_collection:
                        set_collection[path] += sublist[0]
                    else:   
                        set_collection[path] = sublist[0]
        
    for item in set_collection:
        set_collection[item] = set_collection[item]/total_transaction[0]

    set_meet_min_sup = {}
    for item in set_collection:
        if set_collection[item] >= min_sup:
            set_meet_min_sup[item] = set_collection[item]

    max_len_of_item = 0
    for item in set_meet_min_sup:
        test_int = 1
        if type(test_int) != type(item) and len(item) > 1:
            if len(item) > max_len_of_item:
                max_len_of_item = len(item)

    freq_list = []
    
    for i in range(1, max_len_of_item+1, 1):
        k_itemset = {}
        for item in set_meet_min_sup:
            test_int = 1
            if type(test_int) != type(item):
                if len(item) > 1 and len(item) == i:
                    k_itemset[item] = set_meet_min_sup[item]
            elif i == 1:
                k_itemset[item] = set_meet_min_sup[item]
        freq_list.append(k_itemset)

    rules = []

    rule_generation(freq_list, rules, min_conf)
    
    return rules