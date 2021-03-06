# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LULC.py
# Created on: 2016-11-19 16:13:35.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: LULC <Workspace_Folder> <SRTMGL1> <PCS_in_UTM> <cell_size> <GFC_2000> <GFC_loss> <GFC_gain> <GLC30> <LandCover_lyr> <Polygon_for_Clip> <use_geometry> 
# Description: 
# This tool merges GlobeLand30 and GlobalForestChange (state 2012) data into a single LandCover raster. Performing cell resampling and alligment to SRTM 1sec DEM.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
Workspace_Folder = arcpy.GetParameterAsText(0)

SRTMGL1 = arcpy.GetParameterAsText(1)

PCS_in_UTM = arcpy.GetParameterAsText(2)
if PCS_in_UTM == '#' or not PCS_in_UTM:
    PCS_in_UTM = "PROJCS['WGS_1984_UTM_Zone_36N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',33.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]" # provide a default value if unspecified

cell_size = arcpy.GetParameterAsText(3)
if cell_size == '#' or not cell_size:
    cell_size = "25 25" # provide a default value if unspecified

GFC_2000 = arcpy.GetParameterAsText(4)

GFC_loss = arcpy.GetParameterAsText(5)

GFC_gain = arcpy.GetParameterAsText(6)

GLC30 = arcpy.GetParameterAsText(7)

LandCover_lyr = arcpy.GetParameterAsText(8)

Polygon_for_Clip = arcpy.GetParameterAsText(9)

use_geometry = arcpy.GetParameterAsText(10)
if use_geometry == '#' or not use_geometry:
    use_geometry = "false" # provide a default value if unspecified

# Local variables:
GLC30_tif = GLC30
GLC30_no_forest_tif = "%Workspace Folder%\\GlobeLand30_noforest.tif"
DEM_25m_tif = "%Workspace Folder%\\DEM_25m.tif"
GLC30_aux_tif = "%Workspace Folder%\\GlobeLand30_restoDEM.tif"
LandCover_aux_tif = GLC30_aux_tif
GFC_loss_1_tif = "%Workspace Folder%\\treecover_loss_1.tif"
GFC_loss___gain = GFC_loss_1_tif
GFC_gain_50_tif = "%Workspace Folder%\\treecover_gain_50.tif"
GFC_loss___gain_aux_tif = "%Workspace Folder%\\treecover_loss_gain(aux2).tif"
GFC_2012_aux1_tif = GFC_loss___gain_aux_tif
GFC_2012_aux2_tif = "%Workspace Folder%\\treecover2012_actual.tif"
GFC_2012_tif = "%Workspace Folder%\\treecover2012_actual_Proj.tif"
LandCover_tif = LandCover_aux_tif
Water_mask = "%Workspace Folder%\\Water_mask.tif"
LandCover_tif__ATable_ = LandCover_tif
LandCover_tif__Field_ = LandCover_tif__ATable_
LandCover_tif__write_Field_ = LandCover_tif__Field_
LandCover_clip_tif = "%Workspace Folder%\\LandCover_clip.tif"
DEM_25m_clip_tif = "%Workspace Folder%\\DEM_25m_clip.tif"

# Process: Define GLC30 Projection
arcpy.DefineProjection_management(GLC30, PCS_in_UTM)

# Process: Exclude forest
arcpy.gp.Reclassify_sa(GLC30_tif, "", "10 21;20 22;30 22;40 23;50 24;60 25;70 26;80 27;90 28;100 29", GLC30_no_forest_tif, "DATA")

# Process: Project DEM
arcpy.ProjectRaster_management(SRTMGL1, DEM_25m_tif, PCS_in_UTM, "BILINEAR", cell_size, "", "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")

# Process: Resample to DEM resolution
tempEnvironment0 = arcpy.env.snapRaster
arcpy.env.snapRaster = DEM 25m.tif
arcpy.Resample_management(GLC30_no_forest_tif, GLC30_aux_tif, cell_size, "NEAREST")
arcpy.env.snapRaster = tempEnvironment0

# Process: Reclassify loss
arcpy.gp.Reclassify_sa(GFC_loss, "", "0 NODATA;1 1", GFC_loss_1_tif, "DATA")

# Process: Reclassify gain
arcpy.gp.Reclassify_sa(GFC_gain, "", "0 NODATA;1 50", GFC_gain_50_tif, "DATA")

# Process: Mosaic loss & gain
arcpy.MosaicToNewRaster_management("'%Workspace Folder%\\treecover_loss_1.tif';'%Workspace Folder%\\treecover_gain_50.tif'", Workspace_Folder, "treecover_gain_loss(aux).tif", "", "8_BIT_SIGNED", "", "1", "SUM", "FIRST")

# Process: Exclude loss & gain
arcpy.gp.Reclassify_sa(GFC_loss___gain, "Value", "1 0;50 50;51 NODATA", GFC_loss___gain_aux_tif, "DATA")

# Process: Mosaic To New Raster
arcpy.MosaicToNewRaster_management("'';'%Workspace Folder%\\treecover_loss_gain(aux2).tif'", Workspace_Folder, "treecover2012state(aux).tif", "", "8_BIT_SIGNED", "", "1", "LAST", "FIRST")

# Process: Reclassify <30 as NoData
arcpy.gp.Reclassify_sa(GFC_2012_aux1_tif, "Value", "0 29 NODATA;30 30;31 31;32 32;33 33;34 34;35 35;36 36;37 37;38 38;39 39;40 40;41 41;42 42;43 43;44 44;45 45;46 46;47 47;48 48;49 49;50 50;51 51;52 52;53 53;54 54;55 55;56 56;57 57;58 58;59 59;60 60;61 61;62 62;63 63;64 64;65 65;66 66;67 67;68 68;69 69;70 70;71 71;72 72;73 73;74 74;75 75;76 76;77 77;78 78;79 79;80 80;81 81;82 82;83 83;84 84;85 85;86 86;87 87;88 88;89 89;90 90;91 91;92 92;93 93;94 94;95 95;96 96;97 97;98 98;99 99;100 100", GFC_2012_aux2_tif, "DATA")

# Process: Project Raster
tempEnvironment0 = arcpy.env.snapRaster
arcpy.env.snapRaster = DEM 25m.tif
arcpy.ProjectRaster_management(GFC_2012_aux2_tif, GFC_2012_tif, PCS_in_UTM, "NEAREST", cell_size, "", "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.env.snapRaster = tempEnvironment0

# Process: Merge GFC 2012 GlobeLand30
arcpy.MosaicToNewRaster_management("'%Workspace Folder%\\GlobeLand30_restoDEM.tif';'%Workspace Folder%\\treecover2012_actual_Proj.tif'", Workspace_Folder, "Landcover(aux).tif", "", "8_BIT_SIGNED", "", "1", "MAXIMUM", "LAST")

# Process: Extract Water mask
arcpy.gp.ExtractByAttributes_sa(GLC30_aux_tif, "\"Value\"=25", Water_mask)

# Process: Mosaic To New Raster 
arcpy.MosaicToNewRaster_management("D:\\Downloads\\Output\\Landcover(aux).tif;'%Workspace Folder%\\Water_mask.tif'", Workspace_Folder, "LandCover.tif", "", "8_BIT_SIGNED", "", "1", "LAST", "FIRST")

# Process: Build Raster Attribute Table
arcpy.BuildRasterAttributeTable_management(LandCover_tif, "NONE")

# Process: Add Field LC_type
arcpy.AddField_management(LandCover_tif__ATable_, "LC_Type", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(LandCover_tif__Field_, "LC_Type", "{21: \"Cultivated land\", 22: \"Grassland\", 23: \"Schrubland\", 24: \"Wetland\", 25: \"Water bodies\", 26: \"Tundra\", 27: \"Artificial Surfaces\", 28: \"Bareland\", 29: \"Snow and ice\", 30: \"Forest cover 30%\", 31: \"Forest cover 31%\", 32: \"Forest cover 32%\", 33: \"Forest cover 33%\", 34: \"Forest cover 34%\", 35: \"Forest cover 35%\", 36: \"Forest cover 36%\", 37: \"Forest cover 37%\", 38: \"Forest cover 38%\", 39: \"Forest cover 39%\", 40: \"Forest cover 40%\", 41: \"Forest cover 41%\", 42: \"Forest cover 42%\", 43: \"Forest cover 43%\", 44: \"Forest cover 44%\", 45: \"Forest cover 45%\", 46: \"Forest cover 46%\", 47: \"Forest cover 47%\", 48: \"Forest cover 48%\", 49: \"Forest cover 49%\", 50: \"Forest cover 50%\", 51: \"Forest cover 51%\", 52: \"Forest cover 52%\", 53: \"Forest cover 53%\", 54: \"Forest cover 54%\", 55: \"Forest cover 55%\", 56: \"Forest cover 56%\", 57: \"Forest cover 57%\", 58: \"Forest cover 58%\", 59: \"Forest cover 59%\", 60: \"Forest cover 60%\", 61: \"Forest cover 61%\", 62: \"Forest cover 62%\", 63: \"Forest cover 63%\", 64: \"Forest cover 64%\", 65: \"Forest cover 65%\", 66: \"Forest cover 66%\", 67: \"Forest cover 67%\", 68: \"Forest cover 68%\", 69: \"Forest cover 69%\", 70: \"Forest cover 70%\", 71: \"Forest cover 71%\", 72: \"Forest cover 72%\", 73: \"Forest cover 73%\", 74: \"Forest cover 74%\", 75: \"Forest cover 75%\", 76: \"Forest cover 76%\", 77: \"Forest cover 77%\", 78: \"Forest cover 78%\", 79: \"Forest cover 79%\", 80: \"Forest cover 80%\", 81: \"Forest cover 81%\", 82: \"Forest cover 82%\", 83: \"Forest cover 83%\", 84: \"Forest cover 84%\", 85: \"Forest cover 85%\", 86: \"Forest cover 86%\", 87: \"Forest cover 87%\", 88: \"Forest cover 88%\", 89: \"Forest cover 89%\", 90: \"Forest cover 90%\", 91: \"Forest cover 91%\", 92: \"Forest cover 92%\", 93: \"Forest cover 93%\", 94: \"Forest cover 94%\", 95: \"Forest cover 95%\", 96: \"Forest cover 96%\", 97: \"Forest cover 97%\", 98: \"Forest cover 98%\", 99: \"Forest cover 99%\", 100: \"Forest cover 100%\"}.get(!Value!, !LC_Type!)", "PYTHON_9.3", "")

# Process: Clip
arcpy.Clip_management(LandCover_tif__write_Field_, "30,5308333333314 50,5200000000099 37,3741666666709 54,6433333333378", LandCover_clip_tif, Polygon_for_Clip, "-128", use_geometry, "NO_MAINTAIN_EXTENT")

# Process: Clip DEM
arcpy.Clip_management(DEM_25m_tif, "30,5308333333314 50,5200000000099 37,3741666666709 54,6433333333378", DEM_25m_clip_tif, Polygon_for_Clip, "32767", use_geometry, "NO_MAINTAIN_EXTENT")

