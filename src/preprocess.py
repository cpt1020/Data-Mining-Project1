
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