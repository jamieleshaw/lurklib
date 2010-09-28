from distutils.core import setup
setup (\
        name='lurklib',
        packages=['lurklib'],
        version='0.4.7.7',
        author='LK-',
        license='GPL V3',
        author_email='lk.codeshock@gmail.com',
        description='The Lurk Internet Relay Chat Library',
        url='http://github.com/LK-/lurklib/',
        keywords = ['irc', 'internet relay chat'],
        classifiers = [
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 2',
                       'Programming Language :: Python :: 3',
                       'License :: OSI Approved :: GNU General Public License (GPL)',
                       'Operating System :: OS Independent',
                       'Development Status :: 4 - Beta',
                       'Intended Audience :: Developers',
                       'Topic :: Software Development :: Libraries :: Python Modules'
                       ],
        long_description=
        '''
        The Lurk Internet Relay Chat Library is a library that provides an excellent level of, abstraction and serialization from the underlying IRC protocol.
        It has full compatibility with Python 2.6+ and Python 3+, and also works with Python 2.5 however, Python 2.5 doesn't have the SSL module thus their is no SSL support.
        Support for lurklib can be found @ irc.codeshock.org -> #lurklib.
        '''
        )

