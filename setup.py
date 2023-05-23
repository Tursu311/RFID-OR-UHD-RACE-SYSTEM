from setuptools import setup, find_packages

setup(
    name="RFID-OR-UHD-RACE-SYSTEM",
    version="0.9.0",
    author="Nil Massó",
    author_email="n.masso@sapalomera.cat",
    description="",
    long_description=open("README.md", "r").read(),
    url="https://github.com/Tursu311/RFID-OR-UHD-RACE-SYSTEM",
    packages=find_packages(),
    python_requires = '>=3.10',
    #package_data={},
    #package_dir = ["src"],
    install_requires = open('requirements.txt').read().splitlines(),
    download_url="https://github.com/Tursu311/RFID-OR-UHD-RACE-SYSTEM.git",
    entry_points={
    #    'console_scripts': ['RFID-RACE=main:main']
    }
)