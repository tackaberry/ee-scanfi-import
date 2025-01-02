from dotenv import load_dotenv
from google.cloud import storage
import os
import json

load_dotenv()

BUCKET = os.getenv('BUCKET')
ASSET_FOLDER = os.getenv('ASSET_FOLDER')

PYRAMIDING_POLICY = os.getenv('PYRAMIDING_POLICY')
START_TIME = os.getenv('START_TIME')
END_TIME = os.getenv('END_TIME')

COLLECTION_NAME=os.getenv('COLLECTION_NAME')

storage_client = storage.Client()

source_tpl = '''
        {{
            "id": "{name}",
            "sources": [
                {{
                "uris": [
                    "{uri}"
                ]
                }}
        ]
        }}
'''

band_tpl = '''
    {{
      "id": "{name}",
      "tilesetBandIndex": 0,
      "tilesetId": "{name}"
    }}
'''

image_tpl = '''
{{
  "name": "{asset_folder}/{collection_name}_collection/{image_type}_{name}",
  "tilesets": [
    {{
      "id": "{name}",
      "sources": [
        {{
          "uris": [
            "{uri}"
          ]
        }}
      ]
    }}
  ],
  "pyramidingPolicy": "{pyramiding_policy}",
  "startTime": "{start_time}",
  "endTime": "{end_time}"
}}
'''


for image_type in ["sps","att"]:

    items = storage_client.list_blobs(bucket_or_name='tackaberry-scanfi')

    sources = []
    bands = []
    index=1

    for item in items:
        if item.name.startswith(COLLECTION_NAME+"_"+image_type):  
            uri = f"gs://{BUCKET}/{item.name}"
            name_parts = item.name.split("_")
            name = name_parts[2]
            sources.append(source_tpl.format(name=name, uri=uri))
            bands.append(band_tpl.format(name=name))
            index+=1

            image = image_tpl.format(name=name, uri=uri, asset_folder=ASSET_FOLDER, image_type=image_type, pyramiding_policy=PYRAMIDING_POLICY, start_time=START_TIME, end_time=END_TIME, collection_name=COLLECTION_NAME)
            filename = 'manifest-images-'+image_type+'-'+name+'.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json.loads(image), f, ensure_ascii=False, indent=4)
            print('earthengine upload image --manifest '+filename)


    out =   '''
    {{
        "name": "{asset_folder}/{collection_name}_{image_type}_image",
        "tilesets": [
            {sources}
        ],
        "bands": [
            {bands}
        ],
        "pyramidingPolicy": "MEAN",
        "startTime": "2023-01-31T00:00:00Z",
        "endTime": "2023-02-01T00:00:00Z"
    }}
    '''.format(sources=','.join(sources), bands=','.join(bands), asset_folder=ASSET_FOLDER, image_type=image_type, pyramiding_policy=PYRAMIDING_POLICY, start_time=START_TIME, end_time=END_TIME, collection_name=COLLECTION_NAME)

    filename = 'manifest-bands-'+image_type+'.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json.loads(out), f, ensure_ascii=False, indent=4)

    print('earthengine upload image --manifest '+filename)
