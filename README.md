# SCANFI Asset Importer for EarthEngine

This takes the files from the [ScanFI open data](https://ftp.maps.canada.ca/pub/nrcan_rncan/Forests_Foret/SCANFI/v1/), uploads to GCS and prepares  

### Getting Started

Set up python environment

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt

```


```bash
 earthengine create collection projects/tackaberry-ee-project-1/assets/SCANFI_collection
```