from setuptools import setup, find_packages
from src.pybas.version import __version__

module_name = 'pybas'


def requirements_from_pip():
    return [l for l in open('pip.txt').readlines() if not l.startswith('#')]


setup(name=module_name,
      url="https://github.com/tabacof/pybas",
      author="Pedro Tabacof",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version=__version__,
      install_requires=requirements_from_pip(),
      include_package_data=True,
      zip_safe=False)
