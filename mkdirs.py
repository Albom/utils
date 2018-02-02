import os

for year in range(1960, 2019):
	if not os.path.exists(str(year)):
		os.makedirs(str(year))
