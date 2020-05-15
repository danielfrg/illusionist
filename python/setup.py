import os

from setuptools import find_packages, setup


setup_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    filepath = os.path.join(setup_dir, filename)
    with open(filepath) as file:
        return file.read()


scm_version_write_to_prefix = os.environ.get(
    "SETUPTOOLS_SCM_VERSION_WRITE_TO_PREFIX", setup_dir
)


def parse_git(root, **kwargs):
    from setuptools_scm.git import parse

    kwargs["describe_command"] = 'git describe --dirty --tags --long --match "[0-9].*"'
    return parse(root, **kwargs)


setup(
    name="illusionist",
    use_scm_version={
        "root": os.path.dirname(setup_dir),
        "parse": parse_git,
        "write_to": os.path.join(
            scm_version_write_to_prefix, "illusionist/_generated_version.py"
        ),
    },
    packages=find_packages(),
    # package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    # package_data={"illusionist": ["includes/*"]},
    # data_files=data_files,
    # cmdclass={"install": InstallCmd},
    # entry_points = {},
    options={"bdist_wheel": {"universal": "1"}},
    python_requires=">=3.6",
    setup_requires=["setuptools_scm"],
    install_requires=read_file("requirements-package.txt").splitlines(),
    extras_require={
        "test": ["pytest"],
        "dev": read_file("requirements.txt").splitlines(),
    },
    description="",
    long_description=read_file("../README.md"),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    maintainer="Daniel Rodriguez",
    maintainer_email="daniel@danielfrg.com",
    url="https://github.com/danielfrg/illusionist",
    keywords=[],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
