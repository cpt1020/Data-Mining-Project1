
class Tree_node:
    def __init__(self, item, parent):
        self.item = item
        # self.support = support
        self.count = 1
        self.child = []
        self.parent = parent
        self.next_node = None
    
    def set_child(self, child):
        self.child.append(child)

    def set_count(self):
        self.count += 1
    
    def set_next_node(self, next_node):
        self.next_node = next_node


# 此item是否是目前ptr所指向的node的child
def is_child(ptr, item):
    for child in ptr.child:
        if child.item == item:
            return True
    return False

def update_header_table(header_table, count_table, item, new_node):
    # 先確認此item是否已經被加入fp_tree
    # 若尚未加入fp_tree
    if count_table[item] == 0:
        # print(f"item {item} is not in tree")
        count_table[item] += 1
        # 找到該item在header_table的位子
        for ele in header_table:
            if ele[0] == item:
                # 將此item的node append到header table此dict的該item的value
                ele.append(new_node)
    # 若已加入fp_tree，我們要設定同item的node的next_node連到new_node
    else:
        # print(f"item {item} is in tree")
        ptr = new_node
        for ele in header_table:
            if ele[0] == item:
                ptr = ele[3]
        while ptr.next_node != None:
            ptr = ptr.next_node
        ptr.next_node = new_node

def insert_node(root, list_of_item, header_table, count_table):
    ptr = root

    for item in list_of_item:
        # 若此item已經是ptr的child
        if is_child(ptr, item) == True:
            # print(f"{item} is child")
            # 先把ptr移到該child
            for child in ptr.child:
                if child.item == item:
                    ptr = child
            # 該child node的count + 1
            ptr.count += 1
        # 若此item不是ptr的child
        else:
            # print(f"{item} is not child")
            # 建立新的node，ptr是parent
            new_node = Tree_node(item, ptr)
            # 加入parent的child中
            ptr.child.append(new_node)
            update_header_table(header_table, count_table, item, new_node)
            ptr = new_node