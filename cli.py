from downloader import *
def cli():
    make_top_directory()
    manga_list = get_manga_list()
    print_manga_list(manga_list)
    manga = int(input("Introducir numero para seleccionar manga >>> "))
    manga_link = manga_list[manga-1]
    manga_name = manga_link.split("/")[-1]
    download_manga(manga_link,manga_name)
cli()
