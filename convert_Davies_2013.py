#!/usr/bin/env python3

import csv
import numpy
import netCDF4

# Read CSV file
ni,nj = 180,90
mean_HF = numpy.zeros((nj,ni))
median_HF = numpy.zeros((nj,ni))
error_HF = numpy.zeros((nj,ni))
with open('ggge20271-sup-0003-Data_Table1_Eq_lon_lat_Global_HF.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == 'Longitude': continue
        lon, lat = int(row[0]), int(row[1])
        i, j = int(( 179 + lon ) /2), int(( 89 + lat )/2)
        mn, md, er = float(row[2]), float(row[3]), float(row[4])
        #print(lon,lat,i,j,mn,md,er)
        mean_HF[j,i], median_HF[j,i], error_HF[j,i] = mn, md, er

# Convert heat flow to W/m2 (data is in mW/m2)
mean_HF, median_HF, error_HF = 1.e-3*mean_HF, 1.e-3*median_HF, 1.e-3*error_HF

# Coordinates for cells
lon, lat = numpy.arange(-179,180,2), numpy.arange(-89,90,2)
lon_edge, lat_edge = numpy.arange(-180,181,2), numpy.arange(-90,91,2)

# Create netcdf file
with netCDF4.Dataset('ggge20271-sup-0003-Data_Table1_Eq_lon_lat_Global_HF.nc', 'w', format='NETCDF3_64BIT') as ncf:
    # Metadata
    ncf.title = 'Gridded geothermal heat flow from Davies, 2013'
    ncf.reference = 'Davies, J. Huw, 2013: Global map of solid Earth surface heat flow. Geochemistry, Geophysics, Geosystems, 14 (10), pp 4608--4622. doi:10.1002/ggge.20271'
    ncf.reference_url = 'http://dx.doi.org/10.1002/ggge.20271'
    ncf.history = 'Converted from CSV files using script convert_Davies_2013.py available at https://github.com/adcroft/convert_Davies_2013'
    ncf.version = '1.1'
    # Dimensions
    ncf.createDimension('lon', 180)
    ncf.createDimension('lat', 90)
    ncf.createDimension('nv', 2)
    # Latitude, longitude of cell centers
    nc_lon = ncf.createVariable('lon', 'f', ('lon',))
    nc_lon.units = 'degrees_east'
    nc_lon.standard_name = 'longitude'
    nc_lon.long_name = 'Longitude'
    nc_lon.bounds = 'lonbnd'
    nc_lat = ncf.createVariable('lat', 'f', ('lat',))
    nc_lat.units = 'degrees_north'
    nc_lat.standard_name = 'latitude'
    nc_lat.long_name = 'Latitude'
    nc_lat.bounds = 'latbnd'
    # Latitude, longitude of cell corners
    nc_lonbnd = ncf.createVariable('lonbnd', 'f', ('lon','nv',))
    nc_lonbnd.units = 'degrees_east'
    nc_lonbnd.standard_name = 'longitude'
    nc_latbnd = ncf.createVariable('latbnd', 'f', ('lat','nv',))
    nc_latbnd.units = 'degrees_north'
    nc_latbnd.standard_name = 'latitude'
    # Data variables
    nc_mean_HF = ncf.createVariable('mean_HF', 'f', ('lat','lon'))
    nc_mean_HF.units = 'W m-2'
    nc_mean_HF.standard_name = 'upward_geothermal_heat_flux_at_sea_floor'
    nc_mean_HF.long_name = 'Geothermal heat flow'
    nc_mean_HF.cell_methods = 'area: mean'
    nc_median_HF = ncf.createVariable('median_HF', 'f', ('lat','lon'))
    nc_median_HF.units = 'W m-2'
    nc_median_HF.standard_name = 'upward_geothermal_heat_flux_at_sea_floor'
    nc_median_HF.long_name = 'Geothermal heat flow'
    nc_median_HF.cell_methods = 'area: median'
    nc_error_HF = ncf.createVariable('error_HF', 'f', ('lat','lon'))
    nc_error_HF.units = 'W m-2'
    nc_error_HF.long_name = 'Error estimate in geothermal heat flow'
    # Write data
    nc_lon[:] = lon[:]
    nc_lat[:] = lat[:]
    nc_lonbnd[:,0] = lon_edge[:-1]
    nc_lonbnd[:,1] = lon_edge[1:]
    nc_latbnd[:,0] = lat_edge[:-1]
    nc_latbnd[:,1] = lat_edge[1:]
    nc_mean_HF[:,:] = mean_HF[:,:]
    nc_median_HF[:,:] = median_HF[:,:]
    nc_error_HF[:,:] = error_HF[:,:]
