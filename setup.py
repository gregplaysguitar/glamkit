from setuptools import setup, find_packages

setup(
    name='glamkit',
    version='0.5',
    description='A Django toolkit for building websites for the Galleries, Libraries, Archives and Museums sector.',
    url='http://github.com/glamkit/glamkit',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
