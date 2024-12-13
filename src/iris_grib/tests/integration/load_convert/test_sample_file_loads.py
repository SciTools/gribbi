# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""
Integration tests for grib2 file loading.

These tests load various files from iris-test-data, and compare the cube with a
reference CML file, to catch any unexpected changes over time.

"""

from __future__ import annotations

# import iris_grib.tests first so that some things can be initialised
# before importing anything else.
import iris_grib.tests as tests

from pathlib import Path

import eccodes
import iris
import pytest


_RESULTDIR_PREFIX = ("integration", "load_convert", "sample_file_loads")


@tests.skip_data
class TestBasicLoad(tests.IrisGribTest):
    def test_load_rotated(self):
        cubes = iris.load(
            tests.get_data_path(("GRIB", "rotated_uk", "uk_wrongparam.grib1"))
        )
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("rotated.cml",))

    def test_load_time_bound(self):
        cubes = iris.load(
            tests.get_data_path(("GRIB", "time_processed", "time_bound.grib1"))
        )
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("time_bound_grib1.cml",))

    def test_load_time_processed(self):
        cubes = iris.load(
            tests.get_data_path(("GRIB", "time_processed", "time_bound.grib2"))
        )
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("time_bound_grib2.cml",))

    def test_load_3_layer(self):
        cubes = iris.load(tests.get_data_path(("GRIB", "3_layer_viz", "3_layer.grib2")))
        cubes = iris.cube.CubeList([cubes[1], cubes[0], cubes[2]])
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("3_layer.cml",))

    def test_load_masked(self):
        gribfile = tests.get_data_path(
            ("GRIB", "missing_values", "missing_values.grib2")
        )
        cubes = iris.load(gribfile)
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("missing_values_grib2.cml",))

    def test_polar_stereo_grib1(self):
        cube = iris.load_cube(
            tests.get_data_path(("GRIB", "polar_stereo", "ST4.2013052210.01h"))
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("polar_stereo_grib1.cml",))

    def test_polar_stereo_grib2_grid_definition(self):
        cube = iris.load_cube(
            tests.get_data_path(
                (
                    "GRIB",
                    "polar_stereo",
                    "CMC_glb_TMP_ISBL_1015_ps30km_2013052000_P006.grib2",
                )
            )
        )
        self.assertEqual(cube.shape, (200, 247))
        pxc = cube.coord("projection_x_coordinate")
        self.assertAlmostEqual(pxc.points.max(), 4769905.5125, places=4)
        self.assertAlmostEqual(pxc.points.min(), -2610094.4875, places=4)
        pyc = cube.coord("projection_y_coordinate")
        self.assertAlmostEqual(pyc.points.max(), -216.1459, places=4)
        self.assertAlmostEqual(pyc.points.min(), -5970216.1459, places=4)
        self.assertEqual(pyc.coord_system, pxc.coord_system)
        self.assertEqual(
            pyc.coord_system.grid_mapping_name,
            "polar_stereographic",
        )
        self.assertEqual(pyc.coord_system.central_lat, 90.0)
        self.assertEqual(pyc.coord_system.central_lon, 249.0)
        self.assertEqual(pyc.coord_system.false_easting, 0.0)
        self.assertEqual(pyc.coord_system.false_northing, 0.0)
        self.assertEqual(pyc.coord_system.true_scale_lat, 60.0)

    def test_lambert_grib1(self):
        cube = iris.load_cube(tests.get_data_path(("GRIB", "lambert", "lambert.grib1")))
        self.assertCML(cube, _RESULTDIR_PREFIX + ("lambert_grib1.cml",))

    def test_lambert_grib2(self):
        cube = iris.load_cube(tests.get_data_path(("GRIB", "lambert", "lambert.grib2")))
        self.assertCML(cube, _RESULTDIR_PREFIX + ("lambert_grib2.cml",))

    def test_regular_gg_grib1(self):
        cube = iris.load_cube(
            tests.get_data_path(("GRIB", "gaussian", "regular_gg.grib1"))
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("regular_gg_grib1.cml",))

    def test_regular_gg_grib2(self):
        cube = iris.load_cube(
            tests.get_data_path(("GRIB", "gaussian", "regular_gg.grib2"))
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("regular_gg_grib2.cml",))

    def test_reduced_ll(self):
        cube = iris.load_cube(
            tests.get_data_path(("GRIB", "reduced", "reduced_ll.grib1"))
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("reduced_ll_grib1.cml",))

    def test_reduced_gg(self):
        cube = iris.load_cube(
            tests.get_data_path(("GRIB", "reduced", "reduced_gg.grib2"))
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("reduced_gg_grib2.cml",))

    def test_second_order_packing(self):
        cube = iris.load_cube(
            tests.get_data_path(
                ("GRIB", "grib1_second_order_packing", "GRIB_00008_FRANX01")
            )
        )
        self.assertCML(cube, _RESULTDIR_PREFIX + ("second_order_packing.cml",))

    def test_bulletin_headers(self):
        for byte_len in (40, 41):
            cube = iris.load_cube(
                tests.get_data_path(("GRIB", "bulletin", f"{byte_len}bytes.grib"))
            )
            self.assertCML(cube, _RESULTDIR_PREFIX + (f"bulletin_{byte_len}bytes.cml",))


@tests.skip_data
class TestIjDirections(tests.IrisGribTest):
    @staticmethod
    def _old_compat_load(name):
        filepath = tests.get_data_path(("GRIB", "ij_directions", name))
        cube = iris.load_cube(filepath)
        return cube

    def test_ij_directions_ipos_jpos(self):
        cubes = self._old_compat_load("ipos_jpos.grib2")
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("ipos_jpos.cml",))

    def test_ij_directions_ipos_jneg(self):
        cubes = self._old_compat_load("ipos_jneg.grib2")
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("ipos_jneg.cml",))

    def test_ij_directions_ineg_jneg(self):
        cubes = self._old_compat_load("ineg_jneg.grib2")
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("ineg_jneg.cml",))

    def test_ij_directions_ineg_jpos(self):
        cubes = self._old_compat_load("ineg_jpos.grib2")
        self.assertCML(cubes, _RESULTDIR_PREFIX + ("ineg_jpos.cml",))


@tests.skip_data
class TestShapeOfEarth(tests.IrisGribTest):
    @staticmethod
    def _old_compat_load(name):
        filepath = tests.get_data_path(("GRIB", "shape_of_earth", name))
        cube = iris.load_cube(filepath)
        return cube

    def test_shape_of_earth_basic(self):
        # pre-defined sphere
        cube = self._old_compat_load("0.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_0.cml",))

    def test_shape_of_earth_custom_1(self):
        # custom sphere
        cube = self._old_compat_load("1.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_1.cml",))

    def test_shape_of_earth_IAU65(self):
        # IAU65 oblate sphere
        cube = self._old_compat_load("2.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_2.cml",))

    def test_shape_of_earth_custom_3(self):
        # custom oblate spheroid (km)
        cube = self._old_compat_load("3.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_3.cml",))

    def test_shape_of_earth_IAG_GRS80(self):
        # IAG-GRS80 oblate spheroid
        cube = self._old_compat_load("4.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_4.cml",))

    def test_shape_of_earth_WGS84(self):
        # WGS84
        cube = self._old_compat_load("5.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_5.cml",))

    def test_shape_of_earth_pre_6(self):
        # pre-defined sphere
        cube = self._old_compat_load("6.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_6.cml",))

    def test_shape_of_earth_custom_7(self):
        # custom oblate spheroid (m)
        cube = self._old_compat_load("7.grib2")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_7.cml",))

    def test_shape_of_earth_grib1(self):
        # grib1 - same as grib2 shape 6, above
        cube = self._old_compat_load("global.grib1")
        self.assertCML(cube, _RESULTDIR_PREFIX + ("earth_shape_grib1.cml",))


class TestTimesGrib1:
    # Our codebase has support for many timeRangeIndicator values in GRIB1
    #  files, but we do not have files demonstrating these. This class
    #  generates appropriate GRIB1 files so that we can fully refactor the
    #  loading code while ensuring continued support for all possible
    #  scenarios.

    @pytest.fixture(params=[1, 2, 3, 4, 5, 10, 113, 118, 123, 124], autouse=True)
    # Note that the following values are not supported by Eccodes - it can
    #  not provide a startStep value unless the timeRangeIndicator is present
    #  in eccodes/definitions/grib1/localConcepts/edzw/stepType.def:
    #  [51, 114, 115, 116, 117, 125].
    def _get_time_range_file(self, request, tmp_path):
        save_file = tmp_path / "TestTimes.grib1"
        time_range_indicator = request.param

        # Make a file with 10 ascending time steps.
        with save_file.open("wb") as open_file:
            for time_step in range(10):
                grib_message = eccodes.codes_grib_new_from_samples("GRIB1")
                eccodes.codes_set_long(grib_message, "P1", time_step)
                eccodes.codes_set_long(grib_message, "P2", time_step + 1)
                eccodes.codes_set_long(
                    grib_message, "timeRangeIndicator", time_range_indicator
                )
                eccodes.codes_write(grib_message, open_file)
                eccodes.codes_release(grib_message)

        self.time_range_indicator = time_range_indicator
        self.save_file = save_file

    def test_time_range(self):
        cube = iris.load_cube(self.save_file)
        tests.IrisGribTest().assertCML(
            cube, _RESULTDIR_PREFIX + (f"time_range_{self.time_range_indicator}.cml",)
        )


@pytest.fixture
def polar_stereo_south_grib1(tmp_path):
    path_original = Path(
        tests.get_data_path(("GRIB", "polar_stereo", "ST4.2013052210.01h"))
    )
    name_modified = path_original.name.replace("ST4", "ST4_south")
    path_modified = tmp_path / name_modified
    with path_original.open("rb") as file_original:
        gid = eccodes.codes_grib_new_from_file(file_original)
        eccodes.codes_set(gid, "projectionCentreFlag", 1)
        with path_modified.open("wb") as file_modified:
            eccodes.codes_write(gid, file_modified)
        eccodes.codes_release(gid)
    return path_modified


def test_polar_stereo_grib1_south(polar_stereo_south_grib1):
    cube = iris.load_cube(polar_stereo_south_grib1)
    tests.IrisGribTest().assertCML(
        cube, _RESULTDIR_PREFIX + ("polar_stereo_grib1_south.cml",)
    )


def test_reduced_gg_grib1():
    file_path = Path(eccodes.codes_samples_path()) / "reduced_gg_sfc_grib1.tmpl"
    cube = iris.load_cube(file_path)
    tests.IrisGribTest().assertCML(cube, _RESULTDIR_PREFIX + ("reduced_gg_grib1.cml",))


if __name__ == "__main__":
    tests.main()
