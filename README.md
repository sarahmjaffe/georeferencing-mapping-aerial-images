# georeferencing-mapping-aerial-images
This repository will contain python code that automates the georeferencing of any image that has a latitude and longitude associated with it and will walk through the processes of presenting 1,000's of images in mapbox.

In order to run the notebooks

## Setting up your work station
### 1. Installations and Downloads
#### Install Git, Bash and Miniconda
Depending on your operating system, you will need to follow different instructions installing each of these on your computer.  A wonderful source with step-by-step instructions for all operating systems can be found at the <a href='https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-git-bash-conda/'>Earth Data Analytics</a> website.  You can find many tutorials here, too!

#### Cloning or Downloading the Georeferencing-mapping-aerial-images respository contents
There are two ways you can copy the entire contents of this repository illustrated, first, then described below.

<img src="direction-images\\clone-download-modified.JPG" alt="Illustration of how to copy repository">

a.  If you are familiar with Git, cloning is the way to go:
i) Above this README, you will see the green 'Code' button illustrated.  Press the folder icon.

ii) Then, in your terminal, direct the terminal screen to the place you want to save this repository.  You can do this by typing `cd` and then the path leading to the place you want this folder to exist.

iii) It is possible your default location in the terminal is exactly where you want this repository to be.  To see where your default location is, type `pwd` (which stands for present working directory).  To move forward in your path, simply type

`cd path/to/folder/of/interest`

If you want to move back up through the directory, essentially going backward, type `cd ..`.  You can move one folder at a time, or using the `/` to move through several steps.  Try playing with this, continually typing `pwd` to see where you got.  If you get lost and want to start over, simply type `exit`.  This will close your terminal and you can start again.

iv) Once in the location you want to save this repository, type `git clone`, followed by a space and paste the repository you copied by pressing the folder icon.  If you go to your explorer, you will then see the repository in the location you directed it to.

b.  If you are not familiar with Git:
While I recommend the instructions above, you can also download a zipped folder of this repository's contents.  Simply click the green 'Code' button at the top of this README and illustrated above and then press 'Download ZIP'.  Next, in your explorer, past this folder where you want it, making sure you are aware of how to access the path of wherever you decide to store this zipped file.

Then, unzip the file.  <a href='https://www.7-zip.org/download.html'>7-Zip</a> is a free version of <a href='https://www.winzip.com/win/en/'>WinZip</a>, but either will do the job.

The last thing to do in this step is open your terminal and find this folder in the terminal.  Follow step iii above.

#### Installing the environment.yml
Installing the environment.yml is easy, but know that it is 3.5GB.  It will install all of the packages you need to run the code in this repository.  If you want to pick and choose the packages you need, open the environment.yml to see what all you will need and feel free to install these things individually.  Otherwise, follow the instructions below.

To install the entire environment.yml file, go back to your terminal and navigate to the location where the environment.yml file exists.  If your terminal is still open from the steps above, you will then navigate to

`cd Georeferencing-mapping-aerial-images`

When you type `ls` (list) after navigating to this folder, you should see the environment.yml file.

To create the environment in any workflow, type

`conda env create -f environment.yml`

Note, you will only need to do this once!  After the you create this environment, you will be able to activate it no matter where in the terminal you are.  To activate the environment, type

`conda activate auto-georef-project`

This is the name given to the environment as seen when you open the .yml file in a word processor.  You should then see the environment name preceeding any line of code in your terminal.

<img src="direction-images\\activated-environment.JPG" alt="What you should see in your terminal after the environment is activated">

#### Now that your work station is completed...
Your workstation is now ready to go!  That means that when you are ready to work in the `Georeferencing-mapping-aerial-images` folder again,

i) open your terminal
ii) navigate to the folder
iii) activate your environment (`conda activate auto-georef-project`)
iv) type `jupyter notebook` (we will talk about this later)

### 2. Required items: Images and Center Points Metadata
#### Images
RETURN TO

#### Metadata
RETURN TO

## Workflow
The following reflects the workflow being used to georeference a single image:
- Import packages (import-packages.py)
- Download the data (via figshare or some other way)
- Set the paths to your directories: working directory, pre-processed images, post-processed images
- Import your source image(s): src_ds = gdal.Open(....)
- Define image(s) height and width as well as locate where the top and left pixel (pixel-count-location-top-and-left.py)
- Define lon (longitude) and lat (latitude) centroid of the image(s)
- Project the .jpg or .tif using datum WGS84 and projection UTM zone 13N (project-image.py)
- Define the pixel sizes in two ways: pixel_size_estim (positive number) and neg_pixel_size_estim (negative number)
- Based on the number of pixels and coordinates, calculate the top-left corner coordinates (assign-top-left-coordinate.py)
- Wanting to create a GeoTIFF, define the driver
- Create a copy of the unformatted image
- Open the driver, complete the process of georeferencing (georeference.py) and close the driver

## If using Linux....
To run in aws.amazon.com/amazon-linux-ami with python3 already set-up, you must install necessary packages first:
1) sudo yum install `python-numpy` `gdal-bin` `libgdal-dev`
2) pip install `rasterio`
3) pip install `pyproj`
