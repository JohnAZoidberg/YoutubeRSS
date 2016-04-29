#!/usr/bin/python
from lxml.etree import Element, SubElement, tostring, CDATA

itunes = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
atom = 'http://www.w3.org/2005/Atom'
NSMAP = {'itunes': itunes, 'atom': atom}

def buildNS(ns, name):
    return "{%s}%s" % (ns, name)

class PodcastFeed():
    def __init__(self,
        title=None,
        desc=None,
        lng='en-us',
        copyright=None,
        link=None,
        lastBuildDate=None, # TODO format date
        image=None,
        category='',
        channelName=None
    ):
        # TODO check if args are None and throw error
        # TODO HTMLencode all inputs

        self.root = Element('rss', {'version': '2.0'}, nsmap=NSMAP)
        self.channelE = SubElement(self.root, 'channel')
        titleE = SubElement(self.channelE, 'title')
        titleE.text = title
        descE = SubElement(self.channelE, 'description')
        #descE.text = desc
        descE.text = CDATA(desc)
        summaryE = SubElement(self.channelE, buildNS(itunes, 'summary'))
        summaryE.text = CDATA(desc)
        lngE = SubElement(self.channelE, 'language')
        lngE.text = lng
        copyrightE = SubElement(self.channelE, 'copyright')
        copyrightE.text = copyright
        linkE = SubElement(self.channelE, 'link')
        linkE.text = 'https://www.youtube.com/user/' + channelName
        atomLinkE = SubElement(self.channelE, buildNS(atom, 'link'), {'href': link, 'rel': 'self', 'type': 'application/rss+xml'})
        lastBuildDateE = SubElement(self.channelE, 'lastBuildDate')
        lastBuildDateE.text = lastBuildDate
        authorE = SubElement(self.channelE, buildNS(itunes, 'author'))
        authorE.text = title
        ownerE = SubElement(self.channelE, buildNS(itunes, 'owner'))
        ownerNameE = SubElement(ownerE, buildNS(itunes, 'name'))
        ownerNameE.text = title
        explicitE = SubElement(self.channelE, buildNS(itunes, 'explicit'))
        explicitE.text = 'No'
        imageE = SubElement(self.channelE, buildNS(itunes, 'image'), {'href': image})
        categoryE = SubElement(self.channelE, buildNS(itunes, 'category'), {'text': category})
        categoryE.text = ""

    def addItem(self,
        title=None,
        link=None,
        size="1", # TODO should be figured out automatically
        desc=None,
        pubDate=None
    ):


        itemE = SubElement(self.channelE, 'item')
        iTitleE = SubElement(itemE, 'title')
        iTitleE.text = title
        iLinkE = SubElement(itemE, 'link')
        iLinkE.text = link
        iGuidE = SubElement(itemE, 'guid')
        iGuidE.text = link
        iEnclosureE = SubElement(itemE, 'enclosure', {'url': link, 'length': size, 'type': 'audio/mp4'})
        iSummaryE = SubElement(itemE, buildNS(itunes, 'summary'))
        iSummaryE.text = CDATA(desc)
        iDescE = SubElement(itemE, 'description')
        iDescE.text = CDATA(desc)
        iCategoryE = SubElement(itemE, 'category')
        iCategoryE.text = 'Podcasts'
        iPubDate = SubElement(itemE, 'pubDate')
        iPubDate.text = pubDate

    def to_string(self):
        return tostring(self.root)