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
"""Unit tests for the ``utils`` module."""
import unittest
from spine_items.utils import add_items_info_to_project_dict, LATEST_PROJECT_DICT_ITEMS_VERSION


class TestAddItemsInfoToProjectDict(unittest.TestCase):
    def test_project_dict_without_items_info(self):
        project_dict = {"project": {}}
        add_items_info_to_project_dict(project_dict)
        self.assertEqual(project_dict, {
            "project": {
                "project_item_packages": {"spine_items": {"version": LATEST_PROJECT_DICT_ITEMS_VERSION}}
            }
        })

    def test_project_dict_with_existing_items_info(self):
        project_dict = {"project": {"project_item_packages": {"other_items": {"version": 99}}}}
        add_items_info_to_project_dict(project_dict)
        self.assertEqual(project_dict, {
            "project": {
                "project_item_packages": {"spine_items": {"version": LATEST_PROJECT_DICT_ITEMS_VERSION}, "other_items": {"version": 99}}
            }
        })


if __name__ == '__main__':
    unittest.main()
