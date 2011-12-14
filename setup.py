#!/usr/bin/env python
from distutils.core import setup
import lurklib

setup(
        name='lurklib',
        packages=['lurklib'],
        version=lurklib.__version__,
        author='LK-',
        license='GPL V3',
        author_email='lk@lkay.org',
        description='Event-driven IRC library.',
        url='https://github.com/LK-/lurklib/',
        keywords=['irc', 'internet relay chat'],
        classifiers=[
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 2',
                       'Programming Language :: Python :: 3',
                       'License :: OSI Approved ::' + \
                       ' GNU General Public License (GPL)',
                       'Operating System :: OS Independent',
                       'Development Status :: 5 - Production/Stable',
                       'Intended Audience :: Developers',
                       'Topic :: Software Development' + \
                       ' :: Libraries :: Python Modules'
                       ],
        )
