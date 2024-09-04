import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

paser = argparse.ArgumentParser(description='Get the size of index of a website')
paser.add_argument('-U', '--url', dest='url', type=str, help='URL of the website')
paser.add_argument('-T', '--threads', dest='threads_num', type=int, default=10, help='Number of threads to use')
args = paser.parse_args()

def get_file_size(url):
    try:
        head_response = requests.head(url, timeout=5)
        head_response.raise_for_status()
        if 'Content-Length' in head_response.headers:
            size = int(head_response.headers['Content-Length'])
            print(f"File: {url}, Size: {size} bytes")
            return size
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f"Connection error for file {url}: {e}")
    except requests.RequestException as e:
        print(f"Request failed for file {url}: {e}")
    return size

def get_all_files(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        loop_list = ['Name', 'Last modified', 'Size', 'Description', 'Parent Directory']
        subdirs = []
        files = []
        for link in soup.find_all('a'):
            if link.text in loop_list:
                continue
            href = link.get('href')
            if href.endswith('/'):  # if directory
                subdirs.append(url + href)
            else:  # if file
                files.append(url + href)
                print('append file:', url + href)
        
        # Recursively get files from subdirectories
        for subdir in subdirs:
            files += get_all_files(subdir)

        return files

def main():
    files = get_all_files(args.url)

    total_size = 0
    with ThreadPoolExecutor(max_workers=args.threads_num) as executor:
            future_to_url = {executor.submit(get_file_size, url): url for url in files}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    size = future.result()
                    total_size += size
                except Exception as e:
                    print(f"Error occurred for URL {url}: {e}")
    print(f"Total size: {total_size} bytes")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print(f"Total size: {total_size / 1024 / 1024 / 1024:.2f} GB")

if __name__ == '__main__':
    main()