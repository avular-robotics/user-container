from setuptools import find_packages, setup

package_name = 'navigation_tests'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joris Sijs',
    maintainer_email='j.sijs@avular.com',
    description='ROS2-python tests for continuous navigation with Avular its Origin',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'continuous_driving_test = navigation_tests.continuous_driving_test:main',
        ],
    },
)
