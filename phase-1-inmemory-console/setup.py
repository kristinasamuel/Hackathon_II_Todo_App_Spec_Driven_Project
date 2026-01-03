from setuptools import setup, find_packages

setup(
    name="todo-console-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'todo-console=src.main:main',
        ],
    },
    author="AI Developer",
    description="A console-based todo application with in-memory storage",
    python_requires='>=3.13',
)