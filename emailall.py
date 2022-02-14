import fire

from config.log import logger
from datetime import datetime
from common import utils
from modules.collect import Collect
from common.output import Output
from config import settings
import time

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

version = 'v1.0'
message = white + '{' + red + version + ' #dev' + white + '}'

banner = f"""
{red}EmailALl is a powerful Emails integration tool{yellow}
 _____                _ _  ___  _ _ 
|  ___|              (_) |/ _ \| | | {message}{green}
| |__ _ __ ___   __ _ _| / /_\ \ | |
|  __| '_ ` _ \ / _` | | |  _  | | |{blue}
| |__| | | | | | (_| | | | | | | | |
\____/_| |_| |_|\__,_|_|_\_| |_/_|_|{white} By Microtao.
{end}
"""


class EmailAll(object):
    """
    EmailAll help summary page

    EmailAll is a powerful Email Collect tool

    Example:
        python3 emailall.py version
        python3 emailall.py check
        python3 emailall.py --domain example.com run
        python3 emailall.py --domains ./domains.txt run
    """

    def __init__(self, domain=None, domains=None):
        self.domain = domain    # 单条
        self.domains = domains  # 多条
        self.version = self.version # 版本信息
        self.access_internet = False    # 测试上网环境
        self.output = Output()  # 输出结果类

    def main(self):

        if not self.access_internet:
            logger.log('ALERT', 'Because it cannot access the Internet')
        if self.access_internet:
            collect = Collect(self.domain)
            collect.run()
            utils.save_all(self.domain)
            settings.emails.clear()

    def run(self):
    
        print(banner)
        
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[*] Starting EmailAll @ {dt}\n')
        logger.log('DEBUG', f'[*] Starting EmailAll @ {dt}\n')
        self.access_internet, self.in_china = utils.get_net_env()
        self.domains = utils.get_domains(self.domain, self.domains)
        count = len(self.domains)
        
        if not count:
            logger.log('FATAL', 'Failed to obtain domain')
            exit(1)
        for domain in self.domains:
            self.domain = domain
            self.main()
        time.sleep(2)
        for i in range(int(len(self.domains))):
            self.output.run(self.domains[i])
            print(settings.rule_func[i])
    @staticmethod
    def version():
        """
        Print version information and exit
        """
        print(banner)
        exit(0)


if __name__ == '__main__':
    fire.Fire(EmailAll)
