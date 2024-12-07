from setuptools import setup, find_packages

setup(
	name='project3',
	version='1.0',
	author='Pradhyumna Reddy Madhulapally',
	author_email='madhulapally.p@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)