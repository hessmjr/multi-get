# Multi Get Web Client  [![Build Status](https://travis-ci.org/hessmjr/multi-get.svg?branch=master)](https://travis-ci.org/hessmjr/multi-get)
Python web client that downloads a file in chunks with a specified range.

## Usage
Can be operated in two ways, either on local machine or via Vagrant virtual
machine using VirtualBox.

### Vagrant Setup
Requires [Vagrant](https://www.vagrantup.com/) installed.  From project root
directory execute the following:
```
$ vagrant up
$ vagrant ssh
```

When finished utilizing, destroy Vagrant box with the following
```
$ vagrant destroy
```

### Local Setup
Requires Python version 2.7 and `pip` to be installed locally.  Execute install
with the following in the project root directory **(may require sudo)**:
```
$ python -m pip install -e .
```

### Command Line Examples
After project dependencies are installed, run with the following command:
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
$ multiget --help
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

The number of chunks will dictate the number of parallel processes to download
the file with.  Specifying the chunk size will dictate how much each parallel
process will download.  If the number and size is greater than the file size
the threads will still be created although nothing downloaded.  Total file size
dictates how much of the entire file to download.  It overwrites the size of
each chunk and preserves the number of parallel chunks to download.  A total
size greater than the file will only push the parallel processes to run longer
than otherwise would require.  Setting total to a negative value (-1) encourages
the entire file to be downloaded at the specified number of chunks.

## Testing
Unit tests are setup to be run locally and via Travis.  In order to process
tests, from project root directory execute:
```
$ python -m unittest discover -v
```
