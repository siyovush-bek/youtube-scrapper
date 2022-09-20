# youtube-scrapper
Youtube Scrapper

1. Create a virtual environment:
```shell
python3 -m venv env
```
2. Activate the virtual environment:
```shell
source env/bin/activate (linux, macOS)
source env/Scripts/activate (windows, using git bash)
```
3. Install dependencies
```shell
pip install -r requirements.txt
```
3. Create input file (e.g. input.txt): each line must consist of SEARCH QUERY and NAME for output csv file seperated with a whitespace.
Words in search query must be seperated with '+' symbol
here how it would look like:

ted+talks ted
async+tasks async
fastapi+beginner's+tutorial fastapi

4. Run the script

```shell
python main.py input.txt
```

By default script fetches 30 videos from search query, to change this 
you can set env variable MAXRESULTS with your prefered number
just before runing the script do like this

```shell
export MAXRESULTS=35
```
and script will fetch over 35 videos
