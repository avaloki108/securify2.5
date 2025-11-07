from pathlib import Path

from setuptools import find_packages, setup


def read_readme():
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return ""


setup(
    name='securify',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.12',
    install_requires=[
        'py-solc',
        'semantic_version',
        'graphviz',
        'py-etherscan-api',
        'requests',
    ],
    include_package_data=True,
    package_data={
        "securify": [
            "staticanalysis/souffle_analysis/*.dl",
            "staticanalysis/souffle_analysis/patterns/*.dl",
            "staticanalysis/souffle_analysis/semantics/*.dl",
            "staticanalysis/souffle_analysis/contexts/*.dl",
            "staticanalysis/libfunctors/*.sh",
            "staticanalysis/libfunctors/*.cpp",
            "staticanalysis/libfunctors/*.dl",
            "staticanalysis/libfunctors/README.txt",
            "staticanalysis/facts_in/.keep",
            "staticanalysis/facts_out/.keep",
        ]
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'securify = securify.__main__:main'
        ]
    },
    long_description=read_readme(),
    long_description_content_type="text/markdown",
)
