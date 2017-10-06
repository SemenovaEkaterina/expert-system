PARAMETER_TO_ATTRIBUTE = 1
PARAMETER_TO_PARAMETER = 2
TAB = '    '
LINE = '--------------------------------------'
CHOICE = 0
INPUT = 1
EQ = 3
LT = 4
LQ = 5
GT = 6
GQ = 7
NQ = 8

operations = {
    EQ: lambda x, y: x == y,
    NQ: lambda x, y: x != y,
    LT: lambda x, y: x < y,
    LQ: lambda x, y: x <= y,
    GT: lambda x, y: x > y,
    GQ: lambda x, y: x >= y,
}
