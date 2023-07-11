##sign into SDK 
gcloud auth login

##get auth token
export AUTH_TOKEN=$(gcloud auth print-access-token)

##set instance name
export INSTANCE_ID=datafusion12
export REGION=us-central1

##get CDAP_ENDPOINT
export CDAP_ENDPOINT=$(gcloud beta data-fusion instances describe \
    --location=$REGION \
    --format="value(apiEndpoint)" \
  ${INSTANCE_ID})

echo $CDAP_ENDPOINT
https://anthonymm-private2-retail-data-specialists-dot-usc1.datafusion.googleusercontent.com/api

###api call
PUT /v3/namespaces/<namespace-id>/profiles/<profile-name>

## Get list of pipelines
curl -X PUT -H "Authorization: Bearer ${AUTH_TOKEN}" "${CDAP_ENDPOINT}/v3/namespaces/default/profiles/profile1" -d {"name":"profile1","label":"profile1","description":"asdkdjf;a","scope":"SYSTEM","status":"ENABLED","provisioner":{"name":"gcp-existing-dataproc","properties":[{"name":"clusterName","value":"cluster-ea10","isEditable":true},{"name":"region","value":"us-central1","isEditable":true},{"name":"accountKey","value":"","isEditable":true},{"name":"sshUser","value":"","isEditable":true},{"name":"sshKey","value":"","isEditable":true}]},"created":1642001064}



curl -X PUT -H "Authorization: Bearer ${AUTH_TOKEN}" "${CDAP_ENDPOINT}/v3/namespaces/default/profiles/profile2" -d @my-cluster.json


touch my-cluster1.json
{"name":"profile1","label":"profile1","description":"asdkdjf;a","scope":"SYSTEM","status":"ENABLED","provisioner":{"name":"gcp-existing-dataproc","properties":[{"name":"clusterName","value":"cluster-ea10","isEditable":true},{"name":"region","value":"us-central1","isEditable":true},{"name":"accountKey","value":"","isEditable":true},{"name":"sshUser","value":"","isEditable":true},{"name":"sshKey","value":"","isEditable":true}]},"created":1642001064}
curl -X PUT -H "Authorization: Bearer ${AUTH_TOKEN}" "${CDAP_ENDPOINT}/v3/namespaces/default/profiles/profile1" -d @my-cluster1.json


touch my-cluster2.json
{"name":"profile2","label":"profile2","description":"asdkdjf;a","scope":"SYSTEM","status":"ENABLED","provisioner":{"name":"gcp-existing-dataproc","properties":[{"name":"clusterName","value":"cluster-10eb","isEditable":true},{"name":"region","value":"us-central1","isEditable":true},{"name":"accountKey","value":"","isEditable":true},{"name":"sshUser","value":"","isEditable":true},{"name":"sshKey","value":"","isEditable":true}]},"created":1642001064}
curl -X PUT -H "Authorization: Bearer ${AUTH_TOKEN}" "${CDAP_ENDPOINT}/v3/namespaces/default/profiles/profile2" -d @my-cluster2.json
