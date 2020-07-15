 
from lxml import etree as ET 


class ReadWriteMets ():
    def __init__(self, xmlFilePath):
        self.xmlFilePath = xmlFilePath
        
        self.metsNameSpace = "http://www.loc.gov/METS/"
        self.metsNameEntry = "{http://www.loc.gov/METS/}"
        self.xlinkNameSpace = "http://www.w3.org/1999/xlink"
        self.xlinkNameEntry = "{http://www.w3.org/1999/xlink}"
        self.nameSpaceDictionary =  {"mets": self.metsNameSpace, "xlink": self.xlinkNameSpace}
        self.tree = ET.parse(xmlFilePath) 
    
    def getFileGroup (self, fileGroup="OCR-D-SEG-REGION"):
        self.fileGroupList = []   
        for groupeFile in self.tree.xpath('//mets:fileGrp[@USE="%s"]/mets:file/mets:FLocat' % (fileGroup), namespaces = self.nameSpaceDictionary): 
            if  "{http://www.w3.org/1999/xlink}href" in groupeFile.attrib: 
                self.fileGroupList.append(groupeFile.attrib["{http://www.w3.org/1999/xlink}href"])  
        return self.fileGroupList


class ReadWritePageXML(object): 
    def __init__(self, xmlFilePath):
        self.pcNameSpace = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
        self.pcNameEntry = "{http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15}"
         
        ''' read xml files '''
        self.xmlFilePath = xmlFilePath
        self.nameSpaceDictionary =  {"pc": self.pcNameSpace}
        self.regionRefDictionary = {}
        self.textRegionList = []
        self.regionDictionary = ["TextRegion", "GraphicRegion", "ImageRegion", "LineDrawingRegion", "MusicRegion", "TableRegion", "SeparatorRegion" ]
         
  
        self.tree = ET.parse(xmlFilePath)
         
 
    def getCoordinates(self):
        return self.coordinatesList
     
    def getImagePath(self): 
        ''' try to use de binarized image '''
        for alternativeImage in self.tree.xpath('//pc:Page/pc:AlternativeImage[@comments="binarized"]', namespaces = self.nameSpaceDictionary):
            if "filename" in alternativeImage.attrib: return alternativeImage.attrib["filename"]
             
        ''' if binarized image cannot be found, use original '''
        for ocrpage in self.tree.xpath('//pc:Page', namespaces = self.nameSpaceDictionary):
            if "imageFilename" in ocrpage.attrib: return ocrpage.attrib["imageFilename"]
             
        return None
         
     
    def readPageRegionXML(self): 
        ''' build reading order dictionary '''
         
        for regionRef in self.tree.xpath("//pc:RegionRefIndexed", namespaces = self.nameSpaceDictionary): 
            regionIndex = None
            regionReference = None
             
            if "index" in regionRef.attrib: regionIndex = regionRef.attrib["index"]
            if "regionRef" in regionRef.attrib: regionReference = regionRef.attrib["regionRef"]
             
            if regionIndex == None or regionReference == None: continue
            self.regionRefDictionary[regionReference] = regionIndex 
         
         
        ''' loop over every region of interest '''
        for region in self.regionDictionary:
         
            for regionClass in self.tree.xpath("//pc:" +region, namespaces = self.nameSpaceDictionary): 
                regionId = None
                regionType = None
                custom = None
                if "id" in regionClass.attrib: regionId = regionClass.attrib["id"]
                if "type" in regionClass.attrib: regionType = regionClass.attrib["type"]
                if "custom" in regionClass.attrib: custom = regionClass.attrib["custom"]
      
                 
                 
                 
                for coordinates in regionClass:
                    if coordinates.tag == self.pcNameEntry+"Coords":
                        if "points" in coordinates.attrib: 
                            coordsStringList = coordinates.attrib["points"].split(" ") 
                             
                            if len (coordsStringList) <= 1:  break # make sure that the region as at least two coordinates
                                 
     
                                 
                            coordinatesList = []
                            for coordinateString in coordsStringList: 
                                coordinatesList.append([int(i) for i in coordinateString.split(",")] )
                            regionIndex = None
                          
                             
                            if regionId in self.regionRefDictionary: 
                                regionIndex= self.regionRefDictionary[regionId]
                            else:
                                print ("region index not identified for region id" + regionId + " Skipping this region")
                                continue
                              
                             
                            textR = TextRegion(coordinatesList, regionId, regionIndex, regionType, regionClass.tag.replace(self.pcNameEntry, ""), custom)
                            textR.imagePath = self.getImagePath()
                            splitFileName = textR.imagePath.split("/")
                            textR.imageFileName = splitFileName[-1]
                             
                             
                            self.textRegionList.append(textR)
   
        ''' sort text regions accordin to index'''
         
        self.textRegionList = sorted(self.textRegionList, key=lambda textRegion: textRegion.index)
         
         
        return self.textRegionList
     
class TextRegion(object):
    def __init__(self, regionCoordinates,regionId, regionIndex, regionType, regionClass, custom=None):
        self.coordinates = regionCoordinates
        self.regionClass = regionClass
        self.type = regionType
        self.id = regionId
        self.index = int(regionIndex) 
        self.custom = custom
        self.regionName = None # this is not part of xml schema but used in matplot only 
        self.imagePath = None
        self.imageFileName = None
         
         
        if self.regionClass == "TextRegion":
            if self.type in ["paragraph", "caption", "header", "heading", "footer", "drop-capital", "marginalia", "footnote"]:
                self.regionName = self.type   
             
            elif self.type == "other":
                if self.custom == "list":
                    self.regionName = self.custom
                elif self.custom == "linegroup":
                    self.regionName = self.custom
                    
                
                else : 
                    self.regionName = "other"
                 
             
            else: self.regionName = "other"
                 
                 
         
         
         
        elif self.regionClass == "MusicRegion": 
            if self.custom=="staffNotation": self.regionName=  "staffNotation"
            elif self.custom == "tablatureNotation": self.regionName = "tablatureNotation"
                 
        elif self.regionClass == "TableRegion": self.regionName = "table"
        elif self.regionClass == "GraphicRegion": self.regionName = "graphic"
        elif self.regionClass == "ImageRegion": self.regionName = "image"
        elif self.regionClass == "LineDrawingRegion": self.regionName = "linedrawing"
        elif self.regionClass == "SeparatorRegion": self.regionName = "separator"
         