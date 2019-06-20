import pytest
from unittest.mock import patch, Mock

import os
import datetime

import pymad_hzb
import pymad_hzb.pymadhzb as pm
from  pymad_hzb.pymadhzb import IllegalArgumentError

@pytest.fixture(scope="session")
def maddir(tmpdir_factory):
    path = tmpdir_factory.mktemp('mad')
    return path


@pytest.fixture(scope="session")
def madfile(maddir):
    with open(os.path.join(maddir, 'test.in'), 'w') as f:
        f.write('test\n')
    return os.path.join(maddir, 'test.in')


def test___create_instance_no_valid_madprogram____expectexception():
    with pytest.raises(IllegalArgumentError,
                       match='Given madx executable not found.'):
        madx = pm.Madx('madnot')

def test___create_instance__no_date_given___expect_today_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    assert madx.date == "{:%Y-%m-%d}".format(datetime.date.today())
    assert madx.homedir == maddir
    assert madx.madprogram == 'madx-dev'
    assert madx.madinputfn == 'madin.madx'
    assert madx.madoutputfn == 'madx.out'
    assert madx.output == {'files': []}
    assert madx.freq == 1.25e6
    assert madx.madindir == os.path.join(maddir, madx.date, 'madin')
    assert madx.madoutdir == os.path.join(maddir, madx.date, 'madout')
    assert madx.reportdir == os.path.join(maddir, madx.date, 'report')
    assert madx.twissdir == os.path.join(maddir, madx.date, 'twiss')
    assert madx.plotdir == os.path.join(maddir, madx.date, 'plots')
    assert madx.inputstring == ''

def test___create_instance__date_given___expect_today_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir, date="2017-02-01")
    assert madx.date == "2017-02-01"
    assert madx.homedir == maddir


def test___update_output__add_to_list___expectpass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('files', 'test')
    assert madx.output == {'files': ['test']}


def test___update_output__add_dict____expectpass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('dc', {'test': 0})
    assert madx.output == {'files': [], 'dc': {'test': 0}}


def test___update_output__update_dict____expectpass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('dc', {'test': 0})
    assert madx.output == {'files': [], 'dc': {'test': 0}}
    madx.updateoutput('dc', {'test1': 1})
    assert madx.output == {'files': [], 'dc': {'test': 0, 'test1': 1}}


def test___update_output__add_item___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('foo', 'bar')
    assert madx.output == {'files': [], 'foo': 'bar'}


def test___update_output__update_single_value_to_list___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('foo', 'bar')
    assert madx.output == {'files': [], 'foo': 'bar'}
    madx.updateoutput('foo', 'bar2')
    assert madx.output == {'files': [], 'foo': ['bar2', 'bar']}


def test___clear_output___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.updateoutput('foo', 'bar')
    assert madx.output == {'files': [], 'foo': 'bar'}
    madx.clearoutput()
    assert madx.output == {'files': []}


def test___load_file__file_exists__expect_pass(maddir, madfile):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.loadfile(madfile)
    assert madx.output == {'files': [madfile]}

    with open(madfile, 'r') as f:
        teststr = f.read()

    assert madx.inputstring == teststr


def test___load_file__file_does_no_exist__expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)

    with pytest.raises(FileNotFoundError):
        madx.loadfile('abc')


def test___add_string_input___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.add_string_input("boe")
    assert madx.inputstring == "boe\n"


def test___clearinput___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.add_string_input("boe")
    assert madx.inputstring == "boe\n"
    madx.clearinput()
    assert madx.inputstring == ''


def test___set_value___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.set_value({'R1QS1->K1': 42})
    assert madx.inputstring == "R1QS1->K1=42;\n"


def test___set_expression___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.set_expression({'FOO': 'BAR'})
    assert madx.inputstring == "FOO:=BAR;\n"


def test___call__file_exists___expect_pass(maddir, madfile):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.call(madfile)
    assert madx.output == {'files': [madfile]}
    assert madx.inputstring == 'call, file = \'{}\';\n'.format(madfile)


def test___call__file_does_not_exist___expect_exception(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    with pytest.raises(FileNotFoundError):
        madx.call('boe')


def test___beam___particle____expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.beam(particle='electron')
    assert madx.inputstring == "beam, particle = electron;\n"


def test___beam___particle_energy____expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.beam(particle='electron', energy=1.7)
    assert madx.inputstring == "beam, particle = electron, energy = 1.7;\n"


def test___use___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.use('ring')
    assert madx.inputstring == 'USE, PERIOD={};\n'.format('ring')


def test___twiss___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.twiss(file='test')
    assert madx.inputstring == 'TWISS, file = test;\n'
    assert madx.output == {'files': [], 'statustwiss': 'prepared', 'twiss': 'test'}


def test___twiss__file_kwarg_missing___expect_exception(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    with pytest.raises(IllegalArgumentError, match='`file` missing in kwargs.'):
        madx.twiss()


def test___Twiss___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.Twiss(sequence='ring', file='test')
    assert madx.inputstring == "SELECT, FLAG=TWISS, ;\n" \
                               "USE, PERIOD=ring;\n" \
                               "TWISS, SEQUENCE = ring, file = " \
                               "'test';\n"


def test___Twiss__no_seq___expect_exception(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    with pytest.raises(IllegalArgumentError,
                       match='Missing argument, sequence needed.'):
        madx.Twiss()


def test___Twiss__clear___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.Twiss('clear', sequence='ring', file='test')
    assert madx.inputstring == "SELECT, FLAG=TWISS, clear;\n" \
                               "USE, PERIOD=ring;\n" \
                               "TWISS, SEQUENCE = ring, file = " \
                               "'test';\n"


def test___Twiss__columns___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.Twiss(column=['BETX', 'BETY'],
               sequence='ring', file='test')
    assert madx.inputstring == "SELECT, FLAG=TWISS, column = {BETX,BETY}, ;\n" \
                               "USE, PERIOD=ring;\n" \
                               "TWISS, SEQUENCE = ring, file = " \
                               "'test';\n"


@patch.object(pymad_hzb.pymadhzb, 'datetime', Mock(wraps=datetime.datetime))
def test___Twiss__no_gile___expect_pass(maddir):
    pymad_hzb.pymadhzb.datetime.now.return_value = datetime.datetime(2000, 1, 1, 0, 0, 0)
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.Twiss(sequence='ring')

    dir = os.path.join(maddir,
                       "2000-01-01",
                       'twiss2000-01-01-00-00-00-twiss.tfs')
    assert madx.inputstring == "SELECT, FLAG=TWISS, ;\n" \
                               "USE, PERIOD=ring;\n" \
                               "TWISS, SEQUENCE = ring, file = " \
                               "'{}';\n".format(dir)


def test___Twiss__table___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.Twiss(column=['BETX', 'BETY'],
               sequence='ring', file='test', table='tab')
    assert madx.inputstring == "SELECT, FLAG=TWISS, column = {BETX,BETY}, ;\n" \
                               "USE, PERIOD=ring;\n" \
                               "TWISS, SEQUENCE = ring, file = " \
                               "'test', table=tab;\n"
    assert madx.output == {'files': [], 'statustwiss': 'prepared', 'twiss': 'test'}


@patch.object(pymad_hzb.pymadhzb, 'datetime', Mock(wraps=datetime.datetime))
def test___survey___expect_pass(maddir):
    pymad_hzb.pymadhzb.datetime.now.return_value = datetime.datetime(2000, 1, 1, 0, 0, 0)
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.survey(sequence='ringbii')
    print(madx.inputstring)
    dir = os.path.join(maddir, "2000-01-01/twiss2000-01-01-00-00-00-survey.tfs")
    assert madx.inputstring == "USE, SEQUENCE=ringbii;\n" \
                               "SURVEY,FILE='{}';\n".format(dir)


def test___survey_no_seq___expect_exception(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    with pytest.raises(IllegalArgumentError,
                       match='Missing argument, sequence and file needed.'):
        madx.survey()


def test___install_element___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    str_coupler_definition_ref = 'vsrcouplerkickhor1: hkicker,kick:= 0;'
    madx.add_string_input(str_coupler_definition_ref)
    madx.installElement('RINGBII', 'vsrcouplerkickhor1', 45.00 - 1.479)

    assert madx.inputstring == "vsrcouplerkickhor1: hkicker,kick:= 0;\n" \
                               "USE, period = RINGBII;\n" \
                               "SEQEDIT, SEQUENCE = RINGBII;\n" \
                               "FLATTEN;\n" \
                               "INSTALL, ELEMENT = vsrcouplerkickhor1, AT =  43.521000;\n" \
                               "FLATTEN;\n" \
                               "ENDEDIT;\n"


def test___install_element_missing___expect_exception(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    with pytest.raises(TypeError):
        madx.installElement()


def test___slice___expect_pass(maddir):
    madx = pm.Madx('madx-dev', maddir=maddir)
    madx.slice('ring',quadrupole=10)
    print(madx.inputstring)
    assert madx.inputstring == "USE, SEQUENCE=ring;\n" \
                               "SELECT, FLAG=MAKETHIN, class=quadrupole , SLICE=10;\n" \
                               "MAKETHIN, SEQUENCE=ring, style=SIMPLE, MAKEDIPEDGE=false;\n"
