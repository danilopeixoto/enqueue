import os
from distutils.util import convert_path
from setuptools import setup, find_packages


def get_package_info(relative_path):
  '''Get package information from module path.'''

  package_info = {}

  with open(convert_path(
      os.path.join(relative_path, 'package.py')), 'r') as file:
    exec(file.read(), package_info)

  return package_info


package_name = 'enqueue'
package_info = get_package_info(package_name)

sample_requirements = [
  'opencv-python>=4.5.1.0',
  'mediapipe>=0.8.3.0'
]

test_requirements = [
  'pytest>=6.2.0'
]

setup(
  name = package_name,
  version = package_info['__version__'],
  description = package_info['__description__'],
  author = package_info['__author__'],
  author_email = package_info['__email__'],
  license = package_info['__license__'],
  python_requires = '>=3.6.0',
  extras_require = dict(
    sample = sample_requirements,
    test = test_requirements),
  packages = find_packages(),
  zip_safe = False)
