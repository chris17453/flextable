from setuptools import setup


setup(
    name='flextable',
    version='1.0.35',
    packages=['flextable'],
    include_package_data=True,
    url='https://github.com/chris17453/flextable/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
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
    entry_points="""
        [console_scripts]
        flextable = flextable.cli:cli_main
        """    
    
)



