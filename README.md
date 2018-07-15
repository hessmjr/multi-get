# Multi Get Web Client
Python web client that downloads a file in chunks with a specified range.

## Usage

Run directly or run on Docker
 - run install if local, requires...

 - need Docker installed and running
 - run docker commands...


## Testing

## Design

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
