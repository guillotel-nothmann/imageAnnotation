# TMG_ImageAnnotation

TMG_ImageAnnotation is a Python module for viewing and editing OCR outputs and segmentation ground truth. The software is developed in the context of the project [Thesaurus Musicarum Germanicarum](http://tmg.huma-num.fr/), dedicated to  printed music theory of the modern era (1470-1750). The viewer shows the page layout as a transparent overlay on the document image. Text regions  (paragraphs, headins, captions, drop capitals, graphics, music examples, etc.) are displayed as tooltips and can be edited.
TMG_ImageAnnotation takes [METS-data](http://www.loc.gov/standards/mets/) as input and stores image annotations in the [PAGE XML](https://github.com/PRImA-Research-Lab/PAGE-XML/wiki) format. The project is designed to be embedded in the [OCR-D](https://ocr-d.de/) initiative. It aims to improve especially the page segmentation step that remains critical in OCR workflows for historical sources.


## Installation

TMGImageAnnotation is written in Python. It is based on the matplotlib library and requires lxml and numpy. Install [Python3](https://www.python.org/downloads/release/python-377/) and the resources below if they are not available on your machine:

```bash
pip3 install numpy
pip3 install lxml
pip3 install matplotlib
```
Download or clone this project.

```bash
git clone https://github.com/guillotel-nothmann/imageAnnotation.git
```

## Usage

Open a terminal navigate to the src folder and run main.py
```bash
cd ImageAnnotation/src 
python3 main.py
```

Once launched, open a METS file that points to page regions via PAGE files with image urls. 

Use the following commands to navigate and to edit:
* Quit : "ctrl+q"
* Open: mac: "command+O", windows: alt+o
* Save: mac: "command+S", windows: alt+s
* Display polygon information: right click on the polygon 
* Edit polygon information: select a polygon and press "+" 
* Add coordinates: click on the polygon lines and press "i"
* Delete coordinates: click on a polygon point and press "d"
* Delete whole region: select polygon and press "backspace"
* Zoom: shift+mouse selection
* Unzoom: control + mouse click
* Next page: "right"
* Previous page: "left"




Polygon regions can be added using the buttons or the following key combinations: 
* "shift+C": caption
* "shift+D": drop capital
* "shift+F": footer
* "shift+F": footnote
* "shift+G": graphic
* "ctrl+h": header
* "shift+H": heading
* "shift+I": image
* "ctrl+l": linedrawing
* "shift+M": marginalia
* "shift+O": other
* "shift+P": paragraph
* "ctrl+s": separator
* "shift+S": staff notation
* "shift+T": tablature notation
* "ctrl+t": table 
* "shift+Z": list


## Example
Run TMGImageAnnotation:


```bash
cd ImageAnnotation/src 
python3 main.py
```
Open the mets.xml file located in the followin folder: "/ImageAnnotation/annotationExample".
You should see the following example and should be able to edit its region annotation.

![ImageAnnotationExample](https://github.com/guillotel-nothmann/imageAnnotation/blob/master/ImageAnnotation/annotationExample/annotationExemple.png?raw=true)
          

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate. 
## License
CC BY-NC-SA 
