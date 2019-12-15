from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_download_url(driver,webpage_url):
	#Hard coded the number of retries in case of timeout to 5. Change if necessary
	for i in range(0,5):
		try:
			print('Getting url {}'.format(webpage_url))
			driver.get(webpage_url)
			p_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dl"]/a')))
			return p_element.get_attribute('href')
		except:
			try:
				p_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dl"]/a')))
				return p_element.get_attribute('href')
			except:
				print('Timeout exception for url {}. Retrying'.format(webpage_url))