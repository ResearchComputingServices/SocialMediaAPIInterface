# This bash script is used to test the 'curl' calls required to access data through the facebook API


####################################################################################################
curl -G   \
-d 'fields=name,evaluation_spec,execution_spec,status'   \
-d 'access_token=<ACCESS_TOKEN>'   \
https://graph.facebook.com/<VERSION>/<AD_ACCOUNT_ID>/adrules_library

####################################################################################################
curl -G   \
-d 'fields=name,evaluation_spec,execution_spec,status'   \
-d 'access_token=<ACCESS_TOKEN>'   \
https://graph.facebook.com/<VERSION>/<AD_RULE_ID>

####################################################################################################
curl \
-F 'evaluation_spec={
      "evaluation_type": ...,
      "trigger" : {
        "type": "STATS_MILESTONE",
        "field": "impressions",
        "value": 1000,
        "operator": "EQUAL"
      },
      "filters": ...
     ]
   }' \
-F 'access_token=<ACCESS_TOKEN>'   \
https://graph.facebook.com/<VERSION>/<AD_RULE_ID>

####################################################################################################
curl \
-F 'evaluation_spec={
      "evaluation_type": ...,
      "filters" : [
       {
         "field": "clicks",
         "value": 200,
         "operator": "GREATER_THAN",
       },
       {
       ...
     ]
   }' \
-F 'access_token=<ACCESS_TOKEN>'   \
https://graph.facebook.com/<VERSION>/<AD_RULE_ID>