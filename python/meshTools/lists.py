"""List utilities and CycleList for meshTools.

Provides Maya selection string helpers, grouping, duplicates handling,
and CycleList for cyclic (wrap-around) indexing.
"""

from __future__ import annotations

from copy import copy
from math import modf


def chunk(ulist: list) -> map:
    """Split list into overlapping pairs [ulist[i-1:i+1]].

    Args:
        ulist: Input list.

    Returns:
        Map of overlapping pairs.
    """
    return map(lambda i: ulist[i - 1 : i + 1], range(0, len(ulist), 1))


class Enumeration(object):
    """Simple enum: names 'a|b|c' become attributes a=0, b=1, c=2."""

    def __init__(self, names: str) -> None:
        for number, name in enumerate(names.split("|")):
            setattr(self, name, number)


def toStrList(lst: list) -> str:
    """Convert list to comma-separated string.

    Args:
        lst: Input list.

    Returns:
        Comma-separated string.
    """
    return ", ".join(map(str, lst))


def get_row(lst: list, row: int) -> list:
    """Extract column 'row' from 2D list lst.

    Args:
        lst: 2D list.
        row: Column index.

    Returns:
        Column as list.
    """
    nl = []
    for i in range(len(lst)):
        nl += [lst[i][row]]
    return nl


def sortx(a, b) -> int:
    """Compare by .x; for use with list.sort(cmp).

    Returns:
        -1, 0, or 1.
    """
    if a.x < b.x:
        return -1
    elif a.x > b.x:
        return 1
    else:
        return 0


def sorty(a, b) -> int:
    """Compare by .y; for use with list.sort(cmp).

    Returns:
        -1, 0, or 1.
    """
    if a.y < b.y:
        return -1
    elif a.y > b.y:
        return 1
    else:
        return 0


def sortz(a, b) -> int:
    """Compare by .z; for use with list.sort(cmp).

    Returns:
        -1, 0, or 1.
    """
    if a.z < b.z:
        return -1
    elif a.z > b.z:
        return 1
    else:
        return 0


def to_maya_sel(prefix: str, lst: list[int]) -> list[str]:
    """Convert sorted index list to Maya selection strings.

    Args:
        prefix: Maya component prefix (e.g. 'vtx').
        lst: Sorted list of indices (modified in place).

    Returns:
        List of Maya selection strings (e.g. ['vtx[0:5]', 'vtx[10]']).
    """
    lst.sort()
    nl = [[lst[0]]]
    for i in range(1, len(lst)):
        if nl[-1][-1] + 1 == lst[i]:
            nl[-1] += [lst[i]]
        else:
            nl += [[lst[i]]]
    for i in range(len(nl)):
        if len(nl[i]) > 2:
            nl[i] = [nl[i][0], nl[i][-1]]
    st = []
    for i in range(len(nl)):
        # pPlane1.vtx[3:8]
        if len(nl[i]) == 1:
            st += [prefix + "[" + str(nl[i][0]) + "]"]
        else:
            st += [prefix + "[" + str(nl[i][0]) + ":" + str(nl[i][1]) + "]"]
    # lst=[0,1,4,5,6,7,8,18,12,11,15]
    # print listToMayaSel("Pplane01.vtx",lst)
    # select -r pPlane1.vtx[3:8] pPlane1.vtx[11:16] pPlane1.vtx[20:24] pPlane1.vtx[30:32] pPlane1.vtx[40:41] ;
    return st


def enumerate_list(c: list, offset: int = 0) -> list[int]:
    """Return [offset, offset+1, ..., offset+len(c)-1].

    Args:
        c: Input list (length used).
        offset: Starting value.

    Returns:
        List of sequential integers.
    """
    e = []
    for i in range(len(c)):
        e += [i + offset]
    return e


def enumerate_number(n: int, offset: int = 0) -> list[int]:
    """Return [offset, offset+1, ..., offset+n-1].

    Args:
        n: Count.
        offset: Starting value.

    Returns:
        List of sequential integers.
    """
    e = []
    for i in range(n):
        e += [i + offset]
    return e


def offset(c: list, offset: int = 0) -> list:
    """Add offset to each element of list c.

    Args:
        c: Input list (numbers).
        offset: Value to add.

    Returns:
        New list with offset applied.
    """
    e = []
    for i in range(len(c)):
        e += [c[i] + offset]
    return e


def remove_valuez(lst: list, value) -> list:
    """Remove all occurrences of value from list.

    Note:
        Typo in name preserved for compatibility.

    Args:
        lst: Input list.
        value: Value to remove.

    Returns:
        New list with value removed.
    """
    find = 0
    n = copy(lst)
    while find > -1:
        find = find(n, value)
        if find > -1:
            n.pop(find)
    if not n:
        n = []
    return n


def cycle(lst: list, cycles: int) -> list:
    """Rotate lst left by cycles; first element moves to end.

    Args:
        lst: List to rotate (modified in place).
        cycles: Number of rotations.

    Returns:
        lst (same object, mutated).
    """
    for i in range(0, cycles):
        first_to_last = lst[0]
        lst.pop(0)
        lst.append(first_to_last)
    return lst


def find(lst: list, x) -> int:
    """Return index of first x in lst, or -1 if not found.

    Args:
        lst: Input list.
        x: Value to search for.

    Returns:
        Index or -1.
    """
    i = 0
    while i < len(lst):
        if lst[i] == x:
            return i
        i += 1
    return -1


def group_by_1st(lst: list) -> list:
    """Group rows by first element.

    Args:
        lst: List of rows (each row a list).

    Returns:
        Grouped rows; groups stored as extended lists (e.g. [[a,1],[a,2]] -> [[a,1,2]]).
    """

    def sort_my(a, b):
        if a[0] > b[0]:
            return 1
        elif a[0] == b[0]:
            return 0
        else:
            return -1

    l1 = copy(lst)
    l1.sort(sort_my)
    r = []
    e = l1[0][0]
    r.append(l1[0])
    for i in range(1, len(l1)):
        if e == l1[i][0]:
            r[len(r) - 1].extend(l1[i][1:])
        else:
            e = l1[i][0]
            r.append(l1[i])
    return r


def remove_duplicates(l1: list, l2: list) -> list:
    """Return l1 minus elements also in l2.

    Args:
        l1: Source list.
        l2: Elements to remove.

    Returns:
        New list.
    """
    lt = copy(l1)
    for i in range(0, len(l2)):
        try:
            ind = lt.index(l2[i])
            lt.pop(ind)
        except ValueError:
            pass
    return lt


def leave_duplicates(l1: list, l2: list) -> list:
    """Return elements of l1 that are also in l2.

    Args:
        l1: Source list.
        l2: Elements to match.

    Returns:
        Intersection (order from l1).
    """
    lst = []
    lt = copy(l1)
    for i in range(0, len(l2)):
        try:
            ind = lt.index(l2[i])
            lst.append(lt[ind])
            lt.pop(ind)

        except ValueError:
            pass
    return lst


def group_duplicates(lst: list) -> list:
    """Return lst with duplicates removed.

    Args:
        lst: Input list.

    Returns:
        List with duplicates removed (order of first occurrence preserved).
    """
    l_new = []
    for i in range(len(lst)):
        id = find(l_new, lst[i])
        if id == -1:
            l_new.append(lst[i])
    return l_new


def to_pairs(lst: list) -> list[list]:
    """Convert flat list to pairs: [0,1,2,3] -> [[0,1],[2,3]].

    Args:
        lst: Flat list (length must be even).

    Returns:
        List of pairs.
    """
    nl = []
    for i in range(1, len(lst) // 2 + 1):
        nl.append([lst[i * 2 - 2], lst[i * 2 - 1]])
    return nl


def to_edges(lst: list) -> list[list]:
    """Convert vertex loop to edges: [0,1,2,3] -> [[0,1],[1,2],[2,3],[3,0]].

    Args:
        lst: Vertex indices in loop order.

    Returns:
        List of edge pairs.
    """
    edges = []
    for i in range(len(lst)):
        if i == len(lst) - 1:
            edges += [[lst[i], lst[0]]]
        else:
            edges += [[lst[i], lst[i + 1]]]
    return edges


def duplicates_of(seq: list, item) -> list[int]:
    """Return list of all indices where seq[i] == item.

    Args:
        seq: Sequence to search.
        item: Value to find.

    Returns:
        List of indices.
    """
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


class CycleList:
    """List with cyclic indexing: indices wrap around; negative indices supported."""

    def __init__(self, li: list) -> None:
        self.list = copy(li)

    def __str__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)

    def fixkey(self, key):
        len1 = float(len(self.list))
        nkey = key - modf(key / len1)[1] * len1
        if nkey < 0:
            nkey = len1 + nkey
        return int(nkey)

    def __getitem__(self, key):
        key = self.fixkey(key)
        return self.list[key]

    def __setitem__(self, key, value):
        key = self.fixkey(key)
        self.list[key] = value

    def __add__(self, other):
        self.list += other

    def __sub__(self, other):
        return remove_duplicates(self.list, other)

    def __getslice__(self, i, j):
        i = self.fixkey(i)
        if j < 10e10:
            j = self.fixkey(j)
        if i > j:
            i, j = j, i
        return CycleList(self.list[i:j])

    def find(self, key):
        return find(self.list, key)

    def group(self):
        return CycleList(group_duplicates(self.list))

    def pop(self, key):
        self.list.pop(key)

    def append(self, value):
        self.list.append(value)

    def extract(self, id, value):
        # self.list[id].extract(key)
        pass

    def cycle(self, cycles):
        cycle(self.list, cycles)

    def reverse(self):
        return CycleList(self.list[::-1])
