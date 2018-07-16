# Multi Get Web Client
Python web client that downloads a file in chunks with a specified range.

## Usage
Can be operated in two ways, either on local machine or via Vagrant virtual
machine using VirtualBox.

### Local Setup
Requires Python version 2.7 and `pip` to be installed locally.  Execute install
with the following in the project root directory:
```bash
$ bash install.sh
```

### Vagrant Setup
Requires [Vagrant](https://www.vagrantup.com/) installed.  From project root
directory execute the following:
```bash
$ vagrant up
$ vagrant ssh
```


### Command Line
After project dependencies are installed run with the following command:
```
$ multiget http://httpbin.org/image/jpeg
File download complete.

$ multiget http://httpbin.org/image/jpeg --size=1 --num=1 --verbose
Requesting URL: http://httpbin.org/image/jpeg
Number of chunks: 1
Size of chunks: 1048576
Estimated total: 1
Estimated download size: 1048576
Creating download thread 0
Requesting /home/vagrant/multi-get/jpeg_part_0
Downloaded /home/vagrant/multi-get/jpeg_part_0
Downloads complete, file merging at /home/vagrant/multi-get/jpeg
Files merged and deleted.  File saved at /home/vagrant/multi-get/jpeg
File download complete.
```

Command line usage and options:
```
Usage: multiget [OPTIONS] URL

  Retrieves a file from the given URL.  URL must be valid format.  File
  retrieved in chunks, range and size of chunks can be specified.

Options:
  --num INTEGER    Number of file chunks  [default: 4]
  --size INTEGER   File chunk size, in MiB  [default: 1]
  --total INTEGER  Total file download size, in MiB.  Overrides size of the
                   download chunks, if specified.  Negative value downloads
                   entire file.
  --verbose        Turn on logging
  --version        Show the version and exit.
  --help           Show this message and exit.
```

## Testing
Unit tests are setup to be run locally and via Travis.  In order to process
tests, from project root directory execute:
```
python -m unittest discover -v
```

## Design

Vagrant used to contain Python's

use Docker to contain all python crap...
maybe use travis to showcase CI with tests passing

Single python file
 - cli
 - creates connection to url specified
 - downloads chunks for given range (what if no range) in parallel
 - args for chunk size (default 1 MB)
 - args for num chunks
 - args for total download size


test file
 - bad url
 - good url and incorrect range
 - good url and no range
 - good url and range
 - bad args
    - can't have num chunks and total download  (overrides)
 - check if total size downloaded equals total size requested
