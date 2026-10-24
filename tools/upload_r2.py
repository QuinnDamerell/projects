#!/usr/bin/env python3
"""Uploads a file to the Cloudflare R2 bucket behind projects-storage.quinn.space.

The R2 dashboard only accepts uploads up to 300 MB, so larger files, such as long videos,
go through R2's S3-compatible API instead. Big files are split into parts and uploaded in
parallel. The object keeps the file's name.

    pip install boto3
    python tools/upload_r2.py <file> <api-token>

<api-token> is an R2 API token value (R2 > Manage API tokens) with Object Read & Write
access to the bucket. R2 derives its S3 credentials from the token: the access key ID is
the token's ID and the secret is the SHA-256 hash of its value. If you'd rather paste the
S3 credentials the dashboard shows, pass the secret as <api-token> and add
--access-key-id <id>.

Set ACCOUNT_ID and BUCKET below once, or pass --account-id and --bucket.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

ACCOUNT_ID = ""  # Cloudflare dashboard > R2 > Overview, "Account ID"
BUCKET = ""  # the bucket bound to projects-storage.quinn.space
PUBLIC_URL = "https://projects-storage.quinn.space"

# Windows doesn't always know these, and the type decides whether browsers play the file inline.
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("audio/mpeg", ".mp3")


def token_id(token, account_id):
    """Looks up an API token's ID, which R2 uses as the S3 access key ID."""
    endpoints = [
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/tokens/verify",  # account-owned tokens
        "https://api.cloudflare.com/client/v4/user/tokens/verify",  # user-owned tokens
    ]
    for endpoint in endpoints:
        request = urllib.request.Request(endpoint, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)["result"]["id"]
        except urllib.error.HTTPError:
            continue
    sys.exit("Cloudflare didn't accept that API token. Check that it's the token value and that it hasn't expired.")


class Progress:
    def __init__(self, size):
        self.size, self.sent, self.lock = size, 0, threading.Lock()

    def __call__(self, count):
        with self.lock:
            self.sent += count
            print(f"\r  {self.sent / 1e6:,.0f} of {self.size / 1e6:,.0f} MB ({self.sent / self.size:.0%})", end="", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Upload a file to Cloudflare R2, keeping its file name.")
    parser.add_argument("file", help="path to the file to upload")
    parser.add_argument("api_key", help="R2 API token value, or the S3 secret access key with --access-key-id")
    parser.add_argument("--access-key-id", help="S3 access key ID; makes api_key the S3 secret access key")
    parser.add_argument("--account-id", default=os.environ.get("R2_ACCOUNT_ID", ACCOUNT_ID))
    parser.add_argument("--bucket", default=os.environ.get("R2_BUCKET", BUCKET))
    parser.add_argument("--overwrite", action="store_true", help="replace an existing file with the same name")
    args = parser.parse_args()

    if not args.account_id or not args.bucket:
        sys.exit("Set ACCOUNT_ID and BUCKET at the top of this script, or pass --account-id and --bucket.")
    if not os.path.isfile(args.file):
        sys.exit(f"File not found: {args.file}")

    try:
        import boto3
        from boto3.s3.transfer import TransferConfig
        from botocore.config import Config
        from botocore.exceptions import BotoCoreError, ClientError
    except ImportError:
        sys.exit("This script needs boto3: pip install boto3")

    if args.access_key_id:
        access_key_id, secret = args.access_key_id, args.api_key
    else:
        access_key_id, secret = token_id(args.api_key, args.account_id), hashlib.sha256(args.api_key.encode()).hexdigest()

    # Newer boto3 versions add checksum headers by default; only send them when required.
    try:
        config = Config(region_name="auto", request_checksum_calculation="when_required", response_checksum_validation="when_required")
    except TypeError:
        config = Config(region_name="auto")
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{args.account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret,
        config=config,
    )

    name = os.path.basename(args.file)
    size = os.path.getsize(args.file)
    if not args.overwrite:
        try:
            s3.head_object(Bucket=args.bucket, Key=name)
            sys.exit(f'"{name}" is already in the bucket. Pass --overwrite to replace it.')
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
                sys.exit(f"Couldn't reach the bucket: {error}")
        except BotoCoreError as error:
            sys.exit(f"Couldn't connect to R2; check the account ID. ({error})")

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    print(f'Uploading "{name}" ({size / 1e6:,.0f} MB, {content_type}) to {args.bucket}')
    s3.upload_file(
        args.file, args.bucket, name,
        ExtraArgs={"ContentType": content_type},
        Config=TransferConfig(multipart_threshold=64 * 1024 * 1024, multipart_chunksize=64 * 1024 * 1024, max_concurrency=8),
        Callback=Progress(size),
    )
    print(f"\nDone: {PUBLIC_URL}/{urllib.parse.quote(name)}")


if __name__ == "__main__":
    main()
