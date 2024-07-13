from setuptools import find_packages, setup

with open("requirements.txt", "r") as reqs:
    requirements = reqs.readlines()

setup(
    name="emqx_deepstack_exhook",
    version="0.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "emqx_deepstack_exhook = emqx_deepstack_exhook.__main__:cli"
        ]
    },
)
