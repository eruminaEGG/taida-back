#!/bin/bash

while getopts "a:b:s:" opt; do
  case $opt in
    a) AWS_ACCESS_KEY="$OPTARG";;
    b) AWS_SECRET_KEY="$OPTARG";;
    s) STAGE="$OPTARG";;
    *)
      echo "Usage: $0 -a <access_key> -b <secret_key> -s <stage>"
      exit 1
      ;;
  esac
done

if [ -z "$AWS_ACCESS_KEY" ] || [ -z "$AWS_SECRET_KEY" ] || [ -z "$STAGE" ]; then
  echo "Error: Missing required parameters."
  echo "Usage: $0 -a <access_key> -b <secret_key> -s <stage>"
  exit 1
fi

export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY"

#!/bin/bash

while getopts "a:b:s:" opt; do
  case $opt in
    a) AWS_ACCESS_KEY="$OPTARG";;
    b) AWS_SECRET_KEY="$OPTARG";;
    s) STAGE="$OPTARG";;
    *)
      echo "Usage: $0 -a <access_key> -b <secret_key> -s <stage>"
      exit 1
      ;;
  esac
done

if [ -z "$AWS_ACCESS_KEY" ] || [ -z "$AWS_SECRET_KEY" ] || [ -z "$STAGE" ]; then
  echo "Error: Missing required parameters."
  echo "Usage: $0 -a <access_key> -b <secret_key> -s <stage>"
  exit 1
fi

export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY"

npx serverless config credentials \
  --provider aws \
  --key ${AWS_ACCESS_KEY_ID} \
  --secret ${AWS_SECRET_ACCESS_KEY} \
  --profile "polaris-gai-${STAGE}" \
  --overwrite

serverless deploy --stage "$STAGE"

exit 0