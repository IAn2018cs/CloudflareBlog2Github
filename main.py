# coding=utf-8

import os
import re
import time

from github import Auth
from github import Github

import config
from d1py import D1py


def get_all_feeds(d1, db_id, page_size=10):
    all_data = []
    page = 0
    more_data = True

    while more_data:
        offset = page * page_size
        query = f"""
            SELECT *
            FROM feeds
            ORDER BY created_at
            LIMIT {page_size + 1} OFFSET {offset}
            """
        result = d1.query_db(db_id, query)
        page_data = result['result'][0]['results']
        print(f'page_data len: {len(page_data)}')
        if len(page_data) < page_size + 1:
            # 这是最后一页
            all_data.extend(page_data)
            more_data = False
        else:
            # 还有更多页
            all_data.extend(page_data[:page_size])
            print(page_data)
            more_data = True

        print(f"Fetched page {page + 1}")
        page += 1

    return all_data


def get_feed_tags(d1, db_id, feed_id):
    tags = []
    query = f"""
        SELECT *
        FROM feed_hashtags
        WHERE feed_id = {feed_id}
        """
    result = d1.query_db(db_id, query)['result'][0]['results']
    for row in result:
        tag_id = row['hashtag_id']
        name = d1.query_db(db_id, f"SELECT name FROM hashtags WHERE id = {tag_id}")['result'][0]['results'][0]['name']
        tags.append(name)
    return tags


def get_db_id(d1):
    cache_file = './db_id.cache'
    if os.path.exists(cache_file):
        with open('./db_id.cache', 'r') as f:
            return str(f.read())
    db_id = d1.get_db_id(config.cloudflare_db_name)
    with open('./db_id.cache', 'w') as f:
        f.write(db_id)
    return db_id


def convert_markdown_to_gmeek_url(text):
    pattern = r'!\[(.*?)\]\((https?://[^\s)]+)\)'
    replacement = r'`Gmeek-html<img src="\2">`'
    return re.sub(pattern, replacement, text)


if __name__ == '__main__':
    d1 = D1py(config.cloudflare_account_id, config.cloudflare_api_token)
    db_id = get_db_id(d1)
    print(f"db_id: {db_id}")

    auth = Auth.Token(config.github_token)
    g = Github(auth=auth)
    repo = g.get_repo(config.github_repo_full_name)
    exists_title = set()
    for issue in repo.get_issues():
        exists_title.add(issue.title)

    feeds = get_all_feeds(d1, db_id)
    for feed in feeds:
        title = feed['title']
        if title in exists_title:
            continue
        feed_id = feed['id']
        created_at = feed['created_at']
        content = feed['content']
        tags = get_feed_tags(d1, db_id, feed_id)
        publish_time = '<!-- ##{"timestamp":' + str(created_at) + '}## -->'
        new_content = f'{convert_markdown_to_gmeek_url(content)}\n\n{publish_time}'

        print(f"start transfer: {title}")
        repo.create_issue(title, new_content, labels=tags)
        time.sleep(60)
        exists_title.add(title)

    g.close()
