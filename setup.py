from setuptools import setup, find_packages


setup(
    name="es_logging",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
    ],
    description="Elasticsearch logging package for FastAPI services",
    author="Cristher Rubio",
    author_email="cristher@arex.com",
    url="https://github.com/cristherArex/arex_logging_middleware.git",
)
