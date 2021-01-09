import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Kwogger-b_rad_c',
    author='Brad Corlett',
    description='A logging adapter that provides context data to each logging call over its lifetime.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.5',
    packages=['kwogger'],
    install_requires=[
        'termcolor'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent'
    ]
)
