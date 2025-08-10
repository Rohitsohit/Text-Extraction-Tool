# textract_pdf_async.py
import boto3, time

REGION      = "us-east-2"        # change if needed
BUCKET      = "extract-tool" # <-- put your bucket
LOCAL_PDF   = "/Users/rohithooda/Documents/Text Extraction Tool/A$AP Mob - Bahamas.pdf"       # local pdf path
S3_KEY      = "tmp/sample.pdf"   # where to upload in S3

def extract_pdf_text(local_path, bucket, key):
    s3 = boto3.client("s3", region_name=REGION)
    tex = boto3.client("textract", region_name=REGION)

    # 1) upload to S3
    s3.upload_file(local_path, bucket, key)

    # 2) start async text detection
    job = tex.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    job_id = job["JobId"]

    # 3) poll until done
    while True:
        resp = tex.get_document_text_detection(JobId=job_id, MaxResults=1000)
        status = resp["JobStatus"]
        if status in ("SUCCEEDED", "FAILED", "PARTIAL_SUCCESS"):
            break
        time.sleep(2)

    if status != "SUCCEEDED":
        raise RuntimeError(f"Textract job ended with status: {status}")

    # 4) collect all pages using NextToken
    blocks = resp["Blocks"]
    next_token = resp.get("NextToken")
    while next_token:
        resp = tex.get_document_text_detection(JobId=job_id, MaxResults=1000, NextToken=next_token)
        blocks.extend(resp["Blocks"])
        next_token = resp.get("NextToken")

    # 5) return LINE text joined
    lines = [b["Text"] for b in blocks if b["BlockType"] == "LINE"]
    return "\n".join(lines).strip()

if __name__ == "__main__":
    text = extract_pdf_text(LOCAL_PDF, BUCKET, S3_KEY)
    print(text or "[No text detected]")