# 此部分被common.py使用
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
]
# 代理服务器
proxies = {
    "http":"127.0.0.1:8080",
    "https":"127.0.0.1:8080"
}
# 是否启用代理
enable_proxy = False

# 以下部分被LibLatestVersionTracer.py使用
# 组件文件名称
lib_info_filename = "LibExample.xlsx"
lib_info_sheetname = "LibExample Sheet"
# 组件名称为A列
lib_name_column = "A"
# 最新版本存入为L列
latest_version_column = "F"
# 版本监测链接存入M列
monitor_url_column = "G"
# 组件起始行为第三行
lib_start_row = 2
# 组件结束行为第20行
lib_end_row = 19
