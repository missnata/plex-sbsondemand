from config import *
from item import *

VIDEO_PREFIX = '/video/sbsondemand'

def Start():
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')


@handler(VIDEO_PREFIX, L('Title'), art=Config.ART, thumb=Config.ICON)
def MainMenu():
    oc = ObjectContainer(view_group='InfoList')

    for item in GetList():
        if item.has_children:
            oc.add(DirectoryObject(
                key=Callback(SubMenu, id=item.id),
                thumb=item.thumb,
                title=item.title))
        else:
            oc.add(DirectoryObject(
                key=Callback(EpisodeMenu, id=item.id, url=item.path),
                thumb=item.thumb,
                title=item.title))

    return oc


def GetList():
    json = JSON.ObjectFromURL(Config.MENU_URL, cacheTime=Config.MENU_CACHE)

    menu = []
    for main_menu in json['get']['response']['Menu']['children']: #only 1 Browse
        for sub_menu in main_menu['children']:
            if sub_menu['clickable'] == '1' or sub_menu['clickable'] == 1:
                menu.append(Item.MapFromJson(sub_menu))

    return menu

def GetChildren(id):
    json = JSON.ObjectFromURL(Config.MENU_URL, cacheTime=Config.MENU_CACHE)

    menu = []
    for main_menu in json['get']['response']['Menu']['children']: #only 1 Browse
        for sub_menu in main_menu['children']:
            if sub_menu['id'] == id:
                for item in sub_menu['children']:
                    menu.append(Item.MapFromJson(item))

    return menu


@route(VIDEO_PREFIX + '/submenu/{id}')
def SubMenu(id):
    oc = ObjectContainer(view_group='InfoList')

    for item in GetChildren(id):
        oc.add(DirectoryObject(
            key=Callback(EpisodeMenu, id=item.id, url=item.path),
            thumb=item.thumb,
            title=item.title))

    return oc


@route(VIDEO_PREFIX + '/episodemenu/{id}')
def EpisodeMenu(id, url):
    json = JSON.ObjectFromURL(url)

    oc = ObjectContainer(view_group='InfoList')

    for ep in json['entries']:
        video_url = Config.EPISODE_URL % (ep['id'].split('/')[-1])
        oc.add(GetVideo(ep['title'], ep['plmedia$defaultThumbnailUrl'], video_url))

    return oc


@route(VIDEO_PREFIX + '/episode/play')
def GetVideo(title, thumb, url):
    return EpisodeObject(
        title = title,
        thumb = thumb,
        url = url
    )
