# coding=utf-8

from d1py import D1py
import config
from github import Github
from github import Auth

if __name__ == '__main__':
    # Usage example:
    # d1 = D1py(config.cloudflare_account_id, config.cloudflare_api_token)
    # db_id = d1.get_db_id(config.cloudflare_db_name)
    # print(f"db_id: {db_id}")
    # result = d1.query_db(db_id, 'select * from feeds limit 2')
    # print(result)

    auth = Auth.Token(config.github_token)
    g = Github(auth=auth)
    repo = g.get_repo(config.github_repo_full_name)
    for issue in repo.get_issues():
        print(issue.title)

    # repo.create_issue("test", "cf blog test", labels=['测试'])

    g.close()
