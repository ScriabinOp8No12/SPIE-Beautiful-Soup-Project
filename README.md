Looks like it properly scrapes the data from the 2024 Exhibitions!  
It's still a bit hard to tell if it works because most of them have no booth number, and they don't have 
company descriptions yet.   However, I checked a few outputs randomly in the csv output, and they seem to be 
correct (all classes, urls, and company names are correct)

Added tqdm progress bar on 4-21-23.  Trick was not using tqdm on the inner for loop when iterating otherwise the
output is multiple progress bars updating instead of just one progress bar.

