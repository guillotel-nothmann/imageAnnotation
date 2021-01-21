import numpy as np
import skimage.io 
from skimage.measure import find_contours, approximate_polygon
from mrcnn.config import Config
import mrcnn.model as modellib 
import os
from skimage import color
import editor
import math

class InferenceConfig(Config):
    
    # Give the configuration a recognizable name
    NAME = "coco"
    
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES=19
    
     

class RegionAnalysis(object):

    def __init__(self):
        # Root directory of the project
        ROOT_DIR = os.path.abspath("../")
    
        # Config
        config = InferenceConfig()
        
        
        # ModeDirectory
        MODEL_DIR = ROOT_DIR + "/models"
        
        # Local path to trained weights file
        model_path = MODEL_DIR +"/mask_rcnn_tmg_regions.h5"
        
        
        self.class_names = ["bg", #0
                            "paragraph",
                            "caption",
                            "header",
                            "heading",
                            "footer", #5
                            "drop-capital",
                            "marginalia",
                            "footnote",
                            "linegroup",
                            "list",#10
                            "staffNotation",
                            "tablatureNotation",
                            "table",
                            "graphic",
                            "image",#15
                            "linedrawing",
                            "separator", 
                            "other"]

        
        # Create model object in inference mode.
        # Create model
        self.model = modellib.MaskRCNN(mode="inference",   config=config, model_dir=MODEL_DIR)
        
        # Load trained weights
        print("Loading weights from ", model_path)
        self.model.load_weights(model_path, by_name=True)
        
    
    def inferRegions(self, imagePath):
        image = skimage.io.imread(imagePath)
        image =  color.gray2rgb(image)
        
        
        hight = image.shape[0]
        width = image.shape [1]
        
        #tolerance mask => polygon 
        tolerance = math.sqrt((width*hight) * 0.00005) 
        
        print (tolerance)
        
        # Run detection
        results = self.model.detect([image], verbose=1)
        r = results[0]
        
        ### extract polygons
        regionList = []
        
        for regionNumber in range (r['rois'].shape[0]):
            
            mask = r['masks'][:, :, regionNumber] 
            # Mask Polygon
            # Pad to ensure proper polygons for masks that touch image edges.
            padded_mask = np.zeros( (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
            padded_mask[1:-1, 1:-1] = mask
            contours = find_contours(padded_mask, 0.5)
            
            # get only largest contour ??? # 
            
            verts = contours [0] 
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            
            #approximate
            appr_polygon = approximate_polygon(verts, tolerance)
            region = editor.TextRegion(appr_polygon, "regionID", 0, None, None, None)
            
             
            
            print (r['class_ids'][regionNumber])
            print (len (self.class_names))
            
            region.regionName = self.class_names[r['class_ids'][regionNumber]]
            regionList.append(region) 
        return regionList
        
        
        


    
        