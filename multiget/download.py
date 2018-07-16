import sys, os, time, shutil
import urlparse
import threading
import requests


BYTES = 1024


def parse_filename(url):
    """
    Parses the filename from the given URL.  Assumes valid URL given.
    """
    # extract the URL path
    url_path = urlparse.urlparse(url).path
    filename = url_path.split('/')[-1]

    # make loose assumption the file name is for an HTML page
    if len(filename) < 1:
        filename = 'index.html'

    return filename


class Request():
    """
    Class used to encapsulate the file request and processing for parallel
    chunked downloading.  Assumes arguments have been validated, except for URL
    validity, will ensure that when making request.
    """

    def __init__(self, url, num_chunk=4, chunk_size=1*(BYTES**2), verbose=False):
        self.url = url
        self.num_chunk = num_chunk
        self.chunk_size = chunk_size
        self.verbose = verbose

        # thread pool, used for tracking threads, number of threads, and testing
        self.threads = []

        # parse the filename from the URL
        self.filename = parse_filename(url)

    def get(self):
        """
        Retrieves file from stored URL utilizing parallel download streams.
        """
        # calculate the total size
        file_size = self.num_chunk * self.chunk_size

        if self.verbose:
            print 'Estimated download size: %d' % file_size

        # iterate through entire calculated file size with the specified chunk
        # size, create new threads to process the download in parallel
        for location in range(0, file_size, self.chunk_size):
            count = len(self.threads)

            if self.verbose:
                print 'Creating download thread %d' % count

            # create thread arguments and new thread with function to target
            # for processing and being processing
            thread_args = (location, count)
            thread = threading.Thread(target=self._download, args=thread_args)
            self.threads.append(thread)
            thread.start()

        # wait until all active threads are complete
        while threading.active_count() > 1:
            time.sleep(0.1)

        # create final file path that all downloads will merge into
        filepath = os.path.join(os.getcwd(), self.filename)

        if self.verbose:
            print 'Downloads complete, file merging at %s' % filepath

        # iterate through all temp files and write to final file
        with open(filepath, 'wb') as open_file:
            for i in range(self.num_chunk):

                # recreate the temporary file path to get chunk from
                temp_name = self.filename + '_part_%d' % i
                temp_path = os.path.join(os.getcwd(), temp_name)

                # check if temp file exists before trying to write it
                if not os.path.isfile(temp_path):
                    continue

                # copy the temporary file into the final files
                # delete the temporary file once completed
                shutil.copyfileobj(open(temp_path, 'rb'), open_file)
                os.remove(temp_path)

        # if no file was written then remove
        if os.path.getsize(filepath) < 1:
            os.remove(filepath)

            if self.verbose:
                print 'No data to write to file for %s' % self.filename

        if self.verbose:
            print 'Files merged and deleted.  File saved at %s' % filepath

    def _download(self, location, count):
        """
        Internal method used by request threads to make download requests
        """
        # build file location to write this chunk in
        filename = self.filename + '_part_%d' % count
    	filepath = os.path.join(os.getcwd(), filename)

        # build GET request by calculating the next range of bytes to retrieve
        # building the request headers and making the streaming GET request
        gap = (location, location + self.chunk_size - 1)
        headers = {'Range': 'bytes=%d-%d' % gap}
        resp = requests.get(self.url, headers=headers, stream=True)

        if self.verbose:
            print 'Requesting %s' % filename

        # if request was not HTTP OK then stop proceeding
        if resp.status_code >= 300:
            if self.verbose:
                print 'Invalid response code: %d' % resp.status_code
            return

        # write the requested chunk to the temporary file
        with open(filepath, 'wb') as open_file:
            for chunk in resp.iter_content(chunk_size=BYTES):
                if chunk:
                    open_file.write(chunk)

        if self.verbose:
            print 'Downloaded %s' % filepath
