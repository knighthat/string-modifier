class Rules:
    def __init__(self, other: str, zero: str = '', one: str = '', two: str = '', few: str = '', many: str = ''):
        self._other = other
        self._zero = zero
        self._one = one
        self._two = two
        self._few = few
        self._many = many

    @property
    def other(self) -> str:
        return self._other

    @property
    def zero(self) -> str:
        return self._zero if self._zero else self.other

    @property
    def one(self) -> str:
        return self._one if self._one else self.other

    @property
    def two(self) -> str:
        return self._two if self._two else self.other

    @property
    def few(self) -> str:
        return self._few if self._few else self.other

    @property
    def many(self) -> str:
        return self._many if self._many else self.other
            