from setuptools import find_packages, setup

setup(
    name="scrapy_redis_exporter",
    version="0.0.1",
    description="Scrapy Feed Storage for redis",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "scrapy>=2.11.1",
    ],
)
