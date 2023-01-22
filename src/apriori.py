from itertools import combinations # for creating subsets
from src.utils import timer

def build_transaction_table_and_oneitemset(input_data, transaction_table, one_itemset, total_transaction):
    for list in input_data:
        # list[0], list[1]都是transaction ID
        # list[2]才是item
        # 建立transaction table
        if list[0] in transaction_table:
            transaction_table[list[0]].add(list[2])
        else:
            item = set()
            item = {list[2]}
            transaction_table[list[0]] = item
        # 建立C_1
        if list[2] in one_itemset:
            one_itemset[list[2]] += 1
        else:
            item = (list[2])
            one_itemset[item] = 1
        total_transaction[0] = list[0]

def subset_test(Ck, L_k_minus_one):
    pruned_Ck = {}
    for item in Ck:
        not_in = False
        temp_list = list(item)
        for elem in temp_list:
            elem_set = {elem}
            temp = set()
            subset = temp.union(set(item).difference(elem_set))
            subset = tuple(sorted(subset))
            if subset not in L_k_minus_one:
                not_in = True
        if not_in == False:
            pruned_Ck[item] = Ck[item]
    return pruned_Ck

def create_C_k(L_k_minus_one_itemset, transaction_table, total_transaction):
    # create C_k
    k_itemset = {}
    for item1 in L_k_minus_one_itemset:
        for item2 in L_k_minus_one_itemset:
            set1 = set(item1)
            set2 = set(item2)
            set3 = set1.union(set2)
            # 檢查不可同item互相聯集，以及確認兩個L_{k-1}交集的個數等於k-2=1
            # if len(set1.intersection(set2)) == 1:
            if len(set3) == len(set1)+1:
                k_itemset[tuple(sorted(set3))] = 0

    # perfor subset test
    k_itemset = subset_test(k_itemset, L_k_minus_one_itemset)

    # calculate C_k count
    for item in k_itemset:
        temp_set = set(item)
        count = 0
        for transaction in transaction_table:
            if temp_set in transaction_table[transaction] or temp_set.issubset(transaction_table[transaction]):
                count += 1
        k_itemset[item] = count
    
    #calculate C_k support
    for item in k_itemset:
        k_itemset[item] = k_itemset[item] / total_transaction[0]

    return k_itemset

def create_L_k(C_k, min_sup):
    L_k = {}
    for item in C_k:
        if C_k[item] >= min_sup:
            L_k[item] = C_k[item]
    return L_k

def rule_generation(freq_itemset, rules, min_conf):
    for i in range(len(freq_itemset)-1, -1, -1):
        # 從大的freq itemset開始找

        for dict in freq_itemset[i]:
            # freq_itemset[i]是一個L_k
            # dict is a dictionary, which contains L_k
            # key is tuple, and value is support
            test_int = 1
            # 由於當dict到達L_1的時候，key會變成integer，而不是tuple，會造成用tuple找dictionary出問題
            # 所以用test_int來比較type()是否一樣
            if (type(dict) == type(test_int)):
                # 到了L_1
                set_size = 1
                itemset = set()
                itemset.add(dict)
            else:
                # 非L_1
                set_size = len(dict) # how many items in the tuple
                itemset = set(dict)
            itemset_sup = freq_itemset[i][dict]
            # 把support先抓出來
            subset_list = [set(k) for l in range(set_size) for k in combinations(itemset, l+1)]
            # 先產出所有的subset，並存入list
            # print(f"subset_list: {subset_list}")
            for j in subset_list:
                subset_size = len(j)
                if subset_size == 1:
                    elem = j.pop()
                    j.add(elem)
                    # print(f"elem: {elem}")
                    subset_sup = freq_itemset[subset_size-1][elem]
                    # print(f"subset_sup: {subset_sup}")
                else:
                    elem_set = j
                    subset_tup = tuple(sorted(elem_set))
                    subset_sup = freq_itemset[subset_size-1][subset_tup]                    
                
                # print(f"dict: {dict}, j: {j}")
                
                if round(itemset_sup/subset_sup, 10) >= min_conf:
                    output = []
                    diff_set = itemset.difference(j)
                    empty_set = set()
                    if j == empty_set or diff_set == empty_set:
                        continue
                    else:
                        antecedent = str(j)
                        antecedent = antecedent.replace(",","")
                        consequent = str(diff_set)
                        consequent = consequent.replace(",","")
                        # result = str(j) + " -> " + str(diff_set)
                        # output.append(result)
                        output.append(antecedent)
                        output.append(consequent)
                        confidence = itemset_sup/subset_sup
                        if len(diff_set) == 1:
                            elem = diff_set.pop()
                            diff_set.add(elem)
                            diff_set_sup = freq_itemset[0][elem]
                        else:
                            diff_set_tup = tuple(sorted(diff_set))
                            diff_set_sup = freq_itemset[len(diff_set)-1][diff_set_tup]
                        lift = confidence/diff_set_sup
                        # itemset_sup = round(itemset_sup, 3)
                        # confidence = round(confidence, 3)
                        # lift = round(lift, 3)
                        output.append(round(itemset_sup, 3))
                        output.append(round(confidence, 3))
                        output.append(round(lift, 3))
                        rules.append(output)
                
@timer
def apriori(input_data, min_sup, min_conf):
    
    # 總共有多少筆transaction
    total_transaction = [1]
    # 必須要改成list形式，才能從function直接更改這個值

    transaction_table = {}
    # transaction_table is a dictionary
    # key is transaction ID
    # value is a set that contains items
    one_itemset = {}
    # one_itemset is a dictionary
    # key is itemset, its DS is tuple
    # value is support

    # Build transaction table & 1-itemset
    build_transaction_table_and_oneitemset(input_data, transaction_table, one_itemset, total_transaction)
    # print(f"input data: \n{input_data}")
    # print(f"transaction table: \n{transaction_table}")
    # print(f"One-itemset: \n{one_itemset}")

    freq_itemset = []
    # For collecting freq_itemset
    # each element is a dictionary of L_k
    # index i contains dictionary of L_{i+1}

    # calculate support
    for item in one_itemset:
        one_itemset[item] /= total_transaction[0]

    # 保留support >= min_sup的item，建立L_1
    list1 = []
    list2 = []
    for k,v in one_itemset.items():
        if v >= min_sup:
            list1.append(k)
            list2.append(v)
    one_itemset = dict(zip(list1, list2))
    freq_itemset.append(one_itemset)

    # Join step (建立C_2)
    two_itemset = {}
    for item1 in one_itemset:
        for item2 in one_itemset:
            set1 = {item1}
            set2 = {item2}
            set3 = set1.union(set2)
            # 檢查不可同item互相聯集，以及確認兩個L_{k-1}交集的個數等於k-2
            if len(set3) == len(set1)+1:
                two_itemset[tuple(sorted(set3))] = 1
    
    # calculate C_2 count
    for item in two_itemset:
        temp_set = set(item)
        count = 0
        for transaction in transaction_table:
            if temp_set in transaction_table[transaction] or temp_set.issubset(transaction_table[transaction]):
                count += 1
        two_itemset[item] = count

    #calculate C_2 support
    for item in two_itemset:
        two_itemset[item] = two_itemset[item] / total_transaction[0]
                
    #保留support >= min_sup的item，建立L_2
    list1 = []
    list2 = []
    for k,v in two_itemset.items():
        if v >= min_sup:
            list1.append(k)
            list2.append(v)
    two_itemset = dict(zip(list1, list2))

    freq_itemset.append(two_itemset)

    # create C_3
    C_k = create_C_k(two_itemset, transaction_table, total_transaction)

    while len(C_k) > 0:
        L_k = create_L_k(C_k, min_sup)
        freq_itemset.append(L_k)
        C_k = create_C_k(L_k, transaction_table, total_transaction)

    rules = []
    # rules collect each rule generated from freq_itemset
    # each element of rules is a list, which contains the rule (string), support, confidence, and lift

    rule_generation(freq_itemset, rules, min_conf)

    # print result
    # print(f"frequent k-itemset number: {len(freq_itemset)}")
    # total_freq_itemset_num = 0
    # for item in freq_itemset:
    #     total_freq_itemset_num += len(item)
        # print(len(item))
    # print(f"Total frequent itemset number: {total_freq_itemset_num}")
    # print(f"Number of rules generated: {len(rules)}")

    return rules