import webbrowser
import urllib3
import urllib.request

def open():
    new = 2
    html_file = 'firebase.html'
    webbrowser.open(html_file, new = new)

def download(input11):
    opener = urllib3.request.FancyURLopener({})
    url = input1
    # urllib3.urlretrieve(url, "doc.html")
    f = opener.open(url)
    content = f.read()
    new_html = '{}_eiei.html'.format(url)
    ff = open(new_html, 'w')
    ff.write(f)
    ff.close

    print('sadfasdfasfdd')

def new_download(input1):

    site = urllib.request.urlopen(input1)
    data = site.read()
    file = open("file.txt", "wb")
    file.writelines(data)
    file.close()

input1 = input('Add urls here: ')
new_download(input1)