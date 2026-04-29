import base64

import boto3

from app.config import get_settings

settings = get_settings()
R2_ACCOUNT_ID = settings["R2_ACCOUNT_ID"]
R2_ACCESS_KEY_ID = settings["R2_ACCESS_KEY_ID"]
R2_SECRET_ACCESS_KEY = settings["R2_SECRET_ACCESS_KEY"]
BUCKET = settings["R2_BUCKET"]

r2 = boto3.client(
    "s3",
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)


def upload_image(session_id: str, ts: str, action: str, img_b64: str) -> str:
    key = f"sessions/{session_id}/{ts}_{action}.png"
    data = base64.b64decode(img_b64)
    r2.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType="image/png")
    url = r2.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=3600,
    )
    return url


upload_object = upload_image
