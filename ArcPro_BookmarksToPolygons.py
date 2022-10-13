# Import modules
import arcpy, os

# Get Parameters and create blank feature
layoutName = arcpy.GetParameterAsText(0) # Layout - name of target layout
mapFrame = arcpy.GetParameterAsText (1) # String - name of target map frame
output_dir = arcpy.GetParameterAsText(2) # Folder
output_name = arcpy.GetParameterAsText(3) # String - "include .shp"
coordsys = arcpy.GetParameterAsText(4) # CoordinateSystem

aprx = arcpy.mp.ArcGISProject("CURRENT")
lyt = aprx.listLayouts(layoutName)[0]
mf = lyt.listElements("MAPFRAME_ELEMENT", mapFrame)[0]
FC = arcpy.management.CreateFeatureclass(output_dir,output_name,'POLYGON',"","DISABLED","DISABLED",coordsys)
#add bookmark name field to FC
arcpy.management.AddField(FC, "NAME", "TEXT" )

for m in aprx.listMaps():
    for bkmks in m.listBookmarks():
        mf.zoomToBookmark(bkmks)
        extent = mf.camera.getExtent()
        #create polygon from bookmark extent
        polygon = extent.polygon
        name = bkmks.name
        row_values = [(name, polygon)]
        icur = arcpy.da.InsertCursor(FC, ["NAME", 'SHAPE@'])
        #insert name and extent to FC
        for row in row_values:
            icur.insertRow(row)
        del icur
        arcpy.AddMessage("Created polygon for bookmark " + name)

#add FC to map
map = aprx.listMaps()[0]
map.addDataFromPath(output_dir + "\\" + output_name)
arcpy.AddMessage(output_name + " added to map")

