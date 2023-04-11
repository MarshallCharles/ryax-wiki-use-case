import json
import boto3
from pathlib import Path


def write_json(obj: dict, where: str) -> None:
    with open(where, "w") as f:
        json.dump(obj, f)

def load_json(where: str)->dict:
    with open(where, "r") as f:
        return json.load(f)

def connect_to_bucket(name: str, access_key: str, secret_key: str):
    s3 = boto3.resource(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    return s3.Bucket(name)


def handle(req: dict) -> dict:
    access_key: str = req.get("key_id")
    secret_key: str = req.get("secret_key_id")
    bucket_name: str = req.get("bucket_name")

    my_bucket = connect_to_bucket(bucket_name, access_key, secret_key)
    objects_to_list = sorted([obj.key for obj in my_bucket.objects.all()])
    for obj in objects_to_list:
        download_loc = f"/tmp/{str(obj)}"
        my_bucket.download_file(obj, download_loc)
        obj_contents = load_json(download_loc)
        for linkname in obj_contents["links"]:
            if linkname not in [str(Path(o).stem) for o in objects_to_list]:
                print(f"Sending request for {linkname}")
                return {"pagereq": str(json.dumps({"page": linkname}))}
    else:
        print("All links in all bucket items are already accounted for!")



