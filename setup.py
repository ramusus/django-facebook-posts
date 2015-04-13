from setuptools import setup, find_packages

setup(
    name='django-facebook-posts',
    version=__import__('facebook_posts').__version__,
    description='Django implementation for Facebook Graph API Posts',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-facebook-posts',
    download_url='http://pypi.python.org/pypi/django-facebook-posts',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including media that Django needs
    install_requires=[
        'django-facebook-api>=0.5.0',
        'django-facebook-applications>=0.1.0',
        'django-facebook-users>=0.3.0',
        'django-facebook-pages>=0.3.0',
        'django-m2m-history>=0.1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
