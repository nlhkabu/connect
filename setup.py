import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    CHANGELOG = f.read()

with codecs.open(os.path.join(here, 'AUTHORS.rst'),
                 encoding='utf-8') as f:
    CONTRIBUTORS = f.read()


REQUIREMENTS = [
    'django',
    'django-classy-settings',
    'dj-static',
    'Pillow',
    'pytz',
    'dj-database-url',
    'PyYAML',
    'django-gravatar2',
    'django-parsley',
    'psycopg2>2.5',
]

DEPENDENCY_LINKS = [
]


setup(name='django-mentor-connect',
      version='1.0.dev0',
      description='Django Mentor Connect',
      long_description=README + "\n\n" + CHANGELOG + "\n\n" + CONTRIBUTORS,
      license='BSD License',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Framework :: Django :: 1.7",
          "Framework :: Django :: 1.8",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3 :: Only",
      ],
      keywords="django mentor connect",
      author='Nicole Harris',
      author_email='n.harris@kabucreative.com.au',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      dependency_links=DEPENDENCY_LINKS)
