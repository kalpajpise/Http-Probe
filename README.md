# HTTP STREAM PROBE

# Introduction

This program is used to extract the HTTP metadata and store output file i.e Excel, CSV, JSON.

# Developer Guide

**Author:** Kalpaj Pise  
**Organization:** Group Data and Analytics (Aditya Birla Group)*

## How to Run:

Step 1: Create a virtual environment

`virtualenv --python=python3 venv`
or
`python3 -m venv venv`

Step 2 : Activate the virtual environment

`source venv/bin/activate`

Step 3: Install the dependencies from requirement file

`pip install -r requirement`

Step 4: Run the stream bitrate stats module

`python -m stream_bitrate_stats <file_name>`

Supported input file format:

1. CSV
2. XLSX or XLS

The input file should have the column name **'Streams'**.

Sample Template (CSV or excel):

```
Streams
http://localhost:5501/mystream1
http://localhost:5501/mystream2
```

## The HTTP Probe program usage:

~~~~
usage: __main__.py [-h] [-n] [-v] [-s {video,audio}] [-a {time,gop}]
                   [-c CHUNK_SIZE] [-o OUTPUT_DIR]
                   [-output_format {csv,excel,tsv,json}]
                   input_file

Stream Metadata Parser

positional arguments:
  input_file            Input File for list of streams

optional arguments:
  -h, --help            show this help message and exit
  -n, --dry-run         Do not run command, just show what would be done
                        (default: False)
  -v, --verbose         Show verbose output (default: False)
  -s {video,audio}, --stream-type {video,audio}
                        Stream type to analyze (default: video)
  -a {time,gop}, --aggregation {time,gop}
                        Window for aggregating statistics, either time-based
                        (per-second) or per GOP (default: time)
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        Custom aggregation window size in seconds. Probe time
                        in gop (default: 2.0)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory (default: output)
  -output_format {csv,excel,tsv,json}, --output-format {csv,excel,tsv,json}
                        output in which format (default: excel)
                   
   ~~~~
