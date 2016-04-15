import csv
from xml.dom.minidom import Document

class Csv2Xacro(object):

    def __init__(self, tile_csv_file, tag_csv_file, xacro_file, tile_width, tag_offset):
        self.map_csv = csv.reader(open(tile_csv_file, 'rb'), delimiter=',')
        self.tag_csv = csv.reader(open(tag_csv_file, 'rb'), delimiter=',')
        self.map_xml = open(xacro_file, 'w')
        self.tile_width = tile_width
        self.tag_offset = tag_offset

    def writeXacro(self):

        # Create document
        doc = Document()

        # Create comment
        comment = doc.createComment('WARNING: This file was auto-generated by csv2xacro_node.py. It should not be edited by hand.')
        doc.appendChild(comment)

        # Create root label
        root = doc.createElement('robot')
        root.setAttribute( 'name', 'duckietown' )
        root.setAttribute('xmlns:xacro', 'http://www.ros.org/wiki/xacro')
        doc.appendChild(root)

        # Create Parameters comment
        comment = doc.createComment('Parameters')
        root.appendChild(comment)

        # Create tile width
        tempChild = doc.createElement('xacro:property')
        tempChild.setAttribute('name','tile_width')
        tempChild.setAttribute('value',str(self.tile_width))
        root.appendChild(tempChild)

        # Create tag offsets
        tempChild = doc.createElement('xacro:property')
        tempChild.setAttribute('name','pos_0')
        tempChild.setAttribute('value',str(self.tag_offset)+' 0')
        root.appendChild(tempChild)

        tempChild = doc.createElement('xacro:property')
        tempChild.setAttribute('name','pos_1')
        tempChild.setAttribute('value','0 '+str(self.tag_offset))
        root.appendChild(tempChild)

        tempChild = doc.createElement('xacro:property')
        tempChild.setAttribute('name','pos_2')
        tempChild.setAttribute('value','-'+str(self.tag_offset)+' 0')
        root.appendChild(tempChild)

        tempChild = doc.createElement('xacro:property')
        tempChild.setAttribute('name','pos_3')
        tempChild.setAttribute('value','0 -'+str(self.tag_offset))
        root.appendChild(tempChild)

        # Create comment
        comment = doc.createComment('Include the tile and tag macros')
        root.appendChild(comment)

        # Create file name
        tempChild = doc.createElement('xacro:include')
        tempChild.setAttribute('filename','$(find duckietown_description)/urdf/macros.urdf.xacro')
        root.appendChild(tempChild)

        # Create comment
        comment = doc.createComment('The world frame is at the lower left corner of duckietown')
        root.appendChild(comment)

        # Create link
        tempChild = doc.createElement('link')
        tempChild.setAttribute('name','world')
        root.appendChild(tempChild)

        # Create comment
        comment = doc.createComment('Describe the tiles')
        root.appendChild(comment)

        # Create tiles
        header = True
        for row in self.map_csv:
            if header:
                header = False
                continue
            tempChild = doc.createElement('xacro:tile')
            tempChild.setAttribute('x',row[0].strip('" '))
            tempChild.setAttribute('y',row[1].strip('" '))
            tempChild.setAttribute('type',row[2].strip('" '))
            tempChild.setAttribute('rotation',row[3].strip('" '))
            root.appendChild(tempChild)

        # Create comment
        comment = doc.createComment('Describe the tags')
        root.appendChild(comment)

        # Create tags
        header = True
        for row in self.tag_csv:
            if header:
                header = False
                continue
            tempChild = doc.createElement('xacro:tag')
            tempChild.setAttribute('id', row[0].strip('" '))
            tempChild.setAttribute('x', row[1].strip('" '))
            tempChild.setAttribute('y', row[2].strip('" '))
            tempChild.setAttribute('position', row[3].strip('" '))
            tempChild.setAttribute('rotation', row[4].strip('" '))
            root.appendChild(tempChild)

        # Write to file
        doc.writexml(self.map_xml,indent='    ',addindent='    ',newl='\n')

        # Close file
        self.map_xml.close()