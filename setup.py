
import setuptools

setuptools.setup(
    name='sqldiff',
    packages=setuptools.find_packages(),
    version='0.0.1',
    license='MIT',
    description='Compare sql objects on different dataes',
    author='Mateusz Matelski',
    author_email='m.z.matelski@gmail.com',
    url='https://github.com/m-matelski/sqldiff',
    # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords = ['sql', 'diff', 'postgres', 'teradata'],
    install_requires=[
        'sqlparse==0.4.1'
    ],
    # entry_points={
    #     'console_scripts': ['sql-diff=sqldiff.console_program:main']
    # },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)