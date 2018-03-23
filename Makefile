# Makefile for downloading and converting geothermal heat flow data from Davies, 2013.

CSV_FILE = ggge20271-sup-0003-Data_Table1_Eq_lon_lat_Global_HF.csv
NC_FILE = $(CSV_FILE:.csv=.nc)
MD5_FILE = md5sums.txt

all: check

# Download CSV file from supplemental material
$(CSV_FILE):
	wget -O $@ "https://agupubs.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fggge.20271&attachmentId=80046787"

# Convert CSV file to netcdf
$(NC_FILE): $(CSV_FILE)
	python convert_Davies_2013.py

# Create md5 checksums file only if missing
$(MD5_FILE): | $(CSV_FILE) $(NC_FILE)
	md5sum $| > $@

# Check that md5 checksums match after creating netcdf file
check: $(NC_FILE) | $(MD5_FILE)
	md5sum -c $(MD5_FILE)
