
def convertStr(s: str):
    '''
    Преобразование строки в число
    '''
    try:
        ret = int(s)
    except ValueError:
        return 0, 0
    return 1, ret


if __name__ == '__main__':
    pass