# Lung Digitiser

A Python application to sample discrete points across the surfaces of Finite Element lung meshes
and export them as digitised coordinates and corresponding group classes.

Requirements
------------

* Python 3.9
* OpenCMISS-ZINC 3.5.0 or above `pip install opencmiss.zinc`_.
* OpenCMISS-Utils 0.4.0 or above `pip install opencmiss.utils`_.
* CMGUI 3.0.0 or above.

Running
-------
First, you will need to modify the current configuration files in `tests/resources` or create your own 
configuration file.

For example:

    {
        "root": "Y:\\lung\\Data",
        "dataset": "Human_Aging",
        "subjects": [
                        "AGING001",
                        "AGING002",
                        "AGING004",
                        "AGING006",
                        "AGING010"
                    ],
        "volume": "Insp",
        "sub_dir": "Lung\\SurfaceFEMesh"
    }

Then run `src/digitiser.py <input-config> <path/to/cmgui.exe> <output-dir>` 
