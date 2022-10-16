import requests
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

def vlun(urltarget):
    url_target = urltarget    
    try:
        status_1 = requests.options(url=url_target + '/*~1****/a.aspx', verify=False)  # an existed file/folder
        status_2 = requests.options(url=url_target + '/l1j1e*~1****/a.aspx', verify=False)  # not existed file/folder
        if status_1.status_code == 404 and status_2.status_code == 200: 
            print(str(url_target)+' is vulerable')
            with open(outputfile, 'a') as f:
                try:
                    f.write(str(url_target) + '' + '\n')
                except:
                    pass
        else:
            pass
            #print(str(url_target)+' is no vulerable')
    except Exception:
        pass

def Scanner(url_file,max_thread,output_file):
    url_list = []
    if url_file is not None:
        url_list = list(set([i.replace("\n", "") for i in open(str(url_file), "r").readlines()]))
    else:
        exit()
    with open(outputfile, 'w'):
        pass
    l=[]
    p = ThreadPoolExecutor(max_thread)
    for url in url_list:
        obj = p.submit(vlun, url,)
        l.append(obj)
    p.shutdown()


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
    global outputfile
    try:
        if args.url_file and args.max_threads and args.output_file:
            print(usageexample+'url_file:'+args.url_file+'| max_threads:'+str(args.max_threads)+'| output_file:'+args.output_file)
            outputfile = args.output_file
            Scanner(args.url_file,args.max_threads,outputfile)
        else:
            print(usageexample)
    except Exception as e:
        print(e)
