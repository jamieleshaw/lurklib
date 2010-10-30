from distutils.core import setup
setup( \
        name='Lurklib',
        packages=['lurklib'],
        version='0.6',
        author='Jamie Shaw (LK-)',
        license='GPL V3',
        author_email='jamieleshaw@gmail.com',
        description='Event-driven IRC library.',
        url='http://github.com/LK-/lurklib/',
        keywords = ['irc', 'internet relay chat'],
        classifiers = [
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 2',
                       'Programming Language :: Python :: 3',
                       'License :: OSI Approved :: GNU General Public License (GPL)',
                       'Operating System :: OS Independent',
                       'Development Status :: 5 - Production/Stable',
                       'Intended Audience :: Developers',
                       'Topic :: Software Development :: Libraries :: Python Modules'
                       ],
        long_description=
        """Lurklib is a threading-safe, event-driven IRC library designed for creating anything from bots to full-fledged IRC Clients."""
        )

