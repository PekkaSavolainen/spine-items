######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Setup script for Python's setuptools.

:author: A. Soininen (VTT)
:date:   3.10.2019
"""
from setuptools import setup, find_packages

with open("README.md", encoding="utf8") as readme_file:
    readme = readme_file.read()

version = {}
with open("spine_items/version.py") as fp:
    exec(fp.read(), version)

req_toolbox_version = version["REQUIRED_SPINE_TOOLBOX_VERSION"]
install_requires = [f"spinetoolbox == {req_toolbox_version}"]

setup(
    name="spine_items",
    version=version["__version__"],
    description="Spine project items",
    long_description=readme,
    author="Spine Project consortium",
    author_email="spine_info@vtt.fi",
    url="https://github.com/Spine-project/spine-items",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license="LGPL-3.0-or-later",
    zip_safe=False,
    keywords="",
    classifiers=[],
    python_requires=">=3.6, <3.8",
    install_requires=install_requires,
    test_suite="tests",
)
