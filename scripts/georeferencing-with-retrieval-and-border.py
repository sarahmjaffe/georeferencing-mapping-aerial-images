import os
from glob import glob
from osgeo import gdal, osr

import pyproj
from pyproj import Proj

import earthpy as et
import mosaic

# TESTING TO SEE IF REPO IS CONNECTED - WILL DELETE WHEN CHECKED!

# Answer these questions to run through the remainder of the notebook:
# What format are the images in: .jpg vs. .tif?
img_format = '.tif'

# What is the .csv name with images and centroid data?
# FOR TESTING: 'ElPaso_Batch1_YL_20180124_geometa.csv'
specified_df = 'Weld_20200430132018_DD.csv'

# What is the pixel size and width?
# Remember to use to use negative for second variable
pixel_size_estim = 0.950938
neg_pixel_size_estim = -0.950938

# Extract all images with .tif format
if __name__ == "__main__":

    # Set paths and import all images with specified format
    #img_input_path = glob(os.path.join('images', '*' + img_format))
    img_input_path = 'images'

    # Create/Set path for georeferenced images
    output_dir = os.path.join('outputs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Processing of individual image files starts here. Essentially we're going to iterate through
    # the list of items in the S3 bucket and process each image separately. We will also check that
    # the current image is also listed in the source CSV file. Here goes ...
    icat = mosaic.GeoMosaicImageCatalog(specified_df)
    gmb = mosaic.GeoMosaicBucket()
    for image in gmb.items:

        # First check to see if the image in the bucket is also listed in the data frame
        # If so, continue processing else log the item for future reference
        if icat.isin(image):

            # Download the image from S3
            mosaic.GeoMosaicObject(image, img_input_path)

            # Open the image to work on it
            print('Working on image {} ...'.format(image))
            src_ds = gdal.Open(os.path.join(img_input_path, image))

            # Describe the image size
            x_height = src_ds.RasterXSize
            y_width = src_ds.RasterYSize
            print('x_height = {0}, y_width = {1}'.format(x_height, y_width))

            # Grabbing image centroid coodinates from the data frame
            lon = icat.DDX(image)
            lat = icat.DDY(image)
            print('longitude = {0}, latitude = {1}'.format(lon, lat))

            # Reprojection
            myProj = Proj("+proj=utm +zone=13N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
            easting,northing = myProj(lon, lat)
            print('Centroid UTM coordinates: {0},{1}'.format(easting, northing))

            # Counting with pixels from center to top left corner
            top_img_pixel = x_height/2
            left_img_pixel = y_width/2

            # Calculating with coordinates from centroid to top left corner
            x_topleft = easting - (pixel_size_estim/2) - (pixel_size_estim * top_img_pixel)
            y_topleft = northing + (pixel_size_estim/2) + (pixel_size_estim * left_img_pixel)
            print('Top left UTM coordinates: {0},{1}\n\n'.format(x_topleft, y_topleft))

            # Reformatting the image to geotiff
            format = 'GTiff'
            driver = gdal.GetDriverByName(format)

            # Specify year image was taken
            year_details = icat.year(image)
            county_details = icat.county1(image)

            # Create copy with new name
            fn = '{0}-{1}-{2}{3}'.format(image[0:-4], year_details, county_details, img_format)
            dst_ds = driver.CreateCopy(os.path.join(output_dir, fn), src_ds, 0)

            # Set top left corner coordinates in UTM with pixel size and rotation
            gt = [x_topleft, pixel_size_estim, 0, y_topleft, 0, neg_pixel_size_estim]
            dst_ds.SetGeoTransform(gt)

            # Assign CRS
            epsg = 32613 #utm zone 13n
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(epsg)
            dst_wkt = srs.ExportToWkt()
            dst_ds.SetProjection(dst_wkt)

            # Close and finalize dst_ds
            dst_ds = None
            src_ds = None

            # Clean up the images directory
            os.remove(os.path.join(img_input_path, image))

            # DEBUG -- comment out this line for production run
            # break

        else:

            # Log the missing items
            with open('missing-from-csv.txt', 'a') as log:
                log.write('{}\n'.format(image))
