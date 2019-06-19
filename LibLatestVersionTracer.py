from Common import *
import openpyxl
from Config import *

def upnp_latest_version_tracer():
    # 通过比较版本号获取最新1.6系列版本
    def get_latest_version_16(version_table):
        version_trs = get_elements_by_xpath(version_table, "//tr")
        version = "1.6.0"
        for tr in version_trs[1:]:
            version_tmp = get_element_text(get_element_by_xpath(tr, "//td[1]"))
            if ("1.6" in version_tmp) and (compare_version(version_tmp, version) == 1):
                version = version_tmp
                release_time = get_element_text(get_element_by_xpath(tr, "//td[2]"))
        return {"version":version,"release_time":release_time}

    # 通过比较版本号获取最新1.8系列版本
    def get_latest_version(version_table):
        last_version_trs = get_elements_by_xpath(version_table, "//tr")

        last_version = get_element_text(get_element_by_xpath(last_version_trs[-1], "//td[1]"))
        release_time = get_element_text(get_element_by_xpath(last_version_trs[-1], "//td[2]"))
        return {"version":last_version,"release_time":release_time}

    version_monitor_url = "https://github.com/mrjimenez/pupnp"
    version_table_xpath = """//*[@id="readme"]/div[2]/article/table[1]"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)
    version_table = get_element_by_xpath(parser, version_table_xpath)

    latest_version_16 = get_latest_version_16(version_table)
    latest_version = get_latest_version(version_table)
    # print(f"""{latest_version_16}-{latest_version}""")
    return {"version_list":[latest_version_16,latest_version],"version_monitor_url":version_monitor_url}

# 因为response_html xpath一直出错所以需要使用lxml
# requests-html以当前结点为根结点，而lxml总是以最初的节点为根结点;所以xpath表达示requests-html开头可以使用/和//，而lxml不要轻易用
def ansible_latest_version_tracer():
    def get_latest_version(version_div,version_sign):
        version_entries = get_elements_by_xpath(version_div,"div/div")
        # version_entries = version_div[0].xpath("/div//div/div")
        for div in version_entries:
            version_tmp = get_element_text(get_element_by_xpath(div,"div/div/div[1]/h4/a"),index=1)
            # 因为第一个是最新发布的那个，所以如果找到版本标志则直接返回
            if version_sign in version_tmp:
                release_time = get_element_text(get_element_by_xpath(div,"span/relative-time"))
                return {"version":version_tmp,"release_time":release_time}
        # 如果到最后都没找到版本标志，那就返回"-"表示没找到
        return {"version":"-","release_time":"-"}

    version_monitor_url = "https://github.com/ansible/ansible/releases"
    version_div_xpath = "/html/body/div[4]/div/main/div[2]/div[1]/div[3]/div"
    # session = HTMLSession()
    # response = session.get(version_monitor_url, verify=False)
    # version_div = get_element_by_xpath(response.html, version_div_xpath)
    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response,parse_tool="lxml")
    # version_div = parser.xpath(version_div_xpath)
    version_div = get_element_by_xpath(parser,version_div_xpath)

    version_sign = "v2.6"
    latest_version_26 = get_latest_version(version_div,version_sign)
    version_sign = "v2.7"
    latest_version_27 = get_latest_version(version_div, version_sign)
    version_sign = "v2.8"
    latest_version_28 = get_latest_version(version_div, version_sign)
    # print(f"""{latest_version_26}-{latest_version_27}-{latest_version_28}""")
    return {"version_list":[latest_version_26,latest_version_27,latest_version_28],"version_monitor_url":version_monitor_url}

def redis_latest_version_tracer():
    def get_latest_version_5(version_table):
        version_entries = get_elements_by_xpath(version_table,"table/tr")
        version = "5.0.0"
        for entry in version_entries[3:-2]:
            version_str = get_element_text(get_element_by_xpath(entry,"tr/td[2]/a"))
            version_tmp = extract_version_from_str(version_str)
            if ("5." in version_tmp) and (compare_version(version_tmp,version) == 1):
                release_time = get_element_text(get_element_by_xpath(entry,"tr/td[3]"))
                version = version_tmp
        return {"version":version,"release_time":release_time}

    def get_latest_version(version_table):
        version_entries = get_elements_by_xpath(version_table, "table/tr")
        latest_packet = get_element_text(get_element_by_xpath(version_entries[-3],"tr/td[2]/a"))
        latest_version = extract_version_from_str(latest_packet)
        release_time = get_element_text(get_element_by_xpath(version_entries[-3], "tr/td[3]"))
        return {"version":latest_version,"release_time":release_time}

    version_monitor_url = "http://download.redis.io/releases/"
    version_table_xpath = "/html/body/table"

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    version_table = get_element_by_xpath(parser,version_table_xpath)

    latest_version_5 = get_latest_version_5(version_table)
    latest_version = get_latest_version(version_table)
    # print(f"{latest_version_5}-{latest_version}")
    return {"version_list":[latest_version_5,latest_version],"version_monitor_url":version_monitor_url}

# 5.7系列和最新版本其实只是页面url不同，其他如版本位置等是一样的，不过为防以后有变动直接使用两个函数
def mysql_latest_version_tracer():
    def get_latest_version_57():
        version_monitor_url = "https://dev.mysql.com/downloads/mysql/5.7.html"
        version_label_xpath = """//*[@id="ga"]/h1"""
        response = get_url_response(version_monitor_url)
        parser = get_response_parser(response)

        version_label_str = get_element_text(get_element_by_xpath(parser,version_label_xpath))
        latest_version_57 = extract_version_from_str(version_label_str)
        return {"version":latest_version_57,"release_time":"-"}
    def get_latest_version():
        version_label_xpath = """//*[@id="ga"]/h1"""
        response = get_url_response(version_monitor_url)
        parser = get_response_parser(response)

        version_label_str = get_element_text(get_element_by_xpath(parser, version_label_xpath))
        latest_version = extract_version_from_str(version_label_str)

        return {"version":latest_version,"release_time":"-"}

    version_monitor_url = "https://dev.mysql.com/downloads/mysql/"
    latest_version_57 = get_latest_version_57()
    latest_version = get_latest_version()
    # print(f"{latest_version_57}-{latest_version}")
    return {"version_list":[latest_version_57,latest_version],"version_monitor_url":version_monitor_url}

def mycat_latest_version_tracer():
    version_monitor_url = "https://github.com/MyCATApache/Mycat-Server/releases"
    version_label_xpath = """/html/body/div[4]/div/main/div[2]/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/a"""
    release_time_xpath = """/html/body/div[4]/div/main/div[2]/div[1]/div[3]/div[1]/div/div[2]/div[1]/p/relative-time"""
    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response,parse_tool="lxml")

    latest_version = get_element_text(get_element_by_xpath(parser,version_label_xpath))
    release_time = get_element_text(get_element_by_xpath(parser,release_time_xpath))
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def zookeeper_latest_version_tracer():
    version_monitor_url = "https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/"
    version_xpath_34 = """/html/body/pre/a[8]"""
    release_time_xpath_34 = """/html/body/pre"""
    version_xpath_35 = """/html/body/pre/a[9]"""
    release_time_xpath_35 = """/html/body/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version_34_str = get_element_text(get_element_by_xpath(parser,version_xpath_34))
    latest_version_34 = extract_version_from_str(latest_version_34_str)
    release_time_34 = get_element_text(get_element_by_xpath(parser,release_time_xpath_34),index=-4)

    latest_version_35_str = get_element_text(get_element_by_xpath(parser, version_xpath_35))
    latest_version_35 = extract_version_from_str(latest_version_35_str)
    release_time_35 = get_element_text(get_element_by_xpath(parser, release_time_xpath_35),index=-1)

    # print(f"{latest_version_34}-{latest_version_35}")
    return {"version_list":[{"version":latest_version_34,"release_time":release_time_34},{"version":latest_version_35,"release_time":release_time_35}],"version_monitor_url":version_monitor_url}

def kafka_latest_version_tracer():
    version_monitor_url = "https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/"
    version_label_xpath = "/html/body/pre/a[last()]"
    release_time_xpath = """/html/body/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version_str = get_element_text(get_element_by_xpath(parser,version_label_xpath))
    latest_version = extract_version_from_str(latest_version_str)
    release_time = get_element_text(get_element_by_xpath(parser,release_time_xpath),index=-1)

    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def nginx_latest_version_tracer():
    version_monitor_url = "http://nginx.org/en/download.html"
    version_label_xpath = """//*[@id="content"]/table[2]/tr/td[3]/a[1]"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version_str = get_element_text(get_element_by_xpath(parser,version_label_xpath))
    latest_version = extract_version_from_str(latest_version_str)

    # print(f"{latest_version}")
    return {"version_list":[{"version":latest_version,"release_time":"-"}],"version_monitor_url":version_monitor_url}

def ceph_latest_version_tracer():
    def get_latest_version(version_div,version_sign):
        version_entries = get_elements_by_xpath(version_div,"div/div")
        # version_entries = version_div[0].xpath("/div//div/div")
        for div in version_entries:
            version_tmp = get_element_text(get_element_by_xpath(div,"div/div/div[1]/h4/a"),index=1)
            # 因为第一个是最新发布的那个，所以如果找到版本标志则直接返回
            if version_sign in version_tmp:
                release_time = get_element_text(get_element_by_xpath(div,"span/relative-time"))
                return {"version":version_tmp,"release_time":release_time}
        # 如果到最后都没找到版本标志，那就返回"-"表示没找到
        return {"version":"-","release_time":"-"}

    version_monitor_url = "https://github.com/ceph/ceph/releases"
    version_div_xpath = "/html/body/div[4]/div/main/div[2]/div[1]/div[3]/div"
    # session = HTMLSession()
    # response = session.get(version_monitor_url, verify=False)
    # version_div = get_element_by_xpath(response.html, version_div_xpath)
    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response,parse_tool="lxml")
    # version_div = parser.xpath(version_div_xpath)
    version_div = get_element_by_xpath(parser,version_div_xpath)

    version_sign = "v12."
    latest_version_12 = get_latest_version(version_div,version_sign)
    version_sign = "v13."
    latest_version_13 = get_latest_version(version_div, version_sign)
    version_sign = "v14."
    latest_version_14 = get_latest_version(version_div, version_sign)
    version_sign = "v15."
    latest_version_15 = get_latest_version(version_div, version_sign)
    # print(f"""{latest_version_26}-{latest_version_27}-{latest_version_28}""")
    return {"version_list":[latest_version_12,latest_version_13,latest_version_14],"version_monitor_url":version_monitor_url}

# elastic.co的id形如"react-tabs-23087"，数值部分会变化，所以xpath只能使用绝对路径
def elasticsearch_latest_version_tracer():
    version_monitor_url = "https://www.elastic.co/cn/downloads/elasticsearch"
    version_div_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]"""
    release_time_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_div_xpath))
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def logstash_latest_version_tracer():
    version_monitor_url = "https://www.elastic.co/cn/downloads/logstash"
    version_div_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]"""
    release_time_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_div_xpath))
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def kibana_latest_version_tracer():
    version_monitor_url = "https://www.elastic.co/cn/downloads/kibana"
    version_div_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]"""
    release_time_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]"""

    # session = HTMLSession()
    # response = session.get(version_monitor_url, headers=headers, verify=False)
    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_div_xpath))
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def filebeat_latest_version_tracer():
    version_monitor_url = "https://www.elastic.co/cn/downloads/beats/filebeat"
    version_div_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]"""
    release_time_xpath = """/html/body/div[1]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]"""

    # session = HTMLSession()
    # response = session.get(version_monitor_url, headers=headers, verify=False)
    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_div_xpath))
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def zabbix_server_latest_version_tracer():
    version_monitor_url = "https://www.zabbix.com/download_sources"
    version_label_xpath = """//*[@id="content_42"]/div/table/tbody/tr[2]/td[2]/pre"""
    release_time_xpath = """//*[@id="content_42"]/div/table/tbody/tr[2]/td[3]/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_label_xpath))
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def zabbix_agent_latest_version_tracer():
    version_monitor_url = "https://www.zabbix.com/download_agents"
    version_label_xpath = """//*[@id="appliance_zabbix_42"]/div/table/tbody/tr[1]/td[1]/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version = get_element_text(get_element_by_xpath(parser, version_label_xpath))
    # print(f"""{latest_version}""")
    return {"version_list":[{"version":latest_version,"release_time":"-"}],"version_monitor_url":version_monitor_url}

def gitlab_latest_version_tracer():
    def get_latest_version(version_table):
        version_entries = get_elements_by_xpath(version_table,"table/tbody/tr")
        version = "11.0.0"
        release_time = "-"
        for entry in version_entries[1:]:
            version_str = get_element_text(get_element_by_xpath(entry,"tr/td[1]/a"))
            version_tmp = extract_version_from_str(version_str)
            if (compare_version(version_tmp,version) == 1):
                release_time = get_element_text(get_element_by_xpath(entry,"tr/td[3]"))
                version = version_tmp
        return {"version":version,"release_time":release_time}
    version_monitor_url = "https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu/pool/xenial/main/g/gitlab-ce/"
    version_table_xpath = """//*[@id="list"]"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    version_table = get_element_by_xpath(parser,version_table_xpath)

    latest_version = get_latest_version(version_table)

    return {"version_list":[latest_version],"version_monitor_url":version_monitor_url}

def hadoop_latest_version_tracer():
    version_monitor_url = "https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/"
    # last()是最后一个标签，last()-3表示倒数第4个标签
    version_label_xpath = """//a[last()-3]"""
    release_time_xpath = """/html/body/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version_str = get_element_text(get_element_by_xpath(parser,version_label_xpath))
    latest_version = extract_version_from_str(latest_version_str)
    release_time = get_element_text(get_element_by_xpath(parser,release_time_xpath),index=-10)
    # print(f"{latest_version}")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

def hbase_latest_version_tracer():
    version_monitor_url = "https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/"
    # last()是最后一个标签，last()-4表示倒数第5个标签
    version_label_xpath = """//a[last()-4]"""
    release_time_xpath = """/html/body/pre"""

    response = get_url_response(version_monitor_url)
    parser = get_response_parser(response)

    latest_version_str = get_element_text(get_element_by_xpath(parser,version_label_xpath))
    latest_version = extract_version_from_str(latest_version_str)
    release_time = get_element_text(get_element_by_xpath(parser, release_time_xpath),index=-13)
    # print(f"{latest_version}")
    return {"version_list":[{"version":latest_version,"release_time":release_time}],"version_monitor_url":version_monitor_url}

# 主要逻辑是遍历传来的latest_versions，将最新版本写到对应库的同一行中
def save_version_info_to_file(latest_versions):
    mywb = openpyxl.load_workbook(lib_info_filename)
    mysheet = mywb.get_sheet_by_name(lib_info_sheetname)

    for k, v in latest_versions.items():
        for row_index in range(lib_start_row,lib_end_row+1):
            lib_name_cell_name = f"{lib_name_column}{row_index}"
            if k in mysheet[lib_name_cell_name].value:
                latest_version_cell_name = f"{latest_version_column}{row_index}"
                monitor_url_cell_name = f"{monitor_url_column}{row_index}"
                version = ""
                for version_entry in v["version_list"]:
                    version += f"""{version_entry['version']}({version_entry['release_time']})\n"""
                mysheet[latest_version_cell_name] = version
                mysheet[monitor_url_cell_name] = v["version_monitor_url"]
                break
    mywb.save(lib_info_filename)

# 依次调用所有库追踪最新版本的方法获取其最新版本，最后调用save_version_info_to_file将最新版本保存到文件
def all_latest_version_tracer():
    latest_versions = {}
    latest_versions["upnp"] = upnp_latest_version_tracer()
    latest_versions["ansible"] = ansible_latest_version_tracer()
    latest_versions["redis"] = redis_latest_version_tracer()
    latest_versions["mysql"] = mysql_latest_version_tracer()
    latest_versions["mycat"] = mycat_latest_version_tracer()
    latest_versions["zookeeper"] = zookeeper_latest_version_tracer()
    latest_versions["kafka"] = kafka_latest_version_tracer()
    latest_versions["nginx"] = nginx_latest_version_tracer()
    latest_versions["ceph"] = ceph_latest_version_tracer()
    latest_versions["elasticsearch"] = elasticsearch_latest_version_tracer()
    latest_versions["logstash"] = logstash_latest_version_tracer()
    latest_versions["kibana"] = kibana_latest_version_tracer()
    latest_versions["filebeat"] = filebeat_latest_version_tracer()
    latest_versions["zabbix-server"] = zabbix_server_latest_version_tracer()
    latest_versions["zabbix-agent"] = zabbix_agent_latest_version_tracer()
    latest_versions["gitlab"] = gitlab_latest_version_tracer()
    latest_versions["hadoop"] = hadoop_latest_version_tracer()
    latest_versions["hbase"] = hbase_latest_version_tracer()

    for k,v in latest_versions.items():
        print(f"{k}-{v}")

    save_version_info_to_file(latest_versions)


if __name__ == "__main__":
    all_latest_version_tracer()
    # print(mysql_latest_version_tracer())
    pass