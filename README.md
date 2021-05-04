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
$ usage: scraping.py [-h] [--p P] [--s {csv,json}] [--d {simple,deep}] [--o O]
                   [--nopd] [--nopb]

CSGO Web Scraping Options

optional arguments:
  -h, --help            show this help message and exit
  --p P, --pages P      number of pages to scrap (0 == automatic)
  --s {csv,json}, --save-type {csv,json}
                        save type (csv or json)
  --d {simple,deep}, --depth {simple,deep}
                        scraping depth
  --o O, --output O     define output file name
  --nopd, --no-process-data
                        don't processes the data
  --nopb, --no-progress-bar
                        don't show progress bar

```