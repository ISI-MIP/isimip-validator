# isimip-validator

Checks whether filenames follow the ISIMIP protocol as presented on https://protocol.isimip.org.

## Setup

The software can be installed using `pip` and `git`

```
pip install git+https://github.com/ISI-MIP/isimip-validator
```

## Usage

In order to check a file from a given `simulation_round` and `sector` use:

```
isimip-validator <simulation_round> <sector> <path>
```

E.g., for a file in `ISIMIP3a` and `water_global` use:

```
isimip-validator ISIMIP3a water_global lpjml_gswp3_obsclim_histsoc_default_qtot_global_annual_1901_1910.nc
```

You can also use complete pathes and `isimip_publisher` will walk directory hirarchies searching for files (much like `find`).
