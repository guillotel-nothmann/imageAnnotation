''' Used to export data from page documents and store them in json coco format '''

from exportData import createDataset
 
if __name__ == '__main__':
    
    ''' create coco model instance '''
    
    cocoModel = createDataset.CreateDataset()
    
    
    #Alsted 
    cocoModel.addCollection("/Users/christophe/Documents/GitHub/imageAnnotationGroundTruth/Alsted_1620/data/mets.xml", range(1,20+1))
    
    #Burmeister 
    cocoModel.addCollection("/Users/christophe/Documents/GitHub/imageAnnotationGroundTruth/Burmeister_1599/data/mets.xml", range(4,75+1))
    
    #Matthaei 
    cocoModel.addCollection("/Users/christophe/Documents/GitHub/imageAnnotationGroundTruth/Matthaei_1652/data/mets.xml", range(6,70+1))
    
    cocoModel.writeJson("/Users/christophe/Documents/GitHub/imageAnnotationGroundTruth/annotation")
    
    
    
    
    
    
    print (cocoModel) 
    