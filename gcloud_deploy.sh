#!/usr/bin/bash

gcloud run deploy mirai \
	--region asia-northeast1 \
	--source . \
	--base-image python312
