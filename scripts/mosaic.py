import boto3
import pandas as pd
import os

BUCKET = 'cubl-research-geo'

class GeoMosaicObject:
    """
    Represents a single aerial photo in S3.
    
    The individual aerial photographs that comprise a completed mosaic image
    are stored in an S3 bucket. This class exposes properties and methods
    to enable manipulation of an individual photo during the creation of the
    mosaic image.
    """

    def __init__(self, source, target):
        """
        Given a source file and target directory, instantiation of the
        class performs all the actions needed to download the file to
        a local working directory.
        """
        
        self._source = source
        self._target = target
        self._get_object(source, target)

    def _get_object(self, source, target):
        """
        Downloads the source image file from S3 to a local working directory.
        """
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET)
        obj = bucket.Object(source)
        with open('{0}/{1}'.format(target, source), 'wb') as data:
            obj.download_fileobj(data)

class GeoMosaicBucket:
    """
    Represents the S3 bucket containing the individual aerial photos.

    This class is basicaly establishes an iterator that facilitates
    the processing of the individual images contained in the bucket.
    """

    def __init__(self):
        self._bucket = BUCKET
        self._object_list = self._get_object_list()

    def _get_object_list(self):
        """
        Returns a list of all objects in the bucket.
        """

        object_list = list()
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self._bucket)
        for objsum in bucket.objects.all():
            object_list.append(objsum.key)
        return object_list

    @property
    def items(self):
        return self._object_list

class GeoMosaicImageCatalog:
    """
    This class represents the source CSV file containing the image details.
    Note that this approach can be extended further by defining a class that represents
    the image itself with the corresponding metadata details. For future
    consideration.
    """

    def __init__(self, source):
        self._centroid_df = pd.read_csv(source)
        self._centroid_df.lnexp_MEDIAFILENAME = self._centroid_df.lnexp_MEDIAFILENAME.replace({'.jpg':'.tif'}, regex=True)

    def isin(self, image):
        """
        Returns true if image file is present in the source csv.
        """

        result = self._centroid_df.isin({'lnexp_MEDIAFILENAME':[image]})
        return result.any()['lnexp_MEDIAFILENAME']

    def indexof(self, image):
        """
        Returns the dataframe index corresponding to the given image.
        """

        result = self._centroid_df.isin({'lnexp_MEDIAFILENAME':[image]})
        return result['lnexp_MEDIAFILENAME'][result['lnexp_MEDIAFILENAME'] == True].index[0]

    def DDX(self, image):
        """
        Returns the DDX value for the image.
        """
        
        return  self._centroid_df['DDX'][self.indexof(image)]

    def DDY(self, image):
        """
        Returns the DDY for the image.
        """

        return self._centroid_df['DDY'][self.indexof(image)]

    def year(self, image):
        """
        Returns the year the image was taken.
        """

        return self._centroid_df['Date'][self.indexof(image)][5:]

    def county1(self, image):
        """
        Returns the name of the county where the image was taken.
        """
        
        return self._centroid_df['County#1'][self.indexof(image)]
