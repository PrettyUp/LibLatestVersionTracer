import random
import re
import lxml.html
from requests_html import HTMLSession
from Config import user_agents,proxies,enable_proxy

# 根据xpath提取标签，xpath提取出来的总是一个列表（即便使用id筛选），这里只返回第一个
def get_element_by_xpath(father_elemtent, xpath_exp):
    try:
        target_element = father_elemtent.xpath(xpath_exp)[0]
    except Exception as e:
        print(e)
        return None
    return target_element

# 根据xpath提取标签，返回提取出的整个列表
def get_elements_by_xpath(father_elemtent, xpath_exp):
    try:
        target_elements = father_elemtent.xpath(xpath_exp)
    except:
        return None
    return target_elements

# 返回当前标签内的字符串，index用于指定返回第几个字符串
# requests-html以当前节点为根节点，但lxml总是以最开始的节点为根节点，为了通用使用".//text()"格式
def get_element_text(elemtent,index=0):
    try:
        text = elemtent.xpath(".//text()")[index].strip()
    except:
        return ""
    return text

# version1----第一个要比较的版本字符串
# version2----第二个要比较的版本字符串
# split_flag----版本分隔符，默认为"."，可自定义
# 返回值----version1等于version2返回0，version1比version2大返回1，version2比version1大返回2
# 接受的版本字符形式----空/x/x.y/x.y./x.y.z；两个参数可为前边列出的形式的任一种
def compare_version(version1=None,version2=None,split_flag="."):
    # 如果存在有为空的情况则进入
    if (version1 is None) or (version1 == "") or (version2 is None) or (version2 == ""):
        # version1为空且version2不为空，则返回version2大
        if ((version1 is None) or (version1 == "")) and (version2 is not None) and (version2 != ""):
            return 2
        # version2为空且version1不为空，则返回version1大
        if ((version2 is None) or (version2 == "")) and (version1 is not None) and (version1 != ""):
            return 1

    # 如果版本字符串相等，那么直接返回相等，这句会且只会在第一次比较时才可能进入
    # version1和version2都为空时也会进入这里
    if version1 == version2:
        return 0

    # 对版本字符串从左向右查找"."，第一个"."之前的字符串即为此次要比较的版本
    # 如1.3.5中的1
    try:
        current_section_version1 = version1[:version1.index(split_flag)]
    except:
        current_section_version1 = version1
    try:
        current_section_version2 = version2[:version2.index(split_flag)]
    except:
        current_section_version2 = version2
    # 对本次要比较的版本字符转成整型进行比较
    if int(current_section_version1) > int(current_section_version2):
        return 1
    elif int(current_section_version1) < int(current_section_version2):
        return 2

    # 如果本次传来版本字符串中已没有版本号分隔符，那说明本次比较的版本号已是最后一位版本号，下次比较值赋空
    # 如本次传来的是5，那下次要比较的只能赋空
    try:
        other_section_version1 = version1[version1.index(split_flag)+1:]
    except:
        other_section_version1 = ""
    try:
        other_section_version2 = version2[version2.index(split_flag) + 1:]
    except:
        other_section_version2 = ""

    # 递归调用比较
    return compare_version(other_section_version1,other_section_version2)

# 此函数调用compare_version()，打印比较结果
def pick_up_latest_version(version1,version2):
    flag = compare_version(version1,version2)
    if flag == 0:
        print(f"version1 = {version1}, version2 = {version2}, the two version is equal")
    elif flag == 1:
        print(f"version1 = {version1}, version2 = {version2}, the latest version is version1 {version1}")
    elif flag == 2:
        print(f"version1 = {version1}, version2 = {version2}, the latest version is version2 {version2}")

# 从user_agents中随机选出一个user_agent
def select_one_user_agent():
    user_agent_count = len(user_agents)
    user_agent_index = random.randint(0,user_agent_count-1)
    user_agent = user_agents[user_agent_index]
    return user_agent

# 使用requests_html请求url，并返回请求结果
def get_url_response(url):
    session = HTMLSession()
    headers = {}
    # 修改Host头，对于requests没必要，因为requests会自动设置
    # host = re.search("[^/]{1,}\.[^/]{1,}",url).group()
    # headers['Host'] = host
    #
    headers["User-Agent"] = select_one_user_agent()
    try:
        if enable_proxy:
            print(f"request start use proxy: {url}\n{proxies}")
            response = session.get(url, headers=headers, proxies=proxies, verify=False)
        else:
            print(f"request start no proxy: {url}")
            response = session.get(url, headers=headers, verify=False)
    except:
        print(f"request error, will to try again: {url}")
        return get_url_response(url)
    print(f"request success: {url}")
    session.close()
    return response

# 将response格式化成一个xpath解析器
def get_response_parser(response,parse_tool="requests_html"):
    if parse_tool == "lxml":
        parser = lxml.html.fromstring(response.text)
    else:
        parser = response.html
    return parser

# 从传来的字符串中提取出版本号
# 如传来"	nginx/Windows-1.16.0"，提取结果为"1.16.0"
def extract_version_from_str(version_str):
    try:
        version = re.search("[\d\.]+[\d]+", version_str).group()
    except:
        version = "0.0.0"
    return version