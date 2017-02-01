# Makefile for downloading and converting geothermal heat flow data from Davies, 2013.

CSV_FILE = ggge20271-sup-0003-Data_Table1_Eq_lon_lat_Global_HF.csv
NC_FILE = $(CSV_FILE:.csv=.nc)
MD5_FILE = md5sums.txt

all: check

# Download CSV file from supplemental material
$(CSV_FILE):
	wget -O $@ "http://onlinelibrary.wiley.com/store/10.1002/ggge.20271/asset/supinfo/$(CSV_FILE)?v=1&s=119fc3a6ef4b4e39e73d4b0752bc267bb663326d"

# Convert CSV file to netcdf
$(NC_FILE): $(CSV_FILE)
	python3 convert_Davies_2013.py

# Create md5 checksums file only if missing
$(MD5_FILE): | $(CSV_FILE) $(NC_FILE)
	md5sum $| > $@

# Check that md5 checksums match after creating netcdf file
check: $(NC_FILE) | $(MD5_FILE)
	md5sum -c $(MD5_FILE)
