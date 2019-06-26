import os
import subprocess
from datetime import datetime
import logging

from os.path import expanduser

from .DateTools import is_date


# ref : https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def is_tool(name):
    """
    Check if name `name` is on PATH
    and marked as executable.

    Parameters:
    -----------
    name : str
        file/app/execution file

    Returns:
        -------
    rue/False

    """
    from shutil import which

    return which(name) is not None


logger = logging.getLogger(__name__)


class IllegalArgumentError(ValueError):
    """
    Error raised when invalid argument is provided
    """
    pass


class Madx:
    """
    Class to run madx from within python and access Twiss and Tracking results
    """

    def __init__(self, madprogram, maddir=expanduser("~") + '/mad/',
                 date=None):
        """
        Initialize instance variables.

        Parameters:
            madprogram: str
                madx excecutable (needs to be system wide accessible)
            maddir : str
                directory where a directory with the current date will
                be created containing input and output directories/files

        """
        if not is_tool(madprogram):
            raise IllegalArgumentError('Given madx executable not found.')
        now = datetime.now()
        self._madprogram = madprogram
        self._madinputfn = 'madin.madx'
        self._madoutputfn = 'madx.out'
        self._output = {'files': []}
        self._freq = 1.25e6
        self._check_date(date, now)
        self._dirmadin = ''
        self._dirmadout = ''
        self._dirreport = ''
        self._dirtwiss = ''
        self._dirplots = ''
        self._home = maddir

        self.homedir = maddir

        self.inputstring = ''

    def __str__(self):
        """
        String representation of the madx object,
        basically what goes in the madx input file.
        """
        return str(self.inputstring)

    def _check_date(self, date, now):
        """
        Method to check if a valid date is given,
        if not raise value error
        """
        if not date:
            self._date = now.strftime('%Y-%m-%d')
            self._datetime = now.strftime('%Y-%m-%d-%H-%M-%S')
            self.inputstring = ''''''
        elif is_date(date):
            self._date = date
            self._datetime = date + now.strftime('-%H-%M-%S')
        else:
            raise ValueError

    @property
    def madprogram(self):
        return self._madprogram

    @property
    def madinputfn(self):
        return self._madinputfn

    @property
    def madoutputfn(self):
        return self._madoutputfn

    @property
    def output(self):
        return self._output

    @property
    def freq(self):
        return self._freq

    @property
    def homedir(self):
        return self._home

    @property
    def madindir(self):
        return self._dirmadin

    @property
    def madoutdir(self):
        return self._dirmadout

    @property
    def reportdir(self):
        return self._dirreport

    @property
    def twissdir(self):
        return self._dirtwiss

    @property
    def plotdir(self):
        return self._dirplots

    @madinputfn.setter
    def madinputfn(self, fn):
        self._madinputfn = self._datetime + '____' + fn

    @madoutputfn.setter
    def madoutputfn(self, fn):
        self._madoutputfn = self._datetime + '____' + fn

    @freq.setter
    def freq(self, f):
        self._freq = f

    @property
    def date(self):
        return self._date

    @property
    def datetime(self):
        return self._datetime

    @homedir.setter
    def homedir(self, path):
        if not os.path.exists(path):
            logger.info('given path does not exist - path created')
            os.makedirs(path)
        self._home = path
        self._create_dirs()

    def _create_dirs(self):
        """
        Internal function for setting/creating/updating working directories.
        """
        self._dirmadin = os.path.join(self._home, self._date, 'madin')
        self._dirmadout = os.path.join(self._home, self._date, 'madout')
        self._dirreport = os.path.join(self._home, self._date, 'report')
        self._dirtwiss = os.path.join(self._home, self._date, 'twiss')
        self._dirplots = os.path.join(self._home, self._date, 'plots')

        dirlist = [self._dirmadin,
                   self._dirmadout,
                   self._dirreport,
                   self._dirtwiss,
                   self._dirplots,
                   ]

        for dir in dirlist:
            if not os.path.exists(dir):
                os.makedirs(dir)
                logger.info('dir {} does not exist - dir created'.format(dir))

        logger.info('Necessary dirs created/updated')

    def updateoutput(self, k, v):

        """
        Function to update the internal _output dictionary,
        this keeps track of used files and if twiss or survey
        has been run.

        Parameters:
            k: key
            v: value


        """
        if k in self._output.keys():
            # if the value is a list append the new value
            if isinstance(self._output[k], list):
                self._output[k].append(v)
            # if the value is a dict update dict
            elif isinstance(self._output[k], dict):
                self._output[k].update(v)
            # if single value, create a list and add the new value
            else:
                self._output.update({k: [v, self._output[k]]})
        else:
            # if k does not exist add the k,v pair
            self._output.update({k: v})

    def clearoutput(self):
        """
        Clear the output log.
        """
        self._output = {'files': []}

    def loadfile(self, filename):
        """
        Method to load an external madx input file
        and update output log.


        Parameters:
            filename : str
                filename containing the madx input to be loaded
        """
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                self.inputstring = f.read()
                self.updateoutput('files', filename)
        else:
            raise FileNotFoundError

    def add_string_input(self, string):
        """
        Add a string manually to the input string.

        Parameters:
            string : input string
                a newline char will be added automatically
        """
        self.inputstring += string + '\n'

    def clearinput(self):
        """
        Clear all the madx input from the input,
        output log is also cleared.
        """
        self.inputstring = ''
        self.clearoutput()
        logger.info('MADX input cleared.')

    def set_value(self, settingsdict):
        """
        Set a variable value ("=" operator in MAD-X).

        Parameters:
            settingsdict : dict
                dictionary containing the updated settings

        Usage:
            >>> madx = Madx('maddx-dev')
            >>> madx.set_value({'R1QS1->K1': 42})
            >>> madx.inputstring.splitlines()[-1]
            R1QS1->K1=42;\n

            >>> madx.set_value({'R1QS1, K1': 42})
            >>> madx.inputstring.splitlines()[-1]
            R1QS1, K1=42;\n
        """
        returnstr = ''
        for k in settingsdict.keys():
            returnstr += str(k) + '=' + str(settingsdict[k]) + ';\n'
        self.inputstring += returnstr

    def set_expression(self, settingsdict):
        """
        Set a variable expression (":=" operator in MAD-X).

        Parameters:
            settingsdict : dict
                dictionary containing the updated settings

        Usage:
            >>> madx = Madx('maddx-dev')
            >>> madx.set_expression({'FOO': 'BAR'})
            >>> madx.inputstring.splitlines()[-1]
            FOO:=BAR;\n
        """
        returnstr = ''
        for k in settingsdict.keys():
            returnstr += str(k) + ':=' + str(settingsdict[k]) + ';\n'
        self.inputstring += returnstr

    def call(self, filename):
        """
        Call a file.

        Parameters:
            filename : str
                filename
        """
        if os.path.isfile(filename):
            self.inputstring += 'call, file = \'{}\';\n'.format(filename)
            self.updateoutput('files', filename)
        else:
            raise FileNotFoundError

    def beam(self, *args, **kwargs):
        """
        Generate the beam command,

        Usage:
            >>>madx = Madx('madx-dev')
            >>>madx.clearinput()
            >>>madx.beam(particle='electron', energy=1.7)#, sige=7e-4, sigt=2.8e-3, ex=5.0e-9, ey =5.0e-9)

        """
        beam1 = ', '.join("{0} = {1}".format(k, v) for k, v in kwargs.items())
        beam2 = ', '.join(args)
        beam = beam1 + beam2

        self.inputstring += 'beam, {};\n'.format(beam)

    def use(self, period):
        """
        USE command

        Parameters:
            period : name of lattice period to use
        """
        self.inputstring += 'USE, PERIOD={};\n'.format(period)

    def twiss(self, **kwargs):
        """
        Twiss with separate select and use,
        which need to be done manually.
        """
        if 'file' not in kwargs.keys():
            raise IllegalArgumentError('`file` missing in kwargs.')

        twissstr = 'TWISS, '
        twissstr += ', '.join('{0} = {1}'.format(k, v) for k, v in kwargs.items())
        self.inputstring += twissstr + ';\n'  # don't forget to close command with ; and newline char
        self.updateoutput('twiss', '{file}'.format(**kwargs))
        self.updateoutput('statustwiss', 'prepared')

    def Twiss(self, *args, **kwargs):
        """
        Pre-defined twiss with ombined select, use and twiss.
        Requires at least sequence, if not given IllegalArgumentError is raised.
        Twiss file is automatically set to home/dirtwiss/datetime-twiss.tfs

        Example:
            >>> madx = Madx('madx-dev')
            >>> madx.Twiss(sequence='ringbii')
        """
        if 'sequence' not in [k.lower() for k in kwargs.keys()]:
            raise IllegalArgumentError('Missing argument, sequence needed.')

        if 'column' in kwargs.keys():
            kwargs['column'] = '{' + ','.join(kwargs['column']) + '}'

        twissstr = 'SELECT, FLAG=TWISS, '

        twissstr += ', '.join('{0} = {1}, '.format(k, v) for k, v in kwargs.items()
                              if ((k != 'sequence') & (k != 'file') & (k != 'table')))

        if 'clear' in args:
            twissstr += 'clear'

        self.inputstring += twissstr + ';\n'
        self.inputstring += 'USE, PERIOD={sequence};\n'.format(**kwargs)

        if 'file' in kwargs.keys():
            self.inputstring += 'TWISS, SEQUENCE = {sequence}, file = \'{file}\''.format(**kwargs)
            self.updateoutput('twiss', '{file}'.format(**kwargs))
        else:
            self.inputstring += ('TWISS, SEQUENCE = {sequence}, file = \'' + self.twissdir
                                 + self.datetime + '-twiss.tfs\'').format(**kwargs)
            self.updateoutput('twiss', self.twissdir + self.datetime + '-twiss.tfs')

        if 'table' in kwargs.keys():
            self.inputstring += ', table={table}'.format(**kwargs)

        self.inputstring += ';\n'

        self.updateoutput('statustwiss', 'prepared')

        logger.info('Twiss prepared')

    def survey(self, **kwargs):
        """
        Runs the survey module.
        Requires a sequence and filename when
        missing IllegalArgumentError is raised .
        Survey file is automatically set to
        home/dirtwiss/datetime-survey.tfs

        Usage:
            >>> madx = Madx('madx-dev')
            >>> madx.survey(sequence='ringbii')

        """
        if 'sequence' not in kwargs.keys():
            raise IllegalArgumentError('Missing argument, sequence and file needed.')

        self.inputstring += ('USE, SEQUENCE={sequence};\nSURVEY,FILE=\''
                             + self.twissdir + self.datetime + '-survey.tfs\';\n').format(**kwargs)

        self.updateoutput('survey', self._dirtwiss + self._datetime + '-survey.tfs')
        self.updateoutput('statussurvey', 'prepared')

        logger.info('Survey prepared')

    def installElement(self, sequence, element, location):
        """
        Install an element in an existing and preloaded sequence.

        Parameters:
            sequence: sequence where the new element has to be installed
            element: element definition
            location: s position of the middle of the element

        Usage:
            >>> madx = Madx('madx-dev')
            >>> str_coupler_definition_ref = "vsrcouplerkickhor1: hkicker,kick:= 0;"
            >>> madx.add_string_input(str_coupler_definition_ref)
            >>> madx.installElement('RINGBII','vsrcouplerkickhor1',45.00-1.479)

        """
        try:
            logger.info('Installing Element ' + str(element) + ' at ' + str(location))

            strReturn = ''''''
            strstart = 'USE, period = {0};\nSEQEDIT, SEQUENCE = {0};\nFLATTEN;\n'.format(sequence)
            strbody = 'INSTALL, ELEMENT = {0:10}, AT = {1:10.6f};\n'.format(element, location)
            strend = 'FLATTEN;\nENDEDIT;\n'

            strReturn += strstart + strbody + strend

            self.inputstring += strReturn

            logger.info('Element installed successfully.')

        except TypeError:
            logger.exception('Missing arguments')

    def slice(self, seq, **kwargs):
        """
        Slice elements for smoother
        optical functions

        Parameters:
            seq: sequence to use
            kwargs: optional parameters
            updates the madx input string
        """
        if kwargs:
            logger.info('Setting slicing')
            self.inputstring += 'USE, SEQUENCE={};\n'.format(seq)
            for k, v in kwargs.items():
                logger.info('Setting slicing for {0}, # of slices = {1}'.format(k, int(v)))
                self.inputstring += 'SELECT, FLAG=MAKETHIN, class={0} , SLICE={1};\n'.format(k, int(v))
        else:
            logger.info('No arguments provided for slicing, no slicing performed.')
        self.inputstring += 'MAKETHIN, SEQUENCE={0}, style=SIMPLE, MAKEDIPEDGE=false;\n'.format(seq)

    def run(self):  # pragma: no cover
        """
        Run madx on the input string.

        Usage:
            >>> madx = Madx('madx-dev')
            >>> madx.run()

        """
        try:
            # writing mad input to file
            with open(os.path.join(self.madindir, self.madinputfn), 'w') as f:
                f.write(self.inputstring)

            # running mad
            logger.info("MADX running")

            subprocess.call(
                self.madprogram + '<' + os.path.join(self._dirmadin, self.madinputfn) + '>' + os.path.join(
                    self._dirmadout, self.madoutputfn),
                shell=True)

            # get the last two lines of the mad output to check if run was successful or not
            with open(os.path.join(self._dirmadout, self.madoutputfn), 'r') as fout:
                last = fout.readlines()[-2]

            if 'normally' in last:
                if 'statustwiss' in self.output.keys():
                    self.updateoutput('statustwiss', 'ok')

                if 'statussurvey' in self.output.keys():
                    self.updateoutput('statussurvey', 'ok')

                logger.info('Madx finished normally.')

            else:
                raise RuntimeError

        except RuntimeError:
            logger.exception("MADX Failed")
           