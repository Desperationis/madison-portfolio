# Art portfolio website

Reads image files and optional JSON description files and generates 1) a gallery 2) independent webpage for every image.

Production version is viewable [here](https://plantmonster.net/art-portfolio/).

### Usage

* Install python3
* Put artwork under some folder
* Artwork must be named with the following format: `art12_30_12_2023.png` (or jpg)
* You can have an optional file at `art12_30_12_2023.json` with a JSON document containing the following data:

```
{
    "description": "description here"
    "license": "copyleft"
}
```

* Copy `config.json.placeholder` into `config.json`
* Change `plantmonster.net` specific urls to whatever your webserver uses
	* Yes, I'm that lazy
* Run generate.py
* Copy files all `*.png`, `*.css`, `*.html`, and `pieces/*` files to a web accessible folder
* I automated my deployments like so:

```
#!/bin/sh
set -e

DATE=`date`
echo "Date is: $DATE"
cd this-repo-dir
python3 generate.py
cp -r *.png *.css pieces/ /path/to/webroot/
cp portfolio.html /path/to/webroot/index.html
```
