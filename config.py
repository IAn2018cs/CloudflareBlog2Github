# coding=utf-8
import config_helper as helper

# keys
cloudflare_account_id: str = helper.get_str_value('keys.cloudflare_account_id')
cloudflare_api_token: str = helper.get_str_value('keys.cloudflare_api_token')
cloudflare_db_name: str = helper.get_str_value('keys.cloudflare_db_name')
github_token: str = helper.get_str_value('keys.github_token')
github_repo_full_name: str = helper.get_str_value('keys.github_repo_full_name')
