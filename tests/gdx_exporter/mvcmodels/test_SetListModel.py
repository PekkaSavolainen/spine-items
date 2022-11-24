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
Unit tests for :class:`SetListModel`.

:authors: A. Soininen (VTT)
:date:   26.9.2019
"""

import unittest
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QColor
from spine_items.gdx_exporter.mvcmodels.set_list_model import SetListModel
from spinedb_api.spine_io.exporters.gdx import ExportFlag, Origin, SetMetadata, SetSettings


class TestSetListModel(unittest.TestCase):
    """Unit tests for the GAMSSetListModel class used by the Gdx Export Settings Window."""

    def test_data_DisplayRole(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        index = model.index(0, 0)
        self.assertEqual(index.data(), "domain1")
        index = model.index(1, 0)
        self.assertEqual(index.data(), "set1")

    def test_data_BackgroundRole(self):
        set_settings = SetSettings({"domain1", "extra_domain1", "extra_domain2"}, {"set1"}, {})
        set_settings.metadata("extra_domain1").origin = Origin.INDEXING
        set_settings.metadata("extra_domain2").origin = Origin.MERGING
        model = SetListModel(set_settings)
        index = model.index(0, 0)
        self.assertEqual(index.data(Qt.BackgroundRole), QColor(245, 245, 120))
        index = model.index(1, 0)
        self.assertEqual(index.data(Qt.BackgroundRole), QColor(235, 235, 110))
        index = model.index(2, 0)
        self.assertEqual(index.data(Qt.BackgroundRole), QColor(235, 235, 110))
        index = model.index(3, 0)
        self.assertEqual(index.data(Qt.BackgroundRole), None)

    def test_data_CheckStateRole(self):
        set_settings = SetSettings(
            {"domain1"},
            {"set1"},
            {},
            metadatas={
                "domain1": SetMetadata(ExportFlag.NON_EXPORTABLE),
                "set1": SetMetadata(ExportFlag.NON_EXPORTABLE),
            },
        )
        model = SetListModel(set_settings)
        index = model.index(0, 0)
        self.assertEqual(index.data(Qt.CheckStateRole), Qt.Unchecked.value)
        index = model.index(1, 0)
        self.assertEqual(index.data(Qt.CheckStateRole), Qt.Unchecked.value)

    def test_flags(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        flags = model.flags(model.index(0, 0))
        self.assertEqual(flags, Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)

    def test_headerData(self):
        set_settings = SetSettings(set(), set(), {})
        model = SetListModel(set_settings)
        self.assertEqual(model.headerData(0, Qt.Horizontal), "")

    def test_is_domain(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        self.assertTrue(model.is_domain(model.index(0, 0)))
        self.assertFalse(model.is_domain(model.index(1, 0)))

    def test_moveRows_move_domain_row_down(self):
        set_settings = SetSettings({"domain1", "domain2", "domain3"}, set(), {})
        model = SetListModel(set_settings)
        self.assertTrue(model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 1))
        self.assertEqual(set_settings.domain_tiers, {"domain1": 1, "domain2": 0, "domain3": 2})
        self.assertTrue(model.moveRows(QModelIndex(), 1, 1, QModelIndex(), 2))
        self.assertEqual(set_settings.domain_tiers, {"domain1": 2, "domain2": 0, "domain3": 1})
        self.assertFalse(model.moveRows(QModelIndex(), 2, 1, QModelIndex(), 3))

    def test_moveRows_move_domain_row_up(self):
        set_settings = SetSettings({"domain1", "domain2", "domain3"}, set(), {})
        model = SetListModel(set_settings)
        self.assertTrue(model.moveRows(QModelIndex(), 2, 1, QModelIndex(), 1))
        self.assertEqual(set_settings.domain_tiers, {"domain1": 0, "domain2": 2, "domain3": 1})
        self.assertTrue(model.moveRows(QModelIndex(), 1, 1, QModelIndex(), 0))
        self.assertEqual(set_settings.domain_tiers, {"domain1": 1, "domain2": 2, "domain3": 0})
        self.assertFalse(model.moveRows(QModelIndex(), 0, 1, QModelIndex(), -1))

    def test_moveRows_domain_cannot_cross_to_sets(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        self.assertFalse(model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 1))

    def test_moveRows_move_set_row_down(self):
        set_settings = SetSettings(set(), {"set1", "set2", "set3"}, {})
        model = SetListModel(set_settings)
        self.assertTrue(model.moveRows(QModelIndex(), 0, 1, QModelIndex(), 1))
        self.assertEqual(set_settings.set_tiers, {"set1": 1, "set2": 0, "set3": 2})
        self.assertTrue(model.moveRows(QModelIndex(), 1, 1, QModelIndex(), 2))
        self.assertEqual(set_settings.set_tiers, {"set1": 2, "set2": 0, "set3": 1})
        self.assertFalse(model.moveRows(QModelIndex(), 2, 1, QModelIndex(), 3))

    def test_moveRows_move_set_row_up(self):
        set_settings = SetSettings(set(), {"set1", "set2", "set3"}, {})
        model = SetListModel(set_settings)
        self.assertTrue(model.moveRows(QModelIndex(), 2, 1, QModelIndex(), 1))
        self.assertEqual(set_settings.set_tiers, {"set1": 0, "set2": 2, "set3": 1})
        self.assertTrue(model.moveRows(QModelIndex(), 1, 1, QModelIndex(), 0))
        self.assertEqual(set_settings.set_tiers, {"set1": 1, "set2": 2, "set3": 0})
        self.assertFalse(model.moveRows(QModelIndex(), 0, 1, QModelIndex(), -1))

    def test_moveRows_set_cannot_cross_to_domains(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        self.assertFalse(model.moveRows(QModelIndex(), 1, 1, QModelIndex(), 0))

    def test_rowCount(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        self.assertEqual(model.rowCount(), 2)

    def test_setData_CheckStateRole(self):
        set_settings = SetSettings({"domain1"}, {"set1"}, {})
        model = SetListModel(set_settings)
        index = model.index(0, 0)
        model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        self.assertEqual(set_settings.metadata("domain1"), SetMetadata(ExportFlag.NON_EXPORTABLE))
        self.assertEqual(set_settings.metadata("set1"), SetMetadata(ExportFlag.EXPORTABLE))
        model.setData(index, Qt.Checked, Qt.CheckStateRole)
        self.assertEqual(set_settings.metadata("domain1"), SetMetadata(ExportFlag.EXPORTABLE))
        self.assertEqual(set_settings.metadata("set1"), SetMetadata(ExportFlag.EXPORTABLE))
        index = model.index(1, 0)
        model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        self.assertEqual(set_settings.metadata("set1"), SetMetadata(ExportFlag.NON_EXPORTABLE))


if __name__ == "__main__":
    unittest.main()
