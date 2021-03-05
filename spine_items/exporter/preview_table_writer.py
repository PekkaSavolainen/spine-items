######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################
"""
Functions to write export preview tables.

:author: A. Soininen (VTT)
:date:   5.1.2021
"""
import numpy
from spinedb_api.spine_io.exporters.writer import Writer


class TableWriter(Writer):
    """An export writer that writes to a Python dictionary."""

    MAX_ROWS = 20

    def __init__(self, thread):
        """
        Args:
            thread (QThread): a thread instance; used to query if work should be interrupted
        """
        self._tables = dict()
        self._current_table = None
        self._thread = thread

    def finish_table(self):
        self._current_table = None

    def start_table(self, table_name):
        self._current_table = self._tables.setdefault(table_name, list())

    @property
    def tables(self):
        """A dictionary containing the tables."""
        return self._tables

    def write_row(self, row):
        self._current_table.append([_sanitize(cell) for cell in row])
        return len(self._current_table) <= self.MAX_ROWS and not self._thread.isInterruptionRequested()


def _sanitize(x):
    """Converts special parameter value types to strings.

    Args:
        x (Any): parameter value

    Returns:
        float, int, str: sanitized value
    """
    if isinstance(x, numpy.float_):
        return float(x)
    if not isinstance(x, (float, str, int)) and x is not None:
        return str(x)
    return x