#!/usr/bin/env python
try:
    import nose
    if __name__ == '__main__':
        nose.main()
except ImportError:
    print('Nose is needed to run all Lurklib tests at once.' + \
          ' Without Nose you can only run them one by one via tests/.')


def get_suite():
    """ Return Lurklib's test suite. """
    loader = nose.loader.TestLoader()
    merge = nose.suite.ContextSuiteFactory()
    suite = merge(loader.loadTestsFromDir('tests/'))
    return suite
