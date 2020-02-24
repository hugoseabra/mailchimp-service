# MailChimp Service

If you have an application and there is a need to synchronize people's record
in the application to MailChimp Platform to run your campaigns, this project
can be used to make the process easier.

## How it works

In MailChimp we have **Audience Lists** where we subscribe a **contact** as a
**Member** of the **List**. When add a **Member**, some complexities must be
watched:  

* How can we keep tracking of the person's data if the data is edited in your
platform?
* How can we add custom fields to a list when there is more than one source of
data submitting to one **Audience List**?
* How can we handle the correct tags? Will they change?
* How can we *Unsubcribe* a person's record according to one application's
rules?

Well, we started a solution to all these questions by adding an application
service layer between the applications and MailChimp Service. We can have some
benefits with this service:

1. We added a **Namespace** dedicated to an **Audience List** in MailChimp,
and it handles all the configuration to synchronize related members to it;
1. We added support to let the client application decide which data will be
sychronized in the Contact of an **Audience List**;
1. We added support to create as many custom fields as needed by the client
application, so, it is possible to add **Members** to the **List** with the
support to contextualize anything you need - **Origin** for example;
1. We added support to synchronization a person's data as **Member** in
MailChimp **Audience List**. To do that, it needed to submit a person's record
as **Member** related to the **Namespace**. After doing it, you do not have to
worry about anything else. Just check out the contact in MailChimp's
**Audience List** successfully.

# Architecture

## Namespace

Namespace is a place where we handle the important information of the
integration with MailChimp Platform, such as, **api key**, **audience list id**
and synchronization configuration to be processed when the **Members** are
send to MailChimp.

Below we have keys to show how it is done:

* **Name:** My namespace Name to identify the origin
* **API KEY:** My namespace Name to identify the origin
* **Default List ID:** ID of the **Audience List** in MailChimp
* **External ID:** Any external ID used by origin
* **Create Fields:** If custom fields will be created in MailChimp
* **Synchronize Phone:** If members will have their phone number sent to MailChimp 
* **Synchronize Address:** If members will have their address number sent to MailChimp

## List Field

To help to contextualize the contact data in MailChimp, it is possible to add
**Custom Fields** related to the **Namespace**. After that, every **Member**
will support to record values to these fields.

Below we have keys to show how it is done:

* **Label:** the name of the field;
* **tag:** unique tag to identifiy the field in MailChimp;
* **Type:** we support only *text* and *number* fields for a while;
* **Help Text:** how we offer a better understanding of the reason the field exists;

# How to use this project

We used *Django Framework* to build the application. It is possible to deploy
it conventionally or using *Docker*.

*WE WILL ADD THE DOCUMENTATION FOR USAGE - Installation and deploy*
*WE WILL ADD THE DOCUMENTATION FOR DOCKER USAGE - Installation and deploy*

## Usage

After the project deployed, we'll have the following REST endponts:

#### Namespace

```text
GET /v1/namespaces
```
Retrieve all namespaces.

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Name",
            "slug": "slug-of-the-namespace",
            "api_key": "xxxxxx-us4",
            "external_id": "1922",
            "default_tag": "TAG-FROM-ORIGIN",
            "default_list_id": "1121231",
            "default_list_name": "My List",
            "sync_phone": true,
            "sync_address": true,
            "create_fields": true,
            "healthy": true,
            "created_at": "2020-02-20T19:28:41-0300",
            "updated_at": "2020-02-22T21:33:26-0300"
        }
    ]
}
```

- ---

```text
GET /v1/namespaces/:pk
PUT /v1/namespaces/:pk
PATCH /v1/namespaces/:pk
DELETE /v1/namespaces/:pk
```

Retrieve one namespace, or edit it, or delete.


**Request:**
```json
{
    "name": "Name",
    "slug": "slug-of-the-namespace",
    "api_key": "xxxxxx-us4",
    "external_id": "1922",
    "default_list_id": "1121231",
    "sync_phone": true,
    "sync_address": true,
    "create_fields": true
}
```

**Response:**
```json
{
    "name": "Name",
    "slug": "slug-of-the-namespace",
    "api_key": "xxxxxx-us4",
    "external_id": "1922",
    "default_tag": "TAG-FROM-ORIGIN",
    "default_list_id": "1121231",
    "default_list_name": "My List",
    "sync_phone": true,
    "sync_address": true,
    "create_fields": true,
    "create_notes": true,
    "healthy": true,
    "created_at": "2020-02-20T19:28:41-0300",
    "updated_at": "2020-02-22T21:33:26-0300"
}
```
- ---

#### Audience List

```text
GET /v1/namespaces/:namespace_pk/lists
```
Directly from MailChimp:

**Response:**

```json
{
    "count": 1,
    "results": [
        {
            "id": "4136c2c1c6",
            "web_id": 375291,
            "name": "Congressy"
        }
    ]
}
```

- ---

#### Custom Field

```text
GET /v1/namespaces/:namespace_pk/fields/
```
Retrieve all fields of a namespace.

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": "489206ab-9ee8-4b9c-bb58-c6cd66b7f5e4",
            "label": "My custom field",
            "tag": "MYCUSTOMFIELD1",
            "field_type": "text",
            "help_text": "Use it as you wish",
            "active": true,
            "created_at": "2020-02-22T19:33:45-0300",
            "updated_at": "2020-02-22T21:18:05-0300",
            "namespace": {
                "pk": "91a0a247-7dd5-4888-8d5a-bc3b0adaa347",
                "name": "Name",
                "slug": "slug-of-the-namespace",
                "default_tag": "TAG-FROM-ORIGIN",
                "default_list_id": "1121231",
                "default_list_name": "My List",
                "sync_phone": true,
                "sync_address": true,
                "create_fields": true
            }
        }
    ]   
}
```

- ---

```text
GET /v1/namespaces/:namespace_pk/fields/:pk
PUT /v1/namespaces/:namespace_pk/fields/:pk
PATCH /v1/namespaces/:namespace_pk/fields/:pk
DELETE /v1/namespaces/:namespace_pk/fields/:pk
```

Create a field, or edit or delete it.

**Request:**
```json
{
    "label": "My Custom Field 2",
    "tag": "CUSTOMFIELD2",
    "field_type": "number",
    "help_text": "Tell you age",
    "active": true
}
```

**Response:**
```json
{
    "pk": "e50316f4-5d45-4b86-9387-539d7f4bb1a8",
    "label": "My custom field 2",
    "tag": "MYCUSTOMFIELD2",
    "field_type": "number",
    "help_text": "Tell you age",
    "active": true,
    "created_at": "2020-02-22T19:33:45-0300",
    "updated_at": "2020-02-22T21:18:05-0300",
    "namespace": {
        "pk": "91a0a247-7dd5-4888-8d5a-bc3b0adaa347",
        "name": "Name",
        "slug": "slug-of-the-namespace",
        "default_tag": "TAG-FROM-ORIGIN",
        "default_list_id": "1121231",
        "default_list_name": "My List",
        "sync_phone": true,
        "sync_address": true,
        "create_fields": true
    }
}
```

- ---

#### Member

```text
GET /v1/members
```
Retrieve all members.

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "pk": "7058c114-9d4d-4f80-8fe3-4ef5834c40d1",
            "namespace": {
                "pk": "91a0a247-7dd5-4888-8d5a-bc3b0adaa347",
                "name": "Name",
                "slug": "slug-of-the-namespace",
                "default_tag": "TAG-FROM-ORIGIN",
                "default_list_id": "1121231",
                "default_list_name": "My List",
                "sync_phone": true,
                "sync_address": true,
                "create_fields": true
            },
            "first_name": "JOHN",
            "last_name": "LENNON",
            "email": "johnlennno@beatles.com",
            "birthday": "1972-01-01",
            "phone_country_code": "+55",
            "phone_region_code": "62",
            "phone_number": "999887755",
            "address1": "Avenida Paulista",
            "address2": "Bela Vista",
            "city": "SÃO PAULO",
            "state": "SP",
            "zip_code": "1445000",
            "member_fields": [
                {
                    "label": "My custom field",
                    "tag": "MYCUSTOMFIELD1",
                    "field_type": "text",
                    "help_text": "Use it as you wish",
                    "reply": "My answer is no",
                    "active": true,
                    "created_at": "2020-02-22T19:33:45-0300",
                    "updated_at": "2020-02-22T21:18:05-0300"
                },
                {
                    "label": "My custom field 2",
                    "tag": "MYCUSTOMFIELD2",
                    "field_type": "number",
                    "help_text": "Tell you age",
                    "reply": "32",
                    "active": true,
                    "created_at": "2020-02-22T19:33:45-0300",
                    "updated_at": "2020-02-22T21:18:05-0300"
                }            
            ],
            "external_id": "e411161d-9985-4e4a-bba8-ae4f13803723",
            "tags": "Pending,Paid,In Debt",
            "synchronized": true,
            "mailchimp_id": "xxxxxxxxxxxxxxxxxx",
            "excluded": false,
            "created_at": "2020-02-20T19:41:49-0300",
            "updated_at": "2020-02-22T21:34:07-0300"
        }
    ]
}
```

- ---

```text
GET /v1/members/:pk
PUT /v1/members/:pk
PATCH /v1/members/:pk
DELETE /v1/members/:pk
```

Create a member, or edit or delete it.

**Request:**
```json
{
    "namespace": {
        "pk": "91a0a247-7dd5-4888-8d5a-bc3b0adaa347"
    },
    "first_name": "JOHN",
    "last_name": "LENNON",
    "email": "johnlennno@beatles.com",
    "birthday": "1972-01-01",
    "phone_country_code": "+55",
    "phone_region_code": "62",
    "phone_number": "999887755",
    "address1": "Avenida Paulista",
    "address2": "Bela Vista",
    "city": "SÃO PAULO",
    "state": "SP",
    "zip_code": "1445000",
    "member_fields": [
        {
            "tag": "MYCUSTOMFIELD1",
            "reply": "My answer is no"
        },
        {
            "tag": "MYCUSTOMFIELD2",
            "reply": "32"
        }            
    ],
    "external_id": "e411161d-9985-4e4a-bba8-ae4f13803723",
    "tags": "Pending,Paid,In Debt",
    "synchronized": false,
    "excluded": false
}
```

**Response:**
```json
{
    "pk": "7058c114-9d4d-4f80-8fe3-4ef5834c40d1",
    "namespace": {
        "pk": "91a0a247-7dd5-4888-8d5a-bc3b0adaa347",
        "name": "Name",
        "slug": "slug-of-the-namespace",
        "default_tag": "TAG-FROM-ORIGIN",
        "default_list_id": "1121231",
        "default_list_name": "My List",
        "sync_phone": true,
        "sync_address": true,
        "create_fields": true
    },
    "first_name": "JOHN",
    "last_name": "LENNON",
    "email": "johnlennno@beatles.com",
    "birthday": "1972-01-01",
    "phone_country_code": "+55",
    "phone_region_code": "62",
    "phone_number": "999887755",
    "address1": "Avenida Paulista",
    "address2": "Bela Vista",
    "city": "SÃO PAULO",
    "state": "SP",
    "zip_code": "1445000",
    "external_id": "e411161d-9985-4e4a-bba8-ae4f13803723",
    "member_fields": [
        {
            "label": "My custom field",
            "tag": "MYCUSTOMFIELD1",
            "field_type": "text",
            "help_text": "Use it as you wish",
            "reply": "My answer is no",
            "active": true,
            "created_at": "2020-02-22T19:33:45-0300",
            "updated_at": "2020-02-22T21:18:05-0300"
        },
        {
            "label": "My custom field 2",
            "tag": "MYCUSTOMFIELD2",
            "field_type": "number",
            "help_text": "Tell you age",
            "reply": "32",
            "active": true,
            "created_at": "2020-02-22T19:33:45-0300",
            "updated_at": "2020-02-22T21:18:05-0300"
        }            
    ],
    "tags": "Pending,Paid,In Debt",
    "synchronized": false,
    "mailchimp_id": "xxxxxxxxxxxxxxxxxx",
    "excluded": false,
    "created_at": "2020-02-20T19:41:49-0300",
    "updated_at": "2020-02-22T21:34:07-0300"
}
```
