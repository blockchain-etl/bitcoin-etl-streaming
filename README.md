# Bitcoin ETL Streaming

Streams blocks and transactions to a Pub/Sub topic.

1. Create a cluster:

```bash
gcloud container clusters create bitcoin-etl-streaming \
--zone us-central1-a \
--num-nodes 1 \
--disk-size 10GB \
--machine-type custom-2-4096 \
--scopes pubsub,storage-rw,logging-write,monitoring-write,service-management,service-control,trace
```

2. Get `kubectl` credentials:

```bash
gcloud container clusters get-credentials bitcoin-etl-streaming \
--zone us-central1-a
```

3. Create Pub/Sub topics "crypto_bitcoin.blocks" and "crypto_bitcoin.transactions". 
Put it to `overlays/bitcoin/configMap.yaml`, `PUB_SUB_TOPIC_PREFIX` property.

4. Create GCS bucket. Upload a text file with block number you want to start streaming from to 
`gs:/<your-bucket>/bitcoin-etl/streaming/last_synced_block.txt`.
Put your bucket name to `base/configMap.yaml`, `GCS_BUCKET` property.

5. Update `overlays/bitcoin/configMap.yaml`, `PROVIDER_URI` property to point to your Bitcoin node.

5. Create "bitcoin-etl-app" service account with roles:
    - Pub/Sub Editor
    - Storage Object Creator

Download the key. Create a Kubernetes secret:

```bash
kubectl create secret generic bitcoin-etl-app-key --from-file=key.json=$HOME/Downloads/key.json
```

6. Install kustomize https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md. 

```bash
brew install kustomize
```

Create the application:

```bash
kustomize build overlays/bitcoin | kubectl apply -f -
```

7. To troubleshoot:

```bash
kubectl describe pods
kubectl describe node [NODE_NAME]
```