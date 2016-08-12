.. iris-grib documentation master file, created by
   sphinx-quickstart on Fri May 13 11:48:28 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The documentation for iris-grib
===============================

The library ``iris-grib`` provides functionality for converting between weather and
climate datasets that are stored as GRIB files and :class:`Iris cubes <iris.cube.Cube>`.
GRIB files can be loaded as Iris cubes using ``iris-grib`` so that you can use Iris
for analysing and visualising the contents of the GRIB files. Iris cubes can be saved to
GRIB files using ``iris-grib``.

The contents of ``iris-grib`` represent the former grib loading and saving capabilities
of :mod:`Iris <iris>` itself. These capabilities have been separated into a discrete library
so that Iris becomes less monolithic as a library.


Loading
-------

To use ``iris-grib`` to load existing GRIB files we can make use of the
:func:`~iris_grib.load_cubes` function::

    >>> import os
    >>> import iris_sample_data
    >>> import iris_grib
    >>> cubes = iris_grib.load_cubes(os.path.join(iris_sample_data.path,
                                                  'polar_stereo.grib2'))
    >>> print cubes
    <generator object load_cubes at 0x7f69aba69d70>

As we can see, this returns a generator object. The generator object may be iterated
over to access all the Iris cubes loaded from the GRIB file, or converted directly
to a list::

    >>> cubes = list(cubes)
    >>> print cubes
    [<iris 'Cube' of air_temperature / (K) (projection_y_coordinate: 200; projection_x_coordinate: 247)>]

.. note::
    There is no functionality in iris-grib that directly replicates
    ``iris.load_cube`` (that is, load a single cube directly rather than returning
    a length-one `CubeList`. Instead you could use the following, assuming that the
    GRIB file you have loaded contains data that can be loaded to a single cube::

        >>> cube, = list(cubes)
        >>> print cube
        air_temperature / (K)               (projection_y_coordinate: 200; projection_x_coordinate: 247)
             Dimension coordinates:
                  projection_y_coordinate                           x                             -
                  projection_x_coordinate                           -                             x
             Scalar coordinates:
                  forecast_period: 6 hours
                  forecast_reference_time: 2013-05-20 00:00:00
                  pressure: 101500.0 Pa
                  time: 2013-05-20 06:00:00

    This makes use of an idiom known as variable unpacking.


Saving
------

To use ``iris-grib`` to save Iris cubes to a GRIB file we can make use of the
:func:`~iris_grib.save_grib2` function::

    >>> iris_grib.save_grib2(my_cube, 'my_file.grib2')

.. note::
    As the function name suggests, only saving to GRIB2 is supported.


Indices and tables
==================

Contents:

.. toctree::
   :maxdepth: 3

   ref/iris_grib
   ref/message/message
   ref/grib_phenom_translation/grib_phenom_translation


See also:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

