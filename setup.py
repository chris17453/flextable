from setuptools import setup


setup(
    name='flextable',
<<<<<<< HEAD
    version='1.0.37',
    packages=['flextable',],
=======
    version='1.0.35',
    packages=['flextable'],
>>>>>>> refs/remotes/origin/master
    include_package_data=True,
    url='https://github.com/chris17453/flextable/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
<<<<<<< HEAD
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= 'tabular data formatter, for code, cli or pipes',
    install_requires=[
    ],
=======
    author='Charles Watkins',
    author_email='charles@titandws.com',
    description='',
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    #data_files=[
    #    ('share/icons/hicolor/scalable/apps', ['data/proxx.svg']),
    #    ('share/applications', ['data/proxx.desktop'])
    #],
>>>>>>> refs/remotes/origin/master
    entry_points="""
        [console_scripts]
        flextable = flextable.cli:cli_main
        """    
    
)



