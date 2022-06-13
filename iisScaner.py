import requests
import sys
import threading
from queue import Queue
from argparse import ArgumentParser
from datetime import datetime

def vlun(q,of):
    while q.empty() is not True:
        url_target = q.get()    
        try:
            status_1 = requests.options(url_target + '/*~1****/a.aspx')  # an existed file/folder
            status_2 = requests.options(url_target + '/l1j1e*~1****/a.aspx')  # not existed file/folder
            if status_1.status_code == 404 and status_2.status_code == 200:
                with open(of, 'a') as f:
                        try:
                            print(str(url_target)+' is vulerable')
                            f.write(str(url_target) + '' + '\n')
                        except:
                            pass
            else:
                print(str(url_target)+' is no vulerable')
        except Exception:
            pass
        q.task_done()
def Scanner(url_file,max_thread,output_file):
    url_list = []
    global q
    if url_file is not None:
        url_list = list(set([i.replace("\n", "") for i in open(str(url_file), "r").readlines()]))
    else:
        exit()
    with open(output_file, 'w'):
        pass
    
    q = Queue() 
    for url in url_list:
        q.put(url)
    for index in range(max_thread):
        thread = threading.Thread(target=vlun, args=(q,output_file))
        # thread.daemon = True
        thread.start()
    q.join()

if __name__ == '__main__':
    usageexample = '''

██╗██╗░██████╗░██████╗░█████╗░░█████╗░███╗░░██╗███████╗██████╗░
██║██║██╔════╝██╔════╝██╔══██╗██╔══██╗████╗░██║██╔════╝██╔══██╗
██║██║╚█████╗░╚█████╗░██║░░╚═╝███████║██╔██╗██║█████╗░░██████╔╝
██║██║░╚═══██╗░╚═══██╗██║░░██╗██╔══██║██║╚████║██╔══╝░░██╔══██╗
██║██║██████╔╝██████╔╝╚█████╔╝██║░░██║██║░╚███║███████╗██║░░██║
╚═╝╚═╝╚═════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
    \nExample: python3 iisScaner.py -t 100 -f url.txt -o result.txt\n'''
    parser = ArgumentParser(add_help=True, usage=usageexample, description='A IIS Short Name Scanner.')
    parser.add_argument('-f', '--url-file', dest="url_file", help="Example: url.txt")
    parser.add_argument('-t', '--thread', dest="max_threads", nargs='?', type=int, default=1, help="Max threads")
    parser.add_argument('-o', '--output-file', dest="output_file", help="Example: result.txt")
    args = parser.parse_args()
    try:
        if args.url_file and args.max_threads and  args.output_file:
            print(usageexample+'url_file:'+args.url_file+'| max_threads:'+str(args.max_threads)+'| output_file:'+args.output_file)
            Scanner(args.url_file,args.max_threads,args.output_file)
        else:
            print(usageexample)
    except Exception as e:
        print(e)

