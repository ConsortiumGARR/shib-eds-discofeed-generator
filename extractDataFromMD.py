#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from operator import itemgetter
from collections import OrderedDict

import sys, getopt
import json

#OUTPUT="/opt/metadata-to-json/output"

# Get MDUI Keywords
def getEntityID(EntityDescriptor, namespaces):
    return EntityDescriptor.get('entityID')


# Get MDUI Keywords
def getKeywords(EntityDescriptor,namespaces,entType='idp'):

    kw_list = list()
    if (entType.lower() == 'idp'):
       keywords = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Keywords", namespaces)
    if (entType.lower() == 'sp'):
       keywords = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Keywords", namespaces)

    for kw in keywords:
        kw_dict = dict()
        kw_dict['value'] = kw.text
        kw_dict['lang'] = kw.get("{http://www.w3.org/XML/1998/namespace}lang")
        kw_list.append(kw_dict)

    return kw_list


# Get MDUI Privacy Policy
def getPrivacyStatementURLs(EntityDescriptor,namespaces,entType='idp'):

    pp_list = list()
    if (entType.lower() == 'idp'):
       privacy_policies = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementURL", namespaces)
    if (entType.lower() == 'sp'):
       privacy_policies = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementURL", namespaces)

    for pp in privacy_policies:
        pp_dict = dict()
        pp_dict['value'] = pp.text
        pp_dict['lang'] = pp.get("{http://www.w3.org/XML/1998/namespace}lang")
        pp_list.append(pp_dict)

    return pp_list



# Get MDUI InformationURLs
def getInformationURLs(EntityDescriptor,namespaces,entType):

    info_list = list()
    if (entType.lower() == 'idp'):
       info_pages = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:InformationURL", namespaces)
    if (entType.lower() == 'sp'):
       info_pages = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:InformationURL", namespaces)

    for infop in info_pages:
        info_dict = dict()
        info_dict['value'] = infop.text
        info_dict['lang'] = infop.get("{http://www.w3.org/XML/1998/namespace}lang")
        info_list.append(info_dict)

    return info_list


# Get MDUI DisplayName
def getDisplayNames(EntityDescriptor,namespaces,entType='idp'):

    displayName_list = list()
    if (entType.lower() == 'idp'):
       displayNames = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:DisplayName", namespaces)
    if (entType.lower() == 'sp'):
       displayNames = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:DisplayName", namespaces)

    for dispName in displayNames:
        displayName_dict = dict()
        displayName_dict['value'] = dispName.text
        displayName_dict['lang'] = dispName.get("{http://www.w3.org/XML/1998/namespace}lang")
        displayName_list.append(displayName_dict)
    
    return displayName_list


# Get MDUI Descriptions
def getDescriptions(EntityDescriptor,namespaces,entType='idp'):

    description_list = list()
    if (entType.lower() == 'idp'):
       descriptions = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Description", namespaces)
    if (entType.lower() == 'sp'):
       descriptions = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Description", namespaces)

    for desc in descriptions:
        descriptions_dict = dict()
        descriptions_dict['value'] = desc.text
        descriptions_dict['lang'] = desc.get("{http://www.w3.org/XML/1998/namespace}lang")
        description_list.append(descriptions_dict)
    
    return description_list


# Get MDUI Logos
def getLogos(EntityDescriptor,namespaces,entType='idp'):

    logos_list = list()
    if (entType.lower() == 'idp'):
       logo_urls = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Logo", namespaces)
    if (entType.lower() == 'sp'):
       logo_urls = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Logo", namespaces)

    for logo in logo_urls:
        logo_dict = dict()
        logo_dict['value'] = logo.text
        logo_dict['width'] = logo.get("width")
        logo_dict['height'] = logo.get("height")
        logo_dict['lang'] = logo.get("{http://www.w3.org/XML/1998/namespace}lang")
        logos_list.append(logo_dict)

    return logos_list



def main(argv):
   try:
      # 'm:o:hd' means that 'm' and 'o' needs an argument(confirmed by ':'), while 'h' and 'd' don't need it
      opts, args = getopt.getopt(sys.argv[1:], 'm:o:hd', ['metadata=','output=','help','debug' ])
   except getopt.GetoptError as err:
      print (str(err))
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The DiscoFeed JSON content will be put in the output file")
      sys.exit(2)

   inputfile = None
   outputfile = None
   idp_outputfile = None

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
         print ("The DiscoFeed JSON content will be put in the output file")
         sys.exit()
      elif opt in ('-m', '--metadata'):
         inputfile = arg
      elif opt in ('-o', '--output'):
         outputfile = arg
      elif opt == '-d':
         global _debug
         _debug = 1
      else:
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
         print ("The DiscoFeed JSON content will be put in the output file")
         sys.exit()

   namespaces = {
      'xml':'http://www.w3.org/XML/1998/namespace',
      'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
      'mdrpi': 'urn:oasis:names:tc:SAML:metadata:rpi',
      'shibmd': 'urn:mace:shibboleth:metadata:1.0',
      'mdattr': 'urn:oasis:names:tc:SAML:metadata:attribute',
      'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
      'ds': 'http://www.w3.org/2000/09/xmldsig#',
      'mdui': 'urn:oasis:names:tc:SAML:metadata:ui'
   }

   if inputfile == None:
      print ("Metadata file is missing!\n")
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The DiscoFeed JSON content will be put in the output file")
      sys.exit()

   if outputfile == None:
      print ("Output file is missing!\n")
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The DiscoFeed JSON content will be put in the output file")
      sys.exit()


   tree = ET.parse(inputfile)
   root = tree.getroot()
   idp = root.findall("./md:EntityDescriptor[md:IDPSSODescriptor]", namespaces)

   idps = dict()

   list_eds = list()
   list_idp = list()

   for EntityDescriptor in idp:

      ecs = "NO EC SUPPORTED"
      pp_flag = "Privacy Policy assente"
      info_flag = "Info Page assente"
      logo_flag = "Logo non presente"

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get MDUI DisplayName
      displayName_list = getDisplayNames(EntityDescriptor,namespaces,'idp')

      # Get MDUI Descriptions
      description_list = getDescriptions(EntityDescriptor,namespaces,'idp')

      # Get MDUI Keywords
      keyword_list = getKeywords(EntityDescriptor,namespaces,'idp')

      # Get MDUI Privacy Policy
      pp_list = getPrivacyStatementURLs(EntityDescriptor,namespaces,'idp')

      if (len(pp_list) != 0):
         pp_flag = 'Privacy Policy presente'

      # Get MDUI Info Page
      info_list = getInformationURLs(EntityDescriptor,namespaces,'idp')

      if (len(info_list) != 0):
         info_flag = 'Information Page presente'

      # Get MDUI Logos
      logos_list = getLogos(EntityDescriptor,namespaces,'idp')

      if (len(logos_list) != 0):
         logo_flag = 'Logo presente'

      eds = OrderedDict([
        ('entityID',entityID),
        ('DisplayNames',displayName_list),
        ('Descriptions',description_list),
        ('Keywords',keyword_list),
        ('PrivacyStatementURLs', pp_list),
        ('InformationURLs', info_list),
        ('Logos', logos_list)
      ])

      list_eds.append(eds)

   
   result_eds = open(outputfile, "w",encoding=None)
   result_eds.write(json.dumps(sorted(list_eds,key=itemgetter('entityID')),sort_keys=False, indent=4, ensure_ascii=False))
   result_eds.close()


if __name__ == "__main__":
   main(sys.argv[1:])
