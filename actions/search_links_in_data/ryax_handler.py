import boto3
import json
from pathlib import Path

def connect_to_bucket(name: str, key: str, secret: str):
    s3 = boto3.resource("s3", aws_access_key_id=key, aws_secret_access_key=secret)
    return s3.Bucket(name)

def load_json(where: str)->dict:
    with open(where, "r") as f:
        return json.load(f)

def handle(inputs: dict)->dict:
    key = inputs["key"]
    secret = inputs["secret"]
    bucket_name = inputs["bucket"]
    bucket = connect_to_bucket(bucket_name, key, secret)

    objects_in_bucket = sorted(
            [obj.key for obj in bucket.objects.all()]
            )
    for obj in objects_in_bucket:
        download_loc = f"/tmp/{str(obj)}"
        bucket.download_file(obj, download_loc)
        json_object = load_json(download_loc)
        for linkname in json_object["links"]:
            if linkname not in [str(Path(o).stem) for o in objects_in_bucket]:
                print(f"Found new article to fetch with name: {linkname}")
                return {"pagereq": str(json.dumps(
                    {"page":linkname} ))}
    else:
        print("All links have been followed... We hit a dead end.")
    
