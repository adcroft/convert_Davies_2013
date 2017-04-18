# convert_Davies_2013

For converting CSV data in supplemental material of Davies (2013) to netcdf format.

Reference:

Davies, J. Huw, 2013: Global map of solid Earth surface heat flow. Geochemistry, Geophysics, Geosystems, 14 (10), pp 4608--4622. [doi:10.1002/ggge.20271](http://dx.doi.org/10.1002/ggge.20271)

## Usage

```bash
make
```

`make` will invoke the following steps:
- Download CSV file of heat flow data
- Convert CSV file to a netcdf file
- Check the md5sums of files are correct

## Conda environment

The netcdf file is created using the netCDF4 python package. If you have trouble reproducing the netcdf file, or running the python, try the conda environment file:
```bash
conda env create -f conda_env.yml
source activate davies_py3
make
```
