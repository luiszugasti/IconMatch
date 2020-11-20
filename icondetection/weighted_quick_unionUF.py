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
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:
            return

        # make smaller root point to larger one
        if self.size[root_p] < self.size[root_q]:
            self.parent[root_p] = (root_q, self.parent[root_p][1])
            self.size[root_q] = self.size[root_q] + self.size[root_p]
        else:
            self.parent[root_q] = (root_p, self.parent[root_q][1])
            self.size[root_p] = self.size[root_p] + self.size[root_q]

        self.count = self.count - 1
        pass

    def get_unions(self):
        """
        Retrieves and returns all groups, according to their parent
        """
        components = {}
        for index_element in range(len(self.parent)):
            # get parent component
            index_parent = self.find(index_element)
            parent = self.parent[index_parent][1]
            child = self.parent[index_element][1]

            # add it to the mapping, or add the current component to its list
            if index_parent not in components:
                if index_element == index_parent:
                    components[index_parent] = [
                        child,
                    ]
                else:
                    components[index_parent] = [
                        parent,
                        child,
                    ]
            else:
                parent_list = components[index_parent]
                parent_list.append(child)
                components[index_parent] = parent_list

        return components
