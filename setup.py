from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyosmanager",
    packages=["pyosmanager"],
    version="0.2.3",
    license="MIT",
    description="Python client for Open Surplus Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jose R. Morales",
    author_email="dev@josermorales.com",
    url="https://github.com/JoseRMorales/pyOSManager/",
    keywords=[
        "API",
        "Open Surplus Manager",
        "API client",
        "API wrapper",
        "async",
        "iot",
    ],
    install_requires=[
        "aiohttp",
        "backoff",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
