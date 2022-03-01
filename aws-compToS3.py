import sys
import subprocess

#must have Lacework CLI installed and configured with permissions to access account compliance reports
#must have AWS CLI installed and configure with permissions to write to S3 bucket
#pass aws_account and bucket on the command line
#example usage:   python3 aws-compToS3.py 12340983564 mybucketname


if (len(sys.argv) != 3):
    print("Both the Lacework CLI and AWS CLI must be installed and configured.\nAWS account number and S3 bucket name required.\nExample usage: python3 aws-compToS3.py 12312312331231 myS3bucketName")
    exit(0)

aws_account = sys.argv[1] 
bucketname = sys.argv[2] 

raw_cmd = "lacework compliance aws get-report " + aws_account + " --type SOC_Rev2 --pdf"
cmd = raw_cmd.split()

response = subprocess.run(cmd,shell=False,capture_output=True)
if response.returncode > 0:
  print("ERROR Response {}".format(response.stderr.decode('utf-8')))
  exit(response.returncode)
else:
  output = response.stdout.decode('utf-8').split("'")
  filename = output[1]
  raw_cmd = "aws s3 mv " + filename + " s3://" + bucketname
  cmd = raw_cmd.split()
  response = subprocess.run(cmd,shell=False,capture_output=True)
  if response.returncode > 0:
    print("ERROR Response {}".format(response.stderr.decode('utf-8')))
    exit(response.returncode)
  else:
    output = response.stdout.decode('utf-8')
    print(output)
