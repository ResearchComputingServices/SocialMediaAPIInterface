# SocialMediaAPIInterface

A collection of Social Media API wrappers and a WebApp to interact with them

# Tool API Readmes

- [Notes about the Reddit API](Docs/RedditAPI.md)


# Sequence Diagrams: Running a Job with STATUS == RDY

:::mermaid
sequenceDiagram
    participant API
    participant JS as JobScheduler 
    participant TI as ToolInterface
    participant T as Tool
    
    activate API
    JS->>API: GET Jobs "all jobs with status == RDY"
    deactivate API
    activate JS
    API-->>JS: return a list of JOB_JSON objects
     
    JS->>TI: create a ToolInterface for each JOB_JSON in list   
    deactivate JS
    
    activate TI   

    TI->>API: GET Token "token_uid"
    API-->>TI: returns TOKEN_JSON with id *token_uid*
    TI->>API: PUT Jobs "job_uid JOB_JSON with Status = RUNNING"
    TI->>T: pass JOB_DICT to Tool
    deactivate TI   

    activate T
    T->>T: Run
    Note right of T: Make Requests and save data to location in JOB_DICT
    T-->TI: return STATUS, quota used, etc...    
    deactivate T

    activate TI  
    TI->>API: PUT Jobs "job_uid JOB_JSON with updated status"
    TI->>API: PUT Token "token_uid TOKEN_JSON with updated quota"
    deactivate TI  
:::

# Sequence Diagrams: Updating Quotas

:::mermaid
sequenceDiagram
    participant API
    participant JS as JobScheduler    
    JS->>API: GET Token "empty list"
    API-->>JS: list of TOKEN_JSON containing all rows in table

    Note right of JS: loop over all tokens and check if quota should be refreshed
    JS->>JS: 
    Note right of JS: for each TOKEN_JSON which was updated (quota_remaining and refresh_time)
    JS->>API: PUT Token "token_uid with updated TOKEN_JSON"   
:::


<!-- ============================================================================ -->

# JOB_JSON

Contains all fields in the row with primary key *job_uid* in the Jobs Table.

We are basically passing the entire 'page' describing a job so that we can update the required fields (STATUS)

## JOB_DICT

Contains all the data required to run the tool. Including the output path.

# TOKEN_JSON

Contains all fields in the row with primary key *token_uid*, in the Tokens Table.

<!-- ============================================================================ -->

# EndPoint: Job

## Operation: PUT 
Update the entire JOB_JSON data stored at {job_uid} with the one passed to the endpoint in the Request body.

### api call format
```
/api/v1/job/{job_uid}
```
### Request Body 
```json
{JOB_JSON}
```
### Response 
```json
NONE
```

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->

## Operation: GET 
Return a list of JOB_JSON objects which have a STATUS equal to the list of STATUS_TYPES passed in the Request body.

### api call format
```
/api/v1/job/
```
### Request Body 
```json
{"status" : [status1, status2,...]}
```
### Response 
```json
{"jobs": [JOB_JSON1, JOB_JSON2,...]}
```

<!-- ============================================================================ -->

# EndPoint: Token

## Operation: PUT 
Update the entire TOKEN_JSON data stored at {token_uid} with the one passed to the endpoint in the Request body. 

### api call format
```
/api/v1/token/{token_uid}
```

### Request Body 
```json
{TOKEN_JSON}
```

### Response 
```json
NONE
```

<!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->

## Operation: GET 
Return a list of TOKEN_JSON objects which have a PRIMARY KEY equal to the list of 
TOKEN_IDs passed in the Request body.

**NOTE:** if TOKEN_ID list is empty, return all the rows in the list

### api call format
```
/api/v1/token/
```

### Request Body 
```json
{token_ids: [id1,id2,...]}
```

### Response 
```json
{"tokens": [TOKEN_JSON_1, TOKEN_JSON_2,...]}
```

