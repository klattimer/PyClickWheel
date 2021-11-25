from setuptools import setup
import setuptools

PYCLICKWHEEL_VERSION = '0.1'
PYCLICKWHEEL_DOWNLOAD_URL = (
    'https://github.com/klattimer/pyclickwheel/tarball/' + PYCLICKWHEEL_VERSION
)

setup(
    name='pyclickwheel',
    packages=setuptools.find_packages(),
    version=PYCLICKWHEEL_VERSION,
    description='iPod click wheel event driver for raspberry pi GPIO.',
    long_description='',
    license='MIT',
    author='Karl Lattimer',
    author_email='karl@qdh.org.uk',
    url='https://github.com/klattimer/pyclickwheel',
    download_url=PYCLICKWHEEL_DOWNLOAD_URL,
    entry_points={
        'console_scripts': [
            'pyclickwheel=pyclickwheel:main'
        ]
    },
    keywords=[
        'ipod', 'clickwheel', 'raspberrypi', 'pi'
    ],
    install_requires=[
        "pigpio",
        "evdev"
    ],
    data_files=[
        ('etc/systemd/system/', ['data/pyclickwheel.service'])
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
    ],
)
