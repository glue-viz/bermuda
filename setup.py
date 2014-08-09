from setuptools import setup

VERSION = '0.1.dev'

DESCRIPTION = "Interactive shapes in Python"
NAME = "mpl_shapes"
AUTHOR = "Chris Beaumont and Thomas Robitaille"
AUTHOR_EMAIL = "cbeaumont@cfa.harvard.edu and thomas.robitaille@gmail.com"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "BSD"
URL = "https://github.com/glue-viz/bermuda"

setup(name=NAME,
      description=DESCRIPTION,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      license=LICENSE,
      packages=['mpl_shapes', 'mpl_shapes.tests'],
      provides=['mpl_shapes'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Operating System :: OS Independent',
          'Topic :: Utilities'],
      )