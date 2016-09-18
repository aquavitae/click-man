import os
from distutils.core import Command
from distutils.errors import DistutilsSetupError
from pkg_resources import EntryPoint

from click_man.core import write_man_pages


__all__ = ['man_pages']



class man_pages(Command):
    description = 'distutils command to generate man pages'

    user_options = [
        ('target=', 't', 'Target location for the man pages')
    ]
    boolean_options = []

    def initialize_options(self):
        self.target = os.path.join(os.getcwd(), 'man')

    def finalize_options(self):
        self.target = os.path.abspath(self.target)

        # create target directory if it does not exist yet
        try:
            os.makedirs(self.target)
        except OSError:
            pass

    def run(self):
        eps = EntryPoint.parse_map(self.distribution.entry_points or '')

        if 'console_scripts' not in eps or not eps['console_scripts']:
            raise DistutilsSetupError('No entry points defined in setup()')

        console_scripts = [(k, v) for k, v in eps['console_scripts'].items()]
        # Only generate man pages for first console script
        # FIXME: create own setup() attribute for CLI script configuration
        name, entry_point = console_scripts[0]

        self.announce('Load entry point {0}'.format(name), level=2)
        cli = entry_point.resolve()
        self.announce('Generate man pages for {0}'.format(name), level=2)
        write_man_pages(name, cli, target_dir=self.target)