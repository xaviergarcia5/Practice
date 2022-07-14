#!/usr/bin/env python

"""
Example igram processing chain - one process for each interferogram
Masking by coherence, masking by shapefile
Writing in GRD
Will only work on a properly configured machine, e.g. isceenv or pygmt environment with proper codes installed.
July 11, 2022
"""

import json, os, sys   # python core libraries
import numpy as np     # conda/pip code
from matplotlib.path import Path
import matplotlib.pyplot as plt
import shapefile      # pip code (pyshp)
from osgeo import osr   # gdal library
import Tectonic_Utils.read_write.netcdf_read_write          #  pip code (KZM)
import S1_batches.read_write_insar_utilities.isce_read_write as isce_reader   # KZM code
import S1_batches.math_tools.mask_and_interpolate as masking                 # KZM code


def read_config(config_filename):
    """
    Read configuration parameters into dictionary
    """
    if os.path.exists(config_filename):
        config_file = open(config_filename, 'r');
        igram_dictionary = json.load(config_file);
        config_file.close();
    else:
        print("File %s doesn't exist.  Exiting... " % config_filename);   # if user gives bad filename
        sys.exit();
    return igram_dictionary;


def read_data_files(binary_data_filename, cor_file, shapefile_filename):
    """
    Read files into computer memory
    """
    lonarray, latarray, unw = isce_reader.read_isce_unw_geo_single(binary_data_filename);
    cor = isce_reader.read_scalar_data(cor_file);  # cor = 2d_array
    if len(shapefile_filename) > 0:
        sf = shapefile.Reader(shapefile_filename);
        print("reading %d polygons from %s " % (len(sf), shapefile_filename));  # %d means integer, %s means string
    else:
        sf = ();
    return lonarray, latarray, unw, cor, sf;


def get_mask_polygon(lonarray, latarray, polygon_pts):
    """
    Create the mask from manual polygons.  Good pixels = 1.  Bad pixels = np.nan.
    """
    poly_path = Path(polygon_pts);
    x, y = np.meshgrid(lonarray, latarray);
    gridshape = np.shape(x);
    coords = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
    mask = poly_path.contains_points(coords)  # returns a bool
    mask = mask.reshape(gridshape)
    full_mask = np.ones(np.shape(mask));
    full_mask[np.where(mask)] = np.nan
    return full_mask;


def apply_two_masks(lonarray, latarray, unw, cor, sf):  # COMPUTE FUNCTION
    """
    Multiply the data array by coherence mask and by manual mask.
    Returning lons, lats, and masked data.
    """
    coherence_mask = masking.make_coherence_mask(cor, 0.37);   # coherence-based mask
    masked_data = masking.apply_coherence_mask(unw, coherence_mask, is_float32=True);

    # Converting between reference systems using GDAL with Python bindings
    src = osr.SpatialReference()
    tgt = osr.SpatialReference()
    src.ImportFromEPSG(3857)    # source: WGS84 Web Mercator Auxiliary Sphere
    tgt.ImportFromEPSG(4326)   # destination: WGS84 CGS
    transform = osr.CoordinateTransformation(src, tgt)

    for i in range(len(sf)):  # for each polygon
        shapepts = [];
        for point in sf.shape(i).points:  # for each vertex
            newtuple = transform.TransformPoint(point[0], point[1]);  # TRANSFORM
            shapepts.append((newtuple[1], newtuple[0]));
        mask = get_mask_polygon(lonarray, latarray, shapepts);    #  mask with 1 vs NP.NAN
        masked_data = np.multiply(masked_data, mask);

    return lonarray, latarray, masked_data;


def subtract_reference_pixel(masked_data, lonarray, latarray, reflon, reflat):
    """
    Find the pixel nearest to the chosen reference, and subtract it from the data array
    """
    row_idx = np.argmin(np.abs(np.array(latarray) - reflat));
    col_idx = np.argmin(np.abs(np.array(lonarray) - reflon));
    refvelocity = np.nanmean(masked_data[row_idx-10:row_idx+10, col_idx-10:col_idx+10]);  # area near ref pixel
    referenced_data = np.subtract(masked_data, refvelocity);
    return referenced_data;


def flip_array(latarray, masked_data):
    if latarray[1]-latarray[0] < 0:
        masked_data = np.flipud(masked_data);
        latarray = np.flipud(latarray);
    return latarray, masked_data;


if __name__ == "__main__":
    igram_dictionary = read_config(sys.argv[1]);    # CONFIGURE STAGE
    reflon, reflat = -115.428705, 33.247781;  # Choice: GNSS station P508
    for key in igram_dictionary.keys():
        output_filename = "intermediate/"+igram_dictionary[key]["direction"]+"/"+igram_dictionary[key]["filename"].split("/")[-2]+".grd"  # creating a filename like "intermediate/DESC/20210525_20210612.grd
        lonarray, latarray, unw, cor, sf = read_data_files(igram_dictionary[key]["filename"], igram_dictionary[key]["coh"], igram_dictionary[key]["shapefile"]);  # INPUT DATA
        lonarray, latarray, masked_data = apply_two_masks(lonarray, latarray, unw, cor, sf);   # COMPUTE: apply coherence and manual masks
        masked_data = subtract_reference_pixel(masked_data, lonarray, latarray, reflon, reflat);  # COMPUTE: remove reference pixel
        latarray, masked_data = flip_array(latarray, masked_data);
        Tectonic_Utils.read_write.netcdf_read_write.write_netcdf4(lonarray, latarray, masked_data, output_filename);   # WRITE OUTPUT
