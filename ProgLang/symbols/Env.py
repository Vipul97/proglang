class Env:
    __table = None
    _prev = None

    def __init__(self, n):
        self.__table = {}
        self._prev = n

    def put(self, w, i):
        self.__table[w] = i

    def get(self, w):
        e = self

        while e is not None:
            found = e.__table.get(w)

            if found is not None:
                return found

            e = e._prev

        return None
