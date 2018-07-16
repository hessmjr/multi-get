import sys, os, time, shutil
import urlparse
import threading
import requests


BYTES = 1024


def parse_filename(url):
    """
    Parses the filename from the given URL
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
    chunked downloading.
    """

    def __init__(self, url, num_chunk=4, chunk_size=1, verbose=False):
        self.url = url
        self.num_chunk = num_chunk
        self.chunk_size = chunk_size
        self.verbose = verbose

        # container for the total file size, retrieved from first request
        self.total_size = None

        # parse the filename from the URL
        self.filename = parse_filename(url)

    def get(self):
        """
        Retrieves file from stored URL utilizing parallel download streams.
        """
        count = -1

        # calculate the total size
        file_size = self.num_chunk * self.chunk_size

        if self.verbose:
            print 'Estimated download size: %d' % file_size

        # iterate through entire calculated file size with the specified chunk
        # size, create new threads to process the download in parallel
        for location in range(0, file_size, self.chunk_size):
            count += 1

            if self.verbose:
                print 'Creating download thread %d' % count

            # create thread arguments and new thread with function to target
            # for processing and being processing
            thread_args = (location, count)
            thread = threading.Thread(target=self._download, args=thread_args)
            # thread.daemon = True  # used to allow main app to exit
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

                # copy the temporary file into the final files
                # delete the temporary file once completed
                shutil.copyfileobj(open(temp_path, 'rb'), open_file)
                os.remove(temp_path)

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
        print gap
        headers = {'Range': 'bytes=%d-%d' % gap}
        req = requests.get(self.url, headers=headers, stream=True)

        if self.verbose:
            print 'Requesting %s' % filepath

        # write the requested chunk to the temporary file
        with open(filepath, 'wb') as open_file:
            for chunk in req.iter_content(chunk_size=BYTES):
                if chunk:
                    open_file.write(chunk)

        if self.verbose:
            print 'Downloaded %s' % filepath
