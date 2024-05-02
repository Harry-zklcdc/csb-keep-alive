from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Keys, Actions
from threading import Thread
from urllib.parse import urlparse

import os
import time
import logging


options = ChromiumOptions()
options.set_proxy(os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or '')
options.set_headless(True)
options.set_argument('--no-sandbox')

URL_HIDE = os.environ.get('URL_HIDE', '') != ''

def keepAlive(tab, sleepTime):
    while True:
        time.sleep(sleepTime)
        tab.refresh()
        parsed_url = urlparse(tab.url)
        if not URL_HIDE:
            logging.info(f'Refresh {parsed_url.scheme + ":" + parsed_url.hostname}')
        else:
            logging.info(f'Refresh {mask_middle(parsed_url.scheme + ":" + parsed_url.hostname)}')


def mask_middle(s):
    if len(s) <= 16:
        return s
    else:
        return s[:12] + '*' * 16 + s[-4:]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Start KeepAlive')

    sleepTime = int(os.environ.get('SLEEP_TIME', '600'))
    logging.info(f'Sleep Time: {sleepTime}')

    URLraw = os.environ.get('URLS', '')
    urls = URLraw.split(',')
    if not URL_HIDE:
        logging.info(f'URLs: {urls}')
    else:
        logging.info(f'URLs: {[mask_middle(url) for url in urls]}')

    page = ChromiumPage(addr_driver_opts=options)
    logging.info(f'Brower Pid: {page.process_id}')
    for url in urls:
        tab = page.new_tab(url=url)
        if not URL_HIDE:
            logging.info(f'Open {url}')
        else:
            logging.info(f'Open {mask_middle(url)}')
        Thread(target=keepAlive, args=(tab, sleepTime)).start()
