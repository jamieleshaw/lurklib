#!/usr/bin/env python
from distutils.core import setup
setup(
        name='lurklib',
        packages=['lurklib'],
        version='0.8',
        author='LK-',
        license='GPL V3',
        author_email='lk07805@gmail.com',
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
