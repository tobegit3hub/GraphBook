from setuptools import setup, find_packages

setup(
    name="topicland",
    version="0.1.0",
    author="tobe",
    author_email="tobeg3oogle@gmail.com",
    url="https://github.com/topicland/TopicLand",
    description=
      "The tool to manage and explore topics with knowledge graphs and so on.",
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "topicland=client.topicland_cmd:main"
        ],
    })
