######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################
"""
Contains utilities to scan for Data Connection's output resources.

"""
from pathlib import Path
from spine_engine.project.project_item_resource import file_resource, transient_file_resource, url_resource
from spine_engine.utils.serialization import path_in_dir
from ..utils import unsplit_url_credentials


def file_paths_to_resources(name, data_dir, file_paths, project_dir):
    """
    Creates file resources based on DC's file references and data.

    Args:
        name (str): name of the data connection that provides the resources
        data_dir (Path, optional): data connection's data directory
        file_paths (list of Path): file paths
        project_dir (Path, optional): absolute path to project directory

    Returns:
        list of ProjectItemResource: output resources
    """
    def absolute_path_resource(path):
        return file_resource(name, path) if path.exists() else transient_file_resource(name, path)

    resources = []
    if data_dir is not None:
        for fp in file_paths:
            try:
                if path_in_dir(fp, data_dir):
                    resource = file_resource(
                        name, fp, label=f"<{name}>/" + fp.relative_to(data_dir).as_posix()
                    )
                elif path_in_dir(fp, project_dir):
                    label = "<project>/" + fp.relative_to(project_dir).as_posix()
                    if fp.exists():
                        resource = file_resource(name, fp, label=label)
                    else:
                        resource = transient_file_resource(name, label)
                else:
                    resource = absolute_path_resource(fp)
            except PermissionError:
                continue
            resources.append(resource)
    else:
        for fp in file_paths:
            try:
                resource = absolute_path_resource(fp)
            except PermissionError:
                continue
            resources.append(resource)
    return resources


def urls_to_resources(name, urls, url_credentials):
    """Transforms URLs into Data Connection resources.

    Args:
        name (str): name of the data connection that provides the resources
        urls (list of str): urls
        url_credentials (dict): mapping URL from urls to tuple (username, password)

    Returns:
        list of ProjectItemResource: output resources
    """
    resources = []
    for url in urls:
        credentials = url_credentials.get(url)
        full_url = unsplit_url_credentials(url, credentials) if credentials is not None else url
        resource = url_resource(name, full_url, f"<{name}>" + url)
        resources.append(resource)
    return resources
