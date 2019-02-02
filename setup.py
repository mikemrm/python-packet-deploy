from distutils.core import setup

setup(
    name='PacketDeploy',
    version='0.0.1',
    author='Mike Mason',
    author_email='immrmason@gmail.com',
    packages=['packetdeploy'],
    url='https://github.com/mikemrm/python-packet-deploy',
    description="Simple example tool for deploying a server using packet.net's api",
    install_requires=[
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'pd = packetdeploy.command_line:main'
        ]
    }
)
