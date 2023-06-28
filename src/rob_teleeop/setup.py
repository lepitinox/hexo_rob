from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rob_teleeop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share', package_name), glob(f'{package_name}/launch/*.launch.py')),
        (os.path.join('share', package_name), glob(f'{package_name}/urdf/*.urdf.xacro')),
        (os.path.join('share', package_name), glob(f'{package_name}/models/*.stl')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='adrienducourthial@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        "main = rob_teleeop.main:main"
        'teleeop = rob_teleeop.rob_teleeop:main',
        'big_launch = rob_teleeop.big_launch:main',
        ],
    },
)
