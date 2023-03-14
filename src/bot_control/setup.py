from setuptools import setup
from setuptools import find_packages
packages = find_packages(exclude=['test'])
package_name = 'bot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=packages,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kart1004',
    maintainer_email='kart1004@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['talker = bot_control.laser_scan_publisher:main',
                            'listener = scripts.reading_laser:main',
        ],
    },
)
