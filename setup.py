import sys
from setuptools import setup, find_packages


if __name__ == '__main__':
    if not (sys.version[0] >= '3' and sys.version[2] >= '5'):
        raise SystemError("Python version must >= 3.5. Your python version is {}".format(sys.version))
    setup(
        name='residue',
        version='0.1',
        author='ict',
        author_email='ictxiangxin@hotmail.com',
        maintainer='ict',
        maintainer_email='ictxiangxin@hotmail.com',
        description='Common base library',
        platforms=["MS Windows", "Mac X", "Unix/Linux"],
        packages=find_packages(),
        classifiers=[
            'Natural Language :: English',
            'Programming Language :: Python',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Programming Language :: Python :: 3'
        ]
    )
