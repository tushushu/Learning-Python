"""
Created on Wed Apr 12 21:57:50 2017

@author: tushushu
"""

class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0


class AVLTree(object):
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def update_height(self, node):
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def unbalance(self, node):
        return abs(self.height(node.left) - self.height(node.right)) is 2

    """右旋处理LL"""
    def right_rotate(self, node):
        node_right = node
        node = node.left
        node_right.left = node.right
        node.right = node_right
        
        self.update_height(node_right)
        self.update_height(node)
        
        return node

    """左旋处理RR"""
    def left_rotate(self, node):
        node_left = node
        node = node.right
        node_left.right = node.left
        node.left = node_left
        
        self.update_height(node_left)
        self.update_height(node)
        
        return node

    """双向旋转（先左后右）平衡处理LR"""
    def left_right_rotate(self, node):
        node.left = self.left_rotate(node.left)
        return self.right_rotate(node)

    """双向旋转（先右后左）平衡处理RL"""
    def right_left_rotate(self, node):
        node.right = self.right_rotate(node.right)
        return self.left_rotate(node)

    """插入元素"""
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self.root = self._insert(key, self.root)
            
    def _insert(self, key, node):
        if node is None:
            node = Node(key)

        elif key < node.key: #左侧插入结点
            node.left = self._insert(key, node.left)
            if self.unbalance(node): #不平衡
                if key < node.left.key: #LL不平衡
                    node = self.right_rotate(node) #右旋
                else: #LR不平衡
                    node = self.left_right_rotate(node) #先左旋再右旋
             
        elif key > node.key: #右侧插入结点
            node.right = self._insert(key, node.right)
            if self.unbalance(node): #不平衡
                if key < node.right.key: #LR不平衡
                    node = self.right_left_rotate(node) #先右旋再左旋
                else: #RR不平衡
                    node = self.left_rotate(node) #左旋

        self.update_height(node)
        
        return node

"""测试"""
Array = map(int,"6 4 7 3 5 1 2".split())
Tree = AVLTree()
for i in Array:
    Tree.insert(i)
    print(Tree.root.key)