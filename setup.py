from setuptools import setup, find_packages

setup(
    name="persona-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "flask-migrate",
        "flask-cors",
        "pytest",
        "python-dotenv",
    ],
    python_requires=">=3.8",
)
