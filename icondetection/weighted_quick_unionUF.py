class WeightedQuickUnionUF:
    """
    Weighted Quick Union UF is a Python conversion of the algorithm as '
    implemented by Kevin Wayne and Robert Sedgewick for their Algorithms 1
    course on Coursera.

    https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/WeightedQuickUnionUF.html
    """

    def __init__(self, n: int, entries):
        """
        Initializes an empty union–find data structure with n sites
        0 through n-1. Each site is initially in its own
        component.

        Within the parent list, each entry is a tuple that contains the "parent"
        index, as well as the object holding that specific entry (generic)
        """
        self.parent = [None] * n
        self.size = [1] * n
        self.count = n
        for i in range(n):
            self.parent[i] = (i, entries[i])

    def count(self):
        """
        Returns the number of components.
        """
        return self.count

    def find(self, p: int):
        """
        Returns the component identifier for the component containing site p.
        """
        self._validate(p)
        while p != self.parent[p][0]:
            # path compression (make every other node in path point to its grandparent)
            self.parent[p] = (self.parent[self.parent[p][0]][0], self.parent[p][1])

            p = self.parent[p][0]

        return p

    def _validate(self, p: int):
        """
        Validate that p is a valid index
        """
        n = len(self.parent)
        if p is None or p < 0 or p >= n:
            raise ValueError("index {0} is not between 0 and {1}".format(p, n - 1))

    def connected(self, p: int, q: int):
        """
        Returns true if the the two sites are in the same component.
        """
        return self.find(p) == self.find(q)
        pass

    def union(self, p: int, q: int):
        """
        Merges the component containing site p with the
        the component containing site q.
        """
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return

        # make smaller root point to larger one
        if self.size[rootP] < self.size[rootQ]:
            self.parent[rootP] = (rootQ, self.parent[rootP][1])
            self.size[rootQ] = self.size[rootQ] + self.size[rootP]
        else:
            self.parent[rootQ] = (rootP, self.parent[rootQ][1])
            self.size[rootP] = self.size[rootP] + self.size[rootQ]

        self.count = self.count - 1
        pass


if __name__ == "__main__":
    n = int(input("Enter size"))
    uf = WeightedQuickUnionUF(n)
    while True:
        p = int(input("enter a p"))
        q = int(input("enter a q"))
        if uf.connected(p, q):
            continue
        uf.union(p, q)
