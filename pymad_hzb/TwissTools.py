import pandas as pd
from pandas.util.testing import assert_frame_equal


def get_twisscolumns(tfsfile):
    """
    Method to get the of the columns of the twiss file

    Parameters:
    -----------
    tfsfile : str
        Twiss file
    
    Returns:
    --------
    columns : list of str
        list of column names available in the Twiss file
    """
    cols = pd.read_csv(tfsfile, delim_whitespace=True, skiprows=range(45), nrows=2, index_col=None)
    return list(cols.columns[1:].values)


def get_tfsheader(tfsfile):
    """
    Method to get the header part of the Twiss data (e.g. particle energy, mass, etc...)

    Parameters:
    -----------
    tfsfile: str
        Twiss file 

    Returns:
    --------
    headerdata : pandas data frame
        frame containing the header data
    """
    headerdata = pd.read_csv(tfsfile, delim_whitespace=True, nrows=44, index_col=None)
    headerdata.columns = ['AT', 'NAME', 'TYPE', 'VALUE']
    return headerdata[['NAME', 'VALUE']]


def get_twissdata(tfsfile):
    """
    Method to get the table data of the twiss data
    
    Parameters:
    -----------
    tfsfile: str
        Twiss file 

    Returns:
    --------
    data : pandas data frame
        frame containing the Twiss data
    """
    data = pd.read_csv(tfsfile, delim_whitespace=True, skiprows=47, index_col=None, header=None)
    data.columns = get_twisscolumns(tfsfile)
    return data


def get_survey_columns(tfssurveyfile):
    """
    Method to get the headers of the columns of a survey file
    Parameters:
    -----------
    tfsfile: str
        Twiss survey file 

    Returns:
    --------
    columns : list of str
        list containing the Twiss column names
    """
    cols = pd.read_csv(tfssurveyfile, delim_whitespace=True, skiprows=range(6), nrows=2, index_col=None)
    return cols.columns[1:].values


def get_survey_data(tfssurveyfile):
    """
    Method to get the table data of the survey data

    Parameters:
    -----------
    tfsfile: str
        Twiss survey file 

    Returns:
    --------
    data : pandas data frame
        frame containing the Twiss survey data
    """
    data = pd.read_csv(tfssurveyfile, delim_whitespace=True, skiprows=8, index_col=None, header=None)
    data.columns = get_survey_columns(tfssurveyfile)
    return data


def assert_frame_equal_unsorted_rows(left, right, **kwargs):
    """
    Method to compare dataframes in an unsorted way.
    Rows are allowed to be ordered differently in both frames.
    This can be handy when comparing lattices, to check if anything
    changed.

    Parameters:
    -----------
    left: pandas dataframe
    right: pandas dataframe

    Returns:
    --------
    True/False
    """
    left = left.sort_values(by=left.columns.tolist())
    left.reset_index(inplace=True, drop=True)

    right = right.sort_values(by=right.columns.tolist())
    right.reset_index(inplace=True, drop=True)

    assert_frame_equal(left, right, **kwargs)


def assert_frame_equal_unsorted_columns(left, right, **kwargs):
    """
    Method to compare dataframes are equal. Columns
    are allowed to be ordered differently in both frames.
    The index is ignored.

     Parameters:
    -----------
    left: pandas dataframe
    right: pandas dataframe

    Returns:
    --------
    True/False
    """
    left_sorted = left.sort_index(axis=1)
    right_sorted = right.sort_index(axis=1)

    assert_frame_equal(left_sorted, right_sorted, **kwargs)
