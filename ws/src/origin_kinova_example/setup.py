import xml.etree.ElementTree as ET
from pathlib import Path

from setuptools import setup
import os
from glob import glob

package_xml = ET.parse('package.xml').getroot()
package_name = package_xml.find('name').text
setup(
    name=package_name,
    version=package_xml.find('version').text,
    packages=[package_name],
    maintainer=package_xml.find('license').text,
    maintainer_email=package_xml.find('maintainer').attrib['email'],
    license=package_xml.find('license').text,
    data_files=[
        (str(Path('share') / package_name), ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'kinova_node = origin_kinova_example.control_kinova:main'
        ],
    },
)
