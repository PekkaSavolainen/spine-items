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
Unit tests for :class:`ExporterExecutable`.

:author: A. Soininen (VTT)
:date:   6.4.2020
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock
from gdx2py import GdxFile
from spine_engine import ExecutionDirection
from spinedb_api import create_new_spine_database, DiffDatabaseMapping, import_functions
from spine_engine.project_item.project_item_resource import ProjectItemResource
from spine_items.gdx_exporter.database import Database
from spine_items.gdx_exporter.gdx_exporter import SettingsPack
from spine_items.gdx_exporter.executable_item import ExecutableItem
from spine_items.gdx_exporter.settings_state import SettingsState
from spinedb_api.spine_io import gdx_utils
from spinedb_api.spine_io.exporters import gdx


class TestGdxExporterExecutable(unittest.TestCase):
    def test_item_type(self):
        self.assertEqual(ExecutableItem.item_type(), "GdxExporter")

    def test_from_dict(self):
        item_dict = {
            "type": "GdxExporter",
            "description": "",
            "x": 0,
            "y": 0,
            "settings_pack": {
                "settings": {
                    "domains": {
                        "connection": {
                            "tier": 0,
                            "records": {"indexing_type": "fixed", "indexes": []},
                            "metadata": {"exportable": 1, "origin": 1},
                        },
                        "unit": {
                            "tier": 2,
                            "records": {"indexing_type": "fixed", "indexes": [["a"], ["b"], ["c"]]},
                            "metadata": {"exportable": 1, "origin": 1},
                        },
                        "pipe": {
                            "tier": 1,
                            "records": {"indexing_type": "fixed", "indexes": []},
                            "metadata": {"exportable": 1, "origin": 1},
                        },
                    },
                    "sets": {},
                    "global_parameters_domain_name": "",
                },
                "indexing_settings": {},
                "merging_settings": {},
                "none_fallback": 0,
                "none_export": 0,
            },
            "databases": [
                {
                    "scenario": None,
                    "output_file_name": "output.gdx",
                    "database_url": {
                        "type": "file_url",
                        "relative": True,
                        "path": ".spinetoolbox/items/data_store/Data Store.sqlite",
                        "scheme": "sqlite",
                    },
                }
            ],
            "cancel_on_error": True,
        }
        logger = mock.MagicMock()
        with TemporaryDirectory() as temp_dir:
            item = ExecutableItem.from_dict(item_dict, "GdxExporter 1", temp_dir, _MockSettings(), dict(), logger)
            self.assertIsInstance(item, ExecutableItem)
            self.assertEqual("GdxExporter", item.item_type())
            self.assertIsInstance(item._settings_pack, SettingsPack)
            # Make SettingsPack.from_dict raise gdx.GdxExportException
            with mock.patch("spine_items.gdx_exporter.executable_item.SettingsPack.from_dict") as mocksetfromdict:
                mocksetfromdict.side_effect = gdx.GdxExportException("hello")
                item = ExecutableItem.from_dict(item_dict, "GdxExporter 1", temp_dir, _MockSettings(), dict(), logger)
                self.assertIsInstance(item, ExecutableItem)
                self.assertEqual("GdxExporter", item.item_type())
                self.assertIsInstance(item._settings_pack, SettingsPack)
            # Modify item_dict
            item_dict.pop("cancel_on_error")
            item = ExecutableItem.from_dict(item_dict, "GdxExporter 1", temp_dir, _MockSettings(), dict(), logger)
            self.assertIsInstance(item, ExecutableItem)
            self.assertEqual("GdxExporter", item.item_type())
            self.assertTrue(item._cancel_on_error)
            self.assertIsInstance(item._settings_pack, SettingsPack)

    def test_stop_execution(self):
        # TODO: Seems that there is no way to stop the Exporting process at the moment.
        # TODO: Implement this test when GdxExporter ExecutableItem stop_execution() method is implemented
        with TemporaryDirectory() as temp_data_dir:
            executable = ExecutableItem("name", SettingsPack(), [], False, True, temp_data_dir, "", mock.MagicMock())
            with mock.patch(
                "spine_engine.project_item.executable_item_base.ExecutableItemBase.stop_execution"
            ) as mock_stop_execution:
                executable.stop_execution()
                mock_stop_execution.assert_called_once()

    @unittest.skipIf(gdx_utils.find_gams_directory() is None, "No working GAMS installation found.")
    def test_execute_no_output(self):
        executable = ExecutableItem("name", SettingsPack(), [], False, False, "", "", mock.MagicMock())
        self.assertTrue(executable.execute([], []))

    @unittest.skipIf(gdx_utils.find_gams_directory() is None, "No working GAMS installation found.")
    def test_execute_exports_simple_database_to_gdx(self):
        with TemporaryDirectory() as tmp_dir_name:
            database_path = Path(tmp_dir_name).joinpath("test_execute_forward.sqlite")
            database_url = "sqlite:///" + str(database_path)
            create_new_spine_database(database_url)
            database_map = DiffDatabaseMapping(database_url)
            import_functions.import_object_classes(database_map, ["domain"])
            import_functions.import_objects(database_map, [("domain", "record")])
            settings_pack = SettingsPack()
            settings_pack.settings = gdx.make_set_settings(database_map)
            settings_pack.indexing_settings = gdx.make_indexing_settings(
                database_map, gdx.NoneFallback.USE_IT, logger=mock.MagicMock()
            )
            settings_pack.state = SettingsState.OK
            database_map.commit_session("Add an entity_class and an entity for unit tests.")
            database_map.connection.close()
            databases = [Database()]
            databases[0].output_file_name = "output.gdx"
            databases[0].url = database_url
            logger = mock.MagicMock()
            logger.__reduce__ = lambda _: (mock.MagicMock, ())
            executable = ExecutableItem("name", settings_pack, databases, False, False, tmp_dir_name, "", logger)
            resources = [ProjectItemResource(mock.Mock(), "database", database_url)]
            self.assertTrue(executable.execute(resources, []))
            self.assertTrue(Path(tmp_dir_name, "output.gdx").exists())
            gams_directory = gdx.find_gams_directory()
            with GdxFile(str(Path(tmp_dir_name, "output.gdx")), "r", gams_directory) as gdx_file:
                self.assertEqual(len(gdx_file), 1)
                expected_symbol_names = ["domain"]
                for gams_symbol, expected_name in zip(gdx_file.keys(), expected_symbol_names):
                    self.assertEqual(gams_symbol, expected_name)
                gams_set = gdx_file["domain"]
                self.assertEqual(len(gams_set), 1)
                expected_records = ["record"]
                for gams_record, expected_name in zip(gams_set, expected_records):
                    self.assertEqual(gams_record, expected_name)

    def test_output_resources_backward(self):
        executable = ExecutableItem("name", SettingsPack(), [], False, False, "", "", mock.MagicMock())
        self.assertEqual(executable.output_resources(ExecutionDirection.BACKWARD), [])

    def test_output_resources_forward(self):
        with TemporaryDirectory() as data_dir:
            executable = ExecutableItem("name", SettingsPack(), [], False, False, data_dir, "", mock.MagicMock())
            resources = executable.output_resources(ExecutionDirection.FORWARD)
            self.assertEqual(len(resources), 0)


class _MockSettings:
    @staticmethod
    def value(key, defaultValue=None):
        return {"appSettings/gamsPath": ""}.get(key, defaultValue)


if __name__ == "__main__":
    unittest.main()
