# Gitlab Events

This folder contains samples for every gitlab event sent to the webhook app in json format.

Reference: https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#events

All messages will use the following topic schema: `org.centos.$ENV.gitlab.$ORG_NAME.$REPO_NAME.$KIND` where:

* `$ENV`: indicates the topic/mq env, either "prod" or "stg";
* `$ORG_NAME`: The repository organization name, such as `centos`;
* `$REPO_NAME`: The repository name which the event was triggered;
* `$KIND`: the gitlab object kind such as `issue`, `push`, etc; those can be found in the sample json files.

## Events

All events will send its event name in a HTTP header `X-Gitlab-Event` which will be included in the messaging body.

### Push

**Name:** `Push Hook`

**File:** [push.json](./push.json)

**Notes:** Will limit itself to the last 20 commits for performance reasons.

### Tag

**Name:** `Tag Push Hook`

**File:** [tag.json](./tag.json)

**Notes:** Triggered by tag changes, either creation or deletion.

### Tag

**Name:** `Issue Hook`

**File:** [issue.json](./issue.json)

**Notes:** Triggered by issue changes (creation, modification or deletion).

### Comments

Triggered when a comment is added, it can be added in the following objects:

* commit
* merge request
* issue
* code snippet

The hook body will contain specific data for each object.

#### Commit

**Name:** `Note Hook`

**File:** [comment_commit.json](./comment_commit.json)

**Notes:** Triggered when a comment is added in a push commit.

#### Merge Request

**Name:** `Note Hook`

**File:** [comment_commit.json](./comment_merge_request.json)

**Notes:** Triggered when a comment is added in a merge request.

#### Issue

**Name:** `Note Hook`

**File:** [comment_issue.json](./comment_issue.json)

**Notes:** Triggered when a comment is added in an issue.

#### Code Snippet

**Name:** `Note Hook`

**File:** [comment_snippet.json](./comment_snippet.json)

**Notes:** Triggered when a comment is added in a code snippet.

### Merge Request

**Name:** `Merge Request Hook`

**File:** [merge_request.json](./merge_request.json)

**Notes:** Triggered when a merge request is created or updated, including if new commits were added to it.

### Wiki Pages

**Name:** `Wiki Page Hook`

**File:** [wiki_page.json](./wiki_page.json)

**Notes:** Triggered when a wiki page is created, modified or deleted.

### Pipeline

**Name:** `Pipeline Hook`

**File:** [pipeline.json](./pipeline.json)

**Notes:** Triggered whenever there are changes in a pipeline status.

### Job

**Name:** `Job Hook`

**File:** [job.json](./job.json)

**Notes:** Triggered when there is a change in a job status.

### Deployment

**Name:** `Deployment Hook`

**File:** [deployment.json](./deployment.json)

**Notes:** Triggered by a deployment status change (gitlab CD).

### Feature Flag

**Name:** `Feature Flag Hook`

**File:** [feature_flag.json](./feature_flag.json)

**Notes:** Triggered when a feature flag is turned on or off.

### Release

**Name:** `Release Hook`

**File:** [release.json](./release.json)

**Notes:** Triggered whenever a release is created or updated.