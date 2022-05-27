# Thesis Project
Feel free to fork this and use as a starting point for your research.

Contact me at sarah.schmidt714@gmail.com if you are interested in getting more detail about this project, either the 
sources or just questions you have about my research.

Each file title corresponds to the exact video title and was used to match up the transcript files to the feature files 
as well as the files that were created for something like the sentiment analysis piece.

# Original video sources
The file `misc/list-of-video-sources.csv` contains a list of the videos in this data set and the URL where I 
found them.

# Raw transcript data
`data/genuine/` and `data/misinformation/` contain the raw transcripts generated by Happy Scribe or made available as 
an open transcript copied and pasted directly from YouTube.

# MeSH keyword data

A list of MeSH keywords for each video is under `data/keywords/`. These were generated using the 
[MeSH website](https://meshb.nlm.nih.gov/MeSHonDemand). Longer transcripts were segmented into at most 10,000 
characters then run in the MeSH on Demand tool. The resulting keywords copied and pasted into one spreadsheet for each 
video and then the VBA macro in `cleanup-macro.xlsm` was used to merge duplicate keywords.

# Classifier code

All the runnable code used in the experiment for classification is found under `classifiers/`.

## To run a classifier program
1. Uncomment the desired features you want to use in your features set in `build_labeled_feature_set` function.
2. Run program `$ python classifiers/classifier-name.py`

# Feature set
Feature sets for each video in the data set are found under `data/features/`. Each is stored in a CSV file.

## Updating existing feature set files

Run `python services/features.py` to add the sentiment analysis results to the feature sets.

New files overwrite the current ones at `data/features/`.

## Raw transcript

The raw transcript data has been base64 encoded for reasons.

Run services/base64decode.py to decode it back to the raw transcript for viewing and further research.

## Questions

If you have questions or are having issues with running the programs, open an issue.

## Citation

If you end up using this repository for your research, please include my paper in your references. 

Paper citation: 

TBA