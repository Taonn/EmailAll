#!/usr/bin/python3
# coding=utf-8
# Author: @Tao.
import random
import requests
import re
import json

from config.log import logger
from pathlib import Path
from config import settings


def check_net():
    """
    检查网络
    :return:
    """
    urls = ['http://ip-api.com/json/']
    url = random.choice(urls)
    header = {'User_Agent': 'curl'}
    timeout = 5
    verify = False
    logger.log('DEBUG', f'Trying to access {url}')
    session = requests.Session()
    session.trust_env = False
    try:
        rsp = session.get(url, headers=header, timeout=timeout, verify=verify)
    except Exception as e:
        logger.log('ERROR', e.args)
        logger.log('ALERT', 'Unable to access Internet, retrying...')
        raise e
    logger.log('DEBUG', 'Access to Internet OK')
    country = rsp.json().get('country').lower()
    if country in ['cn', 'china']:
        logger.log('DEBUG', f'The computer is located in China')
        return True, True
    else:
        logger.log('DEBUG', f'The computer is not located in China')
        return True, False


def get_net_env():
    logger.log('INFOR', 'Checking network environment')
    try:
        result = check_net()
    except Exception as e:
        logger.log('DEBUG', e.args)
        logger.log('ALERT', 'Please check your network environment.')
        return False, None
    return result


def read_file(path):
    """
    读取domains传入的文件内容
    :param path: domains文件路劲
    :return:
    """
    domains = list()
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            domain = line.strip('\r\n')
            if not domain:
                continue
            domains.append(domain)
        sorted_domains = sorted(set(domains), key=domains.index)

        return sorted_domains


def get_from_domain(domain):
    domains = set()
    if isinstance(domain, str):
        if domain.endswith('.txt'):
            logger.log('FATAL', 'Use domains parameter')
            exit(1)
        domain = domain.lower().strip()
        if not domain:
            return domains
        domains.add(domain)
    return domains


def get_from_domains(domains):
    domains_data = set()
    if not isinstance(domains, str):
        return domains_data
    try:
        path = Path(domains)
    except Exception as e:
        logger.log('ERROR', e.args)
        return domains_data
    if path.exists() and path.is_file():
        domains = read_file(domains)
        return domains
    return domains_data


def get_domains(domain, domains=None):
    logger.log('DEBUG', f'Getting domains')
    domain_data = get_from_domain(domain)
    domains_data = get_from_domains(domains)
    final_domains = list(domain_data.union(domains_data))
    if domains_data:
        final_domains = sorted(final_domains, key=domains_data.index)
    if not final_domains:
        logger.log('ERROR', f'Did not get a valid domain')
    logger.log('DEBUG', f'The obtained domains \n{final_domains}')

    return final_domains

def check_response(method, resp):
    """
    检查响应 输出非正常响应返回json的信息

    :param method: 请求方法
    :param resp: 响应体
    :return: 是否正常响应
    """
    if resp.status_code == 200 and resp.content:
        return True
    logger.log('ALERT', f'{method} {resp.url} {resp.status_code} - '
                        f'{resp.reason} {len(resp.content)}')
    content_type = resp.headers.get('Content-Type')
    if content_type and 'json' in content_type and resp.content:
        try:
            msg = resp.json()
        except Exception as e:
            logger.log('DEBUG', e.args)
        else:
            logger.log('ALERT', msg)
    return False


def match_emails(domain, html):
    """
    匹配邮箱
    :param domain:要配备邮箱的域名
    :param html: 爬取的网页
    :return: 网页解析的邮箱合集
    """
    # reg_emails = re.compile(r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*' + domain.replace('www.', ''))
    reg_emails = re.compile(r'[a-zA-Z0-9.\-_]+' + '@' + '[a-zA-Z0-9.-]*' + domain.replace('www.', ''))
    temp = reg_emails.findall(html)
    emails = list(set(temp))
    true_emails = {str(email)[1:].lower().strip().replace('mailto:', '') if len(str(email)) > 1 and str(email)[0] == '.'
                   else len(str(email)) > 1 and str(email).lower().strip() for email in emails}
    return true_emails


def save_all(domain):
    """
    汇总 所有获取域名的邮箱保存至汇总json文件
    :param domain:
    :return:
    """
    logger.log('TRACE', f'Save the Email results found by '
                        f'All module as a json file')
    path = settings.result_save_dir.joinpath(domain.replace('.', '_'))
    filename = domain + '_All' + '.json'
    path = path.joinpath(filename)
    emails = set()
    for datas in settings.emails:
        for data in datas:
            emails.update(data['emails'])

    results = {
        'total': len(emails),
        'emails': list(emails)}
    with open(path, 'w', errors='ignore') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    logger.log('TRACE', f'Save the ALl Email results found by '
                        f'All module as a file')
