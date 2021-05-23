"""Ad simulo setup file."""

import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 7, 0), "Ad simulo requires Python 3.7+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    """Return long description."""
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


def get_requirements():
    """Return requirements."""
    requirements_txt = CURRENT_DIR / "requirements.txt"
    with open(requirements_txt, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name='adsimulo',
    use_scm_version={
        'write_to': 'adsimulo/_version.py',
        'write_to_template': '__version__ = "{version}"\n',
        'tag_regex': r'^(?P<prefix>.*/)?(?P<version>\d+(?:\.\d+){1,2})$'
    },
    setup_requires=['setuptools>=30.3.0', 'wheel', 'setuptools_scm'],
    description='A civilisation simulator on a procedural universe.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    keywords='civilisation simulation simulator procedural',
    author='Javier Aguilera',
    author_email='jaguilerapuerta@gmail.com',
    url='https://github.com/kafkaphoenix/adsimulo/',
    project_urls={"Changelog": "https://github.com/kafkaphoenix/adsimulo/blob/main/CHANGES.md"},
    license='GPLv3',
    python_requires='>=3.7',
    install_requires=get_requirements(),
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'adsimulo-version=adsimulo.scripts.version:main',
            'adsimulo-run=adsimulo.scripts.run:main',
        ],
    },
)
