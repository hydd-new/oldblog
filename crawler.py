# -*- coding:utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

f = open('blog.md', 'w', encoding='utf-8')

Latextag = 0

def GetHtmlText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""

def Clear(text):
    flag = True
    while flag:
        flag = False
        try:
            index = text.index('$$$')
            if Latextag == 0:
                pass
            elif Latextag == 1:
                text = text[:index] + text[index + 1:]
            elif Latextag == 2:
                text = text[:index] + text[index + 2:]
            flag = True
        except:
            break
    return text

def FindInfo(soup, url, c):
    AllInfo = soup.find('div', {'class', 'problemindexholder'})
    if AllInfo == None:
        # f.close()
        # os._exit(0)
        return


    divs = AllInfo.find_all('div')

    if len(divs)>5:
        title = '# ' + c + divs[5].get_text()
        f.write('%s\n' % title)

    if len(divs)>6:
        tl = 'Time Limit: ' + divs[6].get_text()[19:]
        f.write('```\n%s\n' % tl)

    if len(divs)>8:
        tl = 'Memory Limit: ' + divs[8].get_text()[21:]
        f.write('%s\n```\n' % tl)

    if len(divs)>14:
        problem = '## Description:\n' + divs[14].get_text()
        problem = Clear(problem)
        f.write('%s\n' % problem)

    if len(divs)>15:
        Input = '## Input:\n' + divs[15].get_text()[5:]
        Input = Clear(Input)
        f.write('%s\n' % Input)
    
    if len(divs)>17:
        Output = '## Output\n' + divs[17].get_text()[6:]
        Output = Clear(Output)
        f.write('%s\n' % Output)

    Sample = soup.find('div', {'class', 'sample-test'})
    if Sample != None:
        SampleInputs = Sample.find_all('div', {'class', 'input'})
        SampleOutputs = Sample.find_all('div', {'class', 'output'})
        for i in range(len(SampleInputs)):
            SampleInput = SampleInputs[i].get_text()
            SampleOutput = SampleOutputs[i].get_text()
            f.write('## Sample Input:\n ``` \n%s\n ``` \n' % SampleInput[5:])
            f.write('## Sample Output:\n ``` \n%s\n ``` \n' % SampleOutput[6:])

    Note = soup.find('div', {'class', 'note'})
    if Note != None:
        f.write('## Note:\n')
        notess = Note.get_text()[4:]
        notess = Clear(notess)
        f.write('%s\n' % notess)


    f.write('### [Link](%s)\n\n' % url[:-1])
    # f.write('## AC代码:\n```\n```\n')

def main():
    global Latextag
    print('Welcome to use codeforces contest crawler\n')
    # Latextag = int(input("Please enter the Latex tag you need(0:'$$$',1:'$$',2:'$'):\n"))
    Latextag = 2

    with open("problem-list-fixed.txt") as lines:
        for line in lines:
            t=line.split(' ')
            # t=['1353','B']
            c=int(t[0])
                
            i=t[1]
            Url = 'http://codeforces.com/contest/' + str(c)
            Url += '/problem/'
            # if c!=1164 and c!=630 and c!=802 and i=='O':
                # break
            url = Url + i;
            print(url)
            html = GetHtmlText(url).replace('<br />', '\n').replace('</p>', '\n')
            soup = BeautifulSoup(html, "html.parser")
            FindInfo(soup, url, str(c))

    f.close()

if __name__ == '__main__':
    main()
