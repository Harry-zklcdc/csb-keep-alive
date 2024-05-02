from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Keys, Actions
from threading import Thread

import os
import time
import logging


options = ChromiumOptions()
options.set_proxy(os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or '')
options.set_headless(True)
options.set_argument('--no-sandbox')

URL_HIDE = os.environ.get('URL_HIDE', '') != ''

def keepAlive(tab, url, sleepTime):
    while True:
        time.sleep(sleepTime)
        try:
            tab.refresh()
            if not URL_HIDE:
                logging.info(f'Refresh {url}')
            else:
                logging.info(f'Refresh {mask_middle(url)}')
        except Exception as e:
            if not URL_HIDE:
                logging.error(f'Refresh {url} Error: {e}')
            else:
                logging.error(f'Refresh {mask_middle(url)} Error: {e}')
            tab.close()
            tab = page.new_tab(url=url)
            if not URL_HIDE:
                logging.info(f'Reopen {url}')
            else:
                logging.info(f'Reopen {mask_middle(url)}')
            continue


def mask_middle(s):
    if len(s) <= 16:
        return s
    else:
        return s[:12] + '*' * 16 + s[-4:]


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)
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
        Thread(target=keepAlive, args=(tab, url, sleepTime)).start()
