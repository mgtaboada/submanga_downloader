from bs4 import BeautifulSoup
from urllib.request import urlopen,URLopener
import os

BASE_URL = "http://submanga.com"
def to_n_digits(n,num):
    s = str(num)
    return "0"*(n-len(s))+s
def get_manga_list():
    html = urlopen(BASE_URL + "/series")
    soup = BeautifulSoup(html,"lxml")
    manga = soup.find("div","b468")
    manga_links = [td.a["href"] for td in manga.findAll("td") if td.a is not None]
    return manga_links

def print_manga_list(manga_links):
    i = 1
    for element in manga_links:
        name_with__ = element.split("/")[-1]
        print(str(i) + "\t " +name_with__.replace("_"," "))
        i+=1

def download_page(pic_url,output):
    image = URLopener()
    image.retrieve(pic_url,output)

def get_pic_and_next(page_url):
    html = urlopen(page_url)
    soup = BeautifulSoup(html,"lxml")
    page = soup.find("div",{"id":"ab"})
    if page:
        a = page.findAll("a")[0]
        next_page_url = a["href"]
        pic_url = a.img["src"]
        return (next_page_url, pic_url)
    else:
        return None
def get_chapter_first_page(chapter_url):
    html = urlopen(chapter_url)
    soup = BeautifulSoup(html,"lxml")
    first_page = soup.find("a",{"id":"l"})
    return first_page["href"]

def make_chapter_directory(manga_path,chapter_number):
    path = manga_path + "/Chapter_" + to_n_digits(4,chapter_number)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def download_chapter(first_page,prefix,manga_path,chapter_number):
    path = make_chapter_directory(manga_path, chapter_number)
    current_page = 1
    page_url = first_page
    while page_url:

        data = get_pic_and_next(page_url)
        if data:
            page_url,pic = data
            pic_name = to_n_digits(3,current_page)+"."+pic.split(".")[-1]
            print("Downloading page: "+str(current_page))
            pic_path = path + "/"+prefix+"_"+ to_n_digits(4,chapter_number)+"_"+pic_name
            download_page(pic,pic_path)
        else:
            html = urlopen(page_url)
            page_url = None
            soup = BeautifulSoup(html,"lxml")
            next_chap = soup.find("a",{"id":"c"})
            next_chap_url = next_chap["href"]
        current_page +=1
    return next_chap_url


def get_first_chapter(manga_url):
    html = urlopen(manga_url+"/completa")
    soup = BeautifulSoup(html,"lxml")
    manga = soup.find("table","caps")
    for a in manga.findAll("a"):
        strong = a.find("strong")
        if strong and str(strong) =="<strong>1</strong>":
            chapter_link = a["href"]
            return chapter_link

        
def download_manga(manga_url,manga_name):
    manga_path = make_manga_directory(manga_name)
    first_chap_url = get_first_chapter(manga_url)
    first_page = get_chapter_first_page(first_chap_url)
    next_page_url = first_page
    current_chapter = 1
    while next_page_url != manga_url:
        next_page_url = download_chapter(next_page_url,manga_name,manga_path,current_chapter)
        current_chapter +=1
        
def make_top_directory():
    home = os.getenv("HOME")
    submanga = home + "/submanga"
    if not os.path.exists(submanga):
        os.makedirs(submanga)
    return submanga

def make_manga_directory(manga_name):
    manga = make_top_directory() + "/"+manga_name
    if not os.path.exists(manga):
        os.makedirs(manga)
    return manga




