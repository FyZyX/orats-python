from setuptools import setup


def long_description() -> str:
    with open('README.md') as fh:
        return fh.read()


setup(
    name='orats',
    author='Lucas Lofaro',
    author_email='lucasmlofaro@gmail.com',
    url='',
    version='0.1.0',
    description='Client SDK for the ORATS API.',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    install_requires=(
        'httpx~=0.23.0',
        'pydantic~=1.9.1',
    ),
    extras_require={
        'dev': (
            'pytest>=3.7'
        ),
    },
    # py_modules=['main'],
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        # 'Framework :: FastAPI',
        # 'Framework :: AsyncIO',
        # 'Framework :: Flake8',
        # 'Framework :: Sphinx',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ]
)