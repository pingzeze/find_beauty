# 1. 通过reverse()实现反向迭代
# 不通过将需要反向的对象转化为列表，直接使用yield反向输出
class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1


for rr in reversed(Countdown(30)):
    print(rr)
for rr in Countdown(30):
    print(rr)


# 2. 通过yield实现遍历树形结构
# 树形结构root：node0，一级child1：node1；child2：node2，三级结构child3、child4在child1节点下
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value) # 直接print时调用

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)  # root : _children[child1 : _children[]] 在node(0)的_children中加入child1，此时child1的_children为空
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root.depth_first():
        print(ch)
# Outputs Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)


# 3. 大量数据需要处理，返回所有文件中符合条件的行
import os
import fnmatch
import gzip
import bz2
import re
def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):    # 从top节点遍历
        for name in fnmatch.filter(filelist, filepat):  # 筛选符合filepat的文件
            yield os.path.join(path,name)   # 文件路径

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
            yield f
            f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:    # 所有文件作为迭代器
        yield from it       # 每个文件再进行迭代返回，即返回每个行  => for i in it: yield i

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)
    