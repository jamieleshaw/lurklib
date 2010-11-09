#!/usr/bin/env python
try:
    import nose
    nose.main()
except ImportError:
    print('Nose is needed to run all Lurklib tests at once.' + \
          ' Without Nose you can only run them one by one via tests/.')
