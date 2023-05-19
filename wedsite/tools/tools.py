from sqlalchemy import Column, Integer , String , Text ,Float , Boolean , DateTime


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False