from setuptools import setup, find_packages

HYPHEN_DOT = "-e ."
def get_requirements(requirements_path: str) -> list[str]:
    """Reads the requirements from a file and returns them as a list."""
    with open(requirements_path, "r") as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]
        if HYPHEN_DOT in requirements:
            requirements.remove(HYPHEN_DOT)
    return requirements


setup(
    name="student-performance",
    version="0.1.0",
    author="Alvin Kabwama",
    author_email="alvin.kabwama@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(requirements_path="requirements.txt"),
)