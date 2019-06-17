from dateutil.parser import parse


def is_date(string):
    """
    Check if string is a date

    Parameters:
    ----------
    string  :  str
        input string to check

    Returns:
    --------
    True/False

    Examples
    --------
    >>>is_date('2019-01-01')
    True
    >>>is_date('foo')
    False
    """
    try:
        parse(string)
        return True
    except ValueError:
        return False
