'''
Created on Jul 1, 2020

@author: christophe
'''

import json
from ocrolib.sl import area
from exportData.readXML import ReadWriteMets, ReadWritePageXML
from PIL import Image

class CreateDataset(object):
    def __init__(self):
        self.data = {}
        self.info = {}
        self.type = {}
        self.licences = []
        
        self.region2Id={}
        
        categories = [
            ["TextRegion", 1, "paragraph"],
            ["TextRegion", 2, "caption"],
            ["TextRegion", 3, "header"],
            ["TextRegion", 4, "heading"],
            ["TextRegion", 5, "footer"],
            ["TextRegion", 6, "drop-capital"],
            ["TextRegion", 7, "marginalia"],
            ["TextRegion", 8, "footnote"],
            ["TextRegion", 9, "linegroup"],
            
            ["other", 10, "list"], # careful, this should be "textRegion"
            ["MusicRegion", 11, "staffNotation"],
            ["MusicRegion", 12, "tablatureNotation"],
            ["TableRegion", 13, "table"],
            ["GraphicRegion", 14, "graphic"],
            ["ImageRegion", 15, "image"],
            ["LineDrawingRegion", 16, "linedrawing"],
            ["SeparatorRegion", 17, "separator"] ,

            ["other", 18, "other"]
            ]

        
        self.data["licence"] = []
        self.data["info"] = []
        self.data["images"] = []
        self.data["type"] = []
        self.data["annotations"] = []
        self.data["categories"] = []
        
        self.setInfo()
        self.setLicence()
        self.setType()
        self.setCateories(categories)
        
        
    def addAnnotation (self, segmentation=[], area=None, iscrowd=None, image_id = None, bbox = [], category_id = None, ident = None ):
        annotation = {}
        annotation["segmentation"]= [segmentation]
        annotation["area"]= area
        annotation ["iscrowd"] = iscrowd
        annotation ["image_id"] = image_id
        annotation ["bbox"] = bbox
        annotation ["category_id"] = category_id
        annotation ["id"] = ident
        self.data["annotations"].append (annotation)
        
        
    def addCategory (self, supercategory=None, ident = None, name = None):
        category= {}
        category["supercategory"]= supercategory
        category["id"]= ident
        category["name"]= name
        self.data["categories"].append(category)
        
    
    def addImage (self, licence=None, url=None, file_name=None, height=None, width=None, date_captured=None, ident=None):
        image = {}
        image ["licence"]= licence
        image ["url"]= url
        image ["file_name"] = file_name
        image ["height"] = height
        image ["width"] = width
        image ["date_captured"] = date_captured
        image ["id"] = ident
        self.data["images"].append(image) 
    
    
    def addCollection(self, metsFilePath, filterPage = None):
        ''' this takes a mets file as an input '''
        rwMets = ReadWriteMets(metsFilePath)
        filePathGroup = rwMets.getFileGroup()
        splitFilePath = metsFilePath.split("/")
        
        rootdirectory = metsFilePath.replace(splitFilePath[-1], "")
        
        
        ''' loop over every file '''
        for relativeFilePath in filePathGroup:
            
            if filterPage != None:
                pathWithoutExtension = relativeFilePath.replace(".xml", "")
                splitPath = pathWithoutExtension.split("-")
                
                fileNumber = splitPath[-1]
                
                if not int(fileNumber) in filterPage: 
                    continue 
            
                
            
            filePath = rootdirectory + relativeFilePath
            
            
       
                
                
            rwPage = ReadWritePageXML(filePath) 
            
            ''' add image information '''
            imageRelativePath = rwPage.getImagePath()
            imageFilePath = rootdirectory + imageRelativePath
            splitImageFilePath = imageFilePath.split("/")
            imageFileName = splitImageFilePath[-1]
            im = Image.open(imageFilePath)
        
    
            splitFilePath = filePath.split("/")
            licence = ""
            url = ""
            file_name = splitFilePath[-1]
            
            
            width, height = im.size
            date_captured=""
            imageIdent=file_name.replace(".xml", "")
            self.addImage(licence, url, imageFileName, height, width, date_captured, imageIdent) 
            
            
            regionList = rwPage.readPageRegionXML()
            
            
            ''' add region information '''
            for region in regionList:
                segmentation=[]
                
                if len(region.coordinates) == 4:
                    region.coordinates.append(region.coordinates[-1])
                    
                    print (region.coordinates)
                    print (filePath)
                    continue
                
                
                
                coordinatePair = region.coordinates[0]
                highestX = float(coordinatePair[0])
                highestY = float(coordinatePair[1])
                lowestX = float(coordinatePair[0])
                lowestY = float(coordinatePair[1])  
                
                for coordinatePair in region.coordinates: 
                    if highestX < coordinatePair[0]: highestX = coordinatePair[0]
                    if highestY < coordinatePair[1]: highestY = coordinatePair[1]
                    if lowestX > coordinatePair[0]: lowestX = coordinatePair[0]
                    if lowestY > coordinatePair[1]: lowestY = coordinatePair[1]
            
                    segmentation.append(float(coordinatePair[0]))
                    segmentation.append(float(coordinatePair[1]))
                    
                    
                
                
                
                    
                regionWidth = highestX-lowestX
                regionHight = highestY - lowestY
                area =  regionWidth * regionHight
                iscrowd=0
                image_id = imageIdent
                bbox = [lowestX, lowestY, regionWidth, regionHight]
                category_id = self.region2Id[region.regionName]
                annotationIdent = file_name.replace(".xml", "") + "_" + str(region.index)
                
                self.addAnnotation(segmentation, area, iscrowd, image_id, bbox, category_id, annotationIdent)
                    
                     
       
            
            
        
        
        
        
    def setCateories(self, categories):
        
        for category in categories :
            self.addCategory(category[0], category[1], category[2])
            self.region2Id[category[2]] = category[1]
        
        
        
         
        
        
         
     
    def setLicence (self):
        licence = {} 
        licence ["url"] = "http://creativecommons.org/licenses/by-nc-sa/2.0/"
        licence ["id"]= 1
        licence ["name"] = "Attribution-NonCommercial-ShareAlike License"
        self.licences.append(licence)
        self.data["licence"]=self.licences
        
    
    def setInfo (self): 
        self.info ["description"] = "This is stable 1.0 version of the 2020 TMG page annotation data set"
        self.info ["url"] = "https://github.com/guillotel-nothmann/imageAnnotationGroundTruth"
        self.info ["version"] = "version 1"
        self.info ["year"] = 2020
        self.info ["contributor"] = "Christophe Guillotel-Nothmann, Anne Legrand"
        self.info ["date_created"] = "2020-07-02"
        self.data["info"]=self.info
        
        
    def setType (self):
        self.data["type"] = "instances"
        
        
   
        
        
        
    def writeJson (self, filePath):
        with open(filePath + "/dataset.json", 'w') as outfile:
            json.dump(self.data, outfile)
        
    
    
        
 
        
        
        