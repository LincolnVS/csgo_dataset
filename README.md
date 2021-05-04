# CSGO Scraping 
[![version](https://img.shields.io/badge/Version-Beta%200.2-red?style=flat-square)]()
[![license-apache](https://img.shields.io/github/license/lincolnvs/csgo_dataset?logo=apache&logoColor=white&style=flat-square)]() 
[![made-with-python](https://img.shields.io/pypi/pyversions/webdriver-manager?logo=python&logoColor=white&style=flat-square)]() 

## About
[None]

## Context & Environment
The program was developed and tested on WSL 2. The same bash commands should work on a machine running a unix-based OS (e.g., Ubuntu).

### **Installation**

It is recommended to use python 3.7 and a virtual environment (e.g., virtualenv, venv, and conda). To install the required packages, use the following command:

```console
$ pip install -r requeriments.txt
```

## Usage

In case you need help with the parameters, just run the command below:

```console
$ python scraping.py -h
usage: scraping.py [-h] [--pages PAGES] [--save-type {csv,json}][--scrap-type {simple,deep}] [--output OUTPUT] [--no-process-data] [--no-progress-bar]

CSGO Web Scraping Options

optional arguments:
  -h, --help                    show this help message and exit
  --pages PAGES, --p            number of pages to scrap (0 == automatic)
  --save-type {csv,json}, --s   save type (csv or json)
  --depth {simple,deep}, --d    scraping depth
  --output OUTPUT, --o          define output file name
  --no-process-data, --nopd     don't processes the data
  --no-progress-bar, --nopb     don't show progress bar

```