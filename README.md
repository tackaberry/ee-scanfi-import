# SCANFI Asset Importer for EarthEngine

This takes the files from the [ScanFI open data](https://ftp.maps.canada.ca/pub/nrcan_rncan/Forests_Foret/SCANFI/v1/), uploads to GCS and prepares manifest files for importing into Earth Engine. 

This prepares manifest files for 2 different approaches:
1. Create one collection and upload all images into one `ImageCollection`. 
2. Create one image for each SPS and ATT and upload each image as a separate band. 

### Getting Started

1. Set up python environment
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt

```

2. Set up `.env` file
```
BUCKET="bucket-name" 
BASE_URL="https://ftp.maps.canada.ca/pub/nrcan_rncan/Forests_Foret/SCANFI/v1/"
ASSET_FOLDER="projects/project-name/assets" # earthengine cloud asset folder

COLLECTION_NAME="SCANFI"

PYRAMIDING_POLICY="MEAN" # https://developers.google.com/earth-engine/reference/rest/Shared.Types/PyramidingPolicy
START_TIME="2023-01-31T00:00:00Z"
END_TIME="2023-02-01T00:00:00Z"

```

3. Create the collection

```bash
 earthengine create collection projects/project-name/assets/SCANFI_collection
```

4. Run each step in sequential order

```bash
chmod 755 1-download.sh
chmod 755 2-upload.sh

# get links from web page
python 0-readlinks.py

# download images locally and upload images to storage
./1-download.sh
./2-upload.sh

# create manifest files
python 3-manifest.py 
```

5. The `3-manifest.py` step prints earthengine commands

```
earthengine upload image --manifest manifest-images-sps-balsamFir.json
earthengine upload image --manifest manifest-images-sps-blackSpruce.json
earthengine upload image --manifest manifest-images-sps-douglasFir.json
earthengine upload image --manifest manifest-images-sps-jackPine.json
earthengine upload image --manifest manifest-images-sps-lodgepolePine.json
earthengine upload image --manifest manifest-images-sps-ponderosaPine.json
earthengine upload image --manifest manifest-images-sps-prcB.json
earthengine upload image --manifest manifest-images-sps-prcC.json
earthengine upload image --manifest manifest-images-sps-tamarack.json
earthengine upload image --manifest manifest-images-sps-whiteRedPine.json

earthengine upload image --manifest manifest-images-att-biomass.json
earthengine upload image --manifest manifest-images-att-closure.json
earthengine upload image --manifest manifest-images-att-height.json
earthengine upload image --manifest manifest-images-att-nfiLandCover.json

earthengine upload image --manifest manifest-bands-att.json
earthengine upload image --manifest manifest-bands-sps.json
```