import requests
from multiprocessing import Pool
import requests_stream
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import parse_js
import sys
import os

try:
    os.remove('download_urls.txt')
except OSError:
    pass

#Set page load timeout while using selenium to fetch download urls
page_load_timeout = 30
#Number of processes to run in parallel
num_processes = 10
download_urls = []


def get_download_urls(data):

	#Uncomment below line and update path to chrome driver
	# driver = webdriver.Chrome('/home/anirudh/Ani/Projects/Test/selenium/chromedriver')
	(episode_num, url) = data

	#Comment below three lines if using chrome driver and not chrome headless
	#Comment the chrome driver and uncomment the below three lines if using chrome headless driver
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)


	driver.set_page_load_timeout(page_load_timeout)
	download_url = parse_js.get_download_url(driver, url)
	print(download_url)
	with open('download_urls.txt','a') as f:
		f.write('Episode {}.mp4|{}\n'.format(str(episode_num),download_url))
	driver.close()

def get_urls(from_episode,to_episode):
	urls = []
	for episode_num in range(from_episode,to_episode):
		urls.append((episode_num,'https://ww20.watchop.io/view/one-piece-episode-{}/'.format(episode_num)))
	print('Num of processes:{}'.format(num_processes))
	p = Pool(processes=num_processes)
	p.map(get_download_urls, urls)

if __name__ == '__main__':
	from_episode = int(input("Specify the episode number to download from:"))
	to_episode = int(input("Specify the episode number to download till:"))
	compression_flag = input("Compression after download?(Y/N)").upper()

	get_urls(from_episode,to_episode)
	with open('download_urls.txt','r') as f:
		for line in f:
			if len(line.strip()) > 0:
				download_urls.append(tuple(line.strip().split('|')))

	print('Starting to download {} episodes'.format(len(download_urls)))

	p = Pool(processes=num_processes)
	if compression_flag in ["YES","Y"]:
		p.map(requests_stream.download_file_compress,download_urls)
	elif compression_flag in ["NO","N"]:
		p.map(requests_stream.download_file,download_urls)
	else:
		print('Please Enter a valid value')
		sys.exit(1)