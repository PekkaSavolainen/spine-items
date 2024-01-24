######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# Copyright (C) 2023-2024 Mopo project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Unit tests for Importer's ItemInfo class.

"""
import unittest
from spine_items.importer.item_info import ItemInfo


class TestItemInfo(unittest.TestCase):
    def test_item_type(self):
        self.assertEqual(ItemInfo.item_type(), "Importer")

    def test_item_category(self):
        self.assertEqual(ItemInfo.item_category(), "Importers")


if __name__ == "__main__":
    unittest.main()
