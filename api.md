# Impacto API

## Login

**POST** to `/api/login/` with username or email and password.
Example requests:
```
{"username": "sampleuser", "password": "samplepassword"}
```
OR
```
{"email": "sampleemail@example.com", "password": "samplepassword"}
```

Returns user access token that must be provided as a GET parameter in the other requests.
Example response:
```
{"access_token": "Sample-Access-Token"}
```

## Impact Objects

URLs:

- List objects: `/api/impacts`
- Object details: `/api/impact/<impact_id>`


### Impact object specification

Field | Read/Write | Description
----- | ---------- | ----------
id | read | Unique identifier of the Impact object.
date | read/write | Date the impact was generated.
description | read/write | Description of the impact.
geo | read/write | Location of the Impact. format: `{"lat": <lat>, "lng": <lng>, "address": <optional_address>}`
public | read/write | Flags if the Impact is public or not.
recorded_by | read/write | Person who recorded the record in the system.
story | read | Story associated to the impact. format: `{"id": story_id>, "title": <story_title>, "url": <story_url>}`
story_id | write | ID of story to associate with Impact.
tags | read/write | Tags of the impact. format: `["tag1", "tag2", ...]`
updated_at | read/write | Moment that the tag was updated.
uploaded_file | read/write | File that proves Impact.
source | read/write | Source of the impact. Choices: `1` - Typeform, `2` - Insight, `3` - Form, `4` - API. Defaults to `4`.
repercussion | read | Repercussions of the impact based on impact links. Format: `{"url": <url>, "favicon": <favicon>, "domain": <domain>}`
links | write | List of links that prove the Impact. Format: ["url_1", "url_2"]


### Actions

action | method | url | description
------ | ------ | --- | -----------
create | POST | `/api/impacts/` | Requires links or uploaded_file that prove the Impact.
list | GET | `/api/impacts/` | Lists all impacts for the partner that the user belongs to.
update | PUT | `/api/impact/<id>/` | Generally updates an impact with the `<id>` present in the url. Used to update all fields. If any field is not present, it will be set to `None`.
partial_update | PATCH | `/api/impact/<id>/` | Updates the impact only on the fields sent in the request.


## Insight Objects

URL:

- List objects: `/api/insights`

Available filters:

- `type`: one of the possible insight types, like `influencers`, `politics` and
  `media`;
- `date`: filter by exact date. Format: `YYYY-MM-DD`;
- `date_min`: filter by minimum date (inclusive). Format: `YYYY-MM-DD`;
- `date_max`: filter by maximum date (inclusive). Format: `YYYY-MM-DD`;
- `story_id`: filter by story id;
- `story_url`: filter by story URL;


## Story Objects

URLs:

- List objects: `/api/stories` (show summary information);
- Specific object: `/api/story/<story_id>` (show detailed information, like
  story statistics).
