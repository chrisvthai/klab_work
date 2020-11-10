# klab_work
Work done during 1st lab rotation with Protein-ML group with Sagar and Sijian, which was mainly dataset curation for clan PA proteins. Below is a short description of all of the scripts.

## VAST_scraper(_2).ipynb
First trial at dataset curation, in which the VAST tool was used. The script uses Selenium to query VAST and return a list of similar structure neighbors according to VAST, with sequence identity and alignment length thresholds. This approach did not pan out, as it was creating less diverse datasets than using DALI server.

## dali_scraper.py
Defines the `get_dali_query()` function, which queries the DALI server and waits for a response before extracting a list of all matching PDB90 protein chains.

Also includes the first round of nearest neighbors search, which uses a dictionary representing clan PA proteins.

## dali.sh & dali_scraper_amarel.py
Adaptations of the original dali_scraper.py code in order to run batch jobs of the scraper on Amarel. Takes in a directory called 'neighbors', which is a bunch of text files representing the list of query proteins. Amarel is used to return a second-round nearest-neighbors search, after the initial first round was done on one computer.
