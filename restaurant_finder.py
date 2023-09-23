class Node:
    def __init__(self, val):
        self.val = val
        self.ytree = None
        self.ylist = None
        self.left = None
        self.right = None


def binary_search(arr, low, high, x):
    if high >= low:

        mid = (high + low) // 2

        if arr[mid][1] == x:
            return mid

        elif arr[mid][1] > x:
            return binary_search(arr, low, mid - 1, x)

        else:
            return binary_search(arr, mid + 1, high, x)

    else:

        return low


def binary_search2(arr, low, high, x):
    if high >= low:

        mid = (high + low) // 2

        if arr[mid][1] == x:
            return mid

        elif arr[mid][1] > x:
            return binary_search2(arr, low, mid - 1, x)

        else:
            return binary_search2(arr, mid + 1, high, x)

    else:

        return high


def inserty(root, key):
    if root is None:
        return Node(key)
    else:
        if root.val[1] == key[1]:
            return root
        elif root.val[1] < key[1]:
            root.right = inserty(root.right, key)
        else:
            root.left = inserty(root.left, key)
    return root


def merge_sorted_arr(arr1, arr2):
    arr = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i][1] <= arr2[j][1]:
            arr.append(arr1[i])
            i += 1
        else:
            arr.append(arr2[j])
            j += 1
    while i < len(arr1):
        arr.append(arr1[i])
        i += 1
    while j < len(arr2):
        arr.append(arr2[j])
        j += 1
    return arr


def arr_to_bst(arr):
    if arr != []:
        mid = len(arr) // 2
        root = Node(arr[mid])
        root.left = arr_to_bst(arr[:mid])
        root.right = arr_to_bst(arr[mid + 1:])
        return root


def inorder(root, L):
    if root:
        inorder(root.left, L)
        L.append(root.val)
        inorder(root.right, L)


def inorder2(root):
    if root:
        inorder2(root.left)

        print(root.ylist)
        inorder2(root.right)


class PointDatabase:
    def __init__(self, PointList):
        # L3=[[j,i] for i,j in PointList]
        # L3.sort()
        # L2=[[i,j] for j,i in L3]
        PointList.sort()
        self.L1 = [[i, j] for i, j in PointList]

        self.X = self.BuildRangeTree(0, len(self.L1) - 1)
        # print(self.X.val)
        # inorder2(self.X.ytree)
        # print(self.X.ylist)
        # inorder2(self.X)
        # print()
        self.Range = []

    def BuildRangeTree(self, start, end):
        if start == end:
            v = Node(self.L1[start])
            v.ytree = Node(self.L1[start])
            v.ylist = [self.L1[start]]

            return v
        elif start < end:
            # Ty=self.BuildRangeTree1D(start,end)
            mid = (start + end) // 2
            v = Node(self.L1[mid])
            # v.ytree=Ty
            v.left = self.BuildRangeTree(start, mid)
            v.right = self.BuildRangeTree(mid + 1, end)
            arr1, arr2 = [], []
            inorder(v.left.ytree, arr1)
            # # arr1.append(arr1[-1])
            inorder(v.right.ytree, arr2)

            arr = merge_sorted_arr(arr1, arr2)

            v.ytree = arr_to_bst(arr)
            L = []
            v.ylist = list(arr)

            return v

    def left(self, root, q, d):
        if root != None:
            if root.left == None and root.right == None:
                # print(root.val)
                if root.val[0] >= q[0] - d and root.val[1] >= q[1] - d and root.val[1] <= q[1] + d:
                    self.Range.append(root.val)
            else:

                if root.val[0] <= q[0] - d:
                    self.left(root.right, q, d)
                else:
                    if root.right != None:
                        # inorder(root.right)
                        # print()
                        self.query1D(root.right, q, d)
                    self.left(root.left, q, d)

    def right(self, root, q, d):
        if root != None:
            # inorder(root)
            # print()
            if root.left == None and root.right == None:
                if root.val[0] <= q[0] + d and root.val[1] >= q[1] - d and root.val[1] <= q[1] + d:
                    self.Range.append(root.val)
            else:
                if root.val[0] >= q[0] + d:
                    self.right(root.left, q, d)
                else:
                    if root.left != None:
                        self.query1D(root.left, q, d)
                    self.right(root.right, q, d)

    def query(self, root, q, d):
        if root != None:

            if root.val[0] <= q[0] - d:
                self.query(root.right, q, d)
            elif root.val[0] >= q[0] + d:
                self.query(root.left, q, d)
            else:
                # print(self.X.val)
                if root.left == None and root.right == None and root.val[1] >= q[1] - d and root.val[1] <= q[1] + d:
                    self.Range.append(root.val)
                self.left(root.left, q, d)
                self.right(root.right, q, d)

    def query1D(self, root, q, d):
        if root != None:

            if q[1] - d <= root.ylist[-1][1] and q[1] + d >= root.ylist[0][1]:
                l = binary_search(root.ylist, 0, len(root.ylist) - 1, q[1] - d)
                r = binary_search2(root.ylist, 0, len(root.ylist) - 1, q[1] + d)
                for i in root.ylist[l:r + 1]:
                    self.Range.append(i)

    def searchNearby(self, q, d):
        self.Range = []
        if self.L1 == []:
            return []
        i, j = q
        q = [i, j]
        self.query(self.X, q, d)
        return [(i, j) for i, j in self.Range]

# if __name__=="__main__":
#     pointDbObject =  PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])

# x= pointDbObject.searchNearby((4,9), float('inf'))

# print(x)

# (-13538, 140200) 335 [(-13538, 140200), (-13252, 140132)]

