# coding:utf-8

import datetime
import codecs
import requests
import os
import time
import html2markdown
from pyquery import PyQuery as pq


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(date, filename):
    with open(filename, 'w') as f:
        f.write("## " + date + "\n")


def scrape(language, filename):
    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'pt-BR,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    
    print(url)

    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')
    
    if language=="":
        #print(items)
        markdown = html2markdown.convert(r.content)
        with open("trending.md", "w", encoding="utf-8") as file:
            file.write(markdown)

    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(filename, "a", "utf-8") as f:
        if language=="":
            language= "trending"
            
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            # ownerImg = i("p.repo-list-meta a img").attr("src")
            # print(ownerImg)
            f.write(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))


def job():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    # write markdown
    scrape('', filename)
    scrape('c#', filename)
    scrape('c++', filename)
    scrape('go', filename)
    scrape('html', filename)
    scrape('javascript', filename)
    scrape('php', filename)
    #toscrape('ruby', filename)
    scrape('rust', filename)
    scrape('swift', filename)
    scrape('vue', filename)
    scrape('python', filename)
    scrape('typescript', filename)
    #scrape('markdown', filename)
    # git add commit push
    # git_add_commit_push(strdate, filename)


if __name__ == '__main__':
    job()
