# Open-Notify-Streaming-API
Real time updates from Open Notify with server sent events (SSEs).

## Table of contents
- [Open-Notify-Streaming-API](#open-notify-streaming-api)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [API Documentation](#api-documentation)
    - [Resources](#resources)
      - [GET::/v1/iss/location](#getv1isslocation)
        - [Example usage](#example-usage)
          - [Retrieve ISS location data for past 30 seconds](#retrieve-iss-location-data-for-past-30-seconds)
          - [Provide an invalid window of time](#provide-an-invalid-window-of-time)
      - [GET::/v1/iss/stream](#getv1issstream)
        - [Example Usage](#example-usage-1)
          - [Client successfully streams ISS location data from application server.](#client-successfully-streams-iss-location-data-from-application-server)

## Overview
This repository was created primarily to resolve some personal knowledge gaps (not any tanglible issue). This is in regard for the following items:
- **Streaming APIs:** I've had conceptual understanding of long-lived HTTP connections with web sockets and server sent events, but never had the chance to build anything directly with either. This repository has a small streaming API created to read near real time updates from the [Open Notify ISS Location API](http://open-notify.org/Open-Notify-API/ISS-Location-Now). This API's documentation has an example of updates which use [short polling](https://www.geeksforgeeks.org/javascript/what-is-long-polling-and-short-polling/) to update the client's browser.
  - By proxying calls to the ISS Location API with a streaming API, calls from short polling no longer need to be done independently across every clients' browser. This kind of pattern allows us to scale client connections independently of updates from short polling.
- **Distributed coordination services:** Also only had conceptual understanding of distributed coordination services. I wanted to use one for this project to implement a consensus protocol like Raft. This project has a stateful service called `ingestion`, which runs [ZooKeeper](https://zookeeper.apache.org/index.html) with leader election. The leader handles short polling from Open Notify, updates to a Redis channel, and upserts into Firestore document storage. [Sequential ephemeral znodes](https://zookeeper.apache.org/doc/r3.9.4/recipes.html#sc_leaderElection) was implemented to elect a new leader from the ensemble if the current leader crashes for whatever reason.
  - Because of the way failures could happen (hardware failure, outages etc.), in a real setting using separate physical hosts for every node in the ensemble makes the most sense. This is because replication of virtual nodes on the same physical host makes that host a single source of failure.
- **Infrastructure as Code:** Past work involved manually provisioning resources in public clouds from their respective consoles. Due to constraints (primarily financial), I would eventually manually deprovision everything to save on cloud billing. Not having infrastructure managed from an infra as code tool makes going back to past projects a lot more difficult - if I want to reconfigure a project on a public cloud like GCP, I would need to remember exactly what configurations were used in offerings like GCE, GKE, etc. for the project to work as expected. This project manages a cluster in GCP with [Terraform](https://developer.hashicorp.com/terraform/docs) to avoid this kind of cognitive debt for future work.
- **Configuration management across multiple k8s clusters:** Previously struggled with manually applying patches and editing k8s manifests for development purposes. This project uses [kustomize](https://kustomize.io/) with overlays to handle configuration changes between development and staging environments.
- **Miscellaneous:** Better understanding of container networking, managing common dependencies across projects using a package manager like PyPI, using build backends like Hatch.

![Component Diagram](/specs/diagrams/component_diagram.png)

## API Documentation
### Resources
#### GET::/v1/iss/location

| Resource | Description | Type | Request Headers | Path parameters | Query parameters |
| ---- | ---- | ---- | ---- | ---- | ---- |
| /v1/iss/location | Retrieve ISS location data on a rolling window. | GET  | N/A | N/A | **window** - The window size in seconds. Default value of 30. |

| Status code | Description                                             |
| ----------- | ------------------------------------------------------- |
| 200         | A rolling window of ISS location data is successfully returned. |
| 400         | Miscellaneous client failure                            |
| 500         | Miscellaneous service failure                           |

##### Example usage

###### Retrieve ISS location data for past 30 seconds
**Request**
```
GET /v1/iss/location?window=30 HTTP/1.1
Host: localhost
User-Agent: curl/8.1.2
Accept: */*
```

**Response**
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Tue, 24 Feb 2026 06:21:55 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 248

{
    "locations": [
        {
            "pos_la": "-50.8442",
            "pos_lo": "145.8207",
            "ts": 1771914092
        },
        {
            "pos_la": "-50.9072",
            "pos_lo": "146.3504",
            "ts": 1771914098
        },
        {
            "pos_la": "-50.9835",
            "pos_lo": "147.0267",
            "ts": 1771914105
        },
        {
            "pos_la": "-51.0354",
            "pos_lo": "147.5113",
            "ts": 1771914110
        }
    ]
}
```

###### Provide an invalid window of time
**Request**
```
GET /v1/iss/location?window=-1 HTTP/1.1
Host: localhost
User-Agent: curl/8.1.2
Accept: */*
```

**Response**
```
HTTP/1.1 400 BAD REQUEST
Server: gunicorn
Date: Tue, 24 Feb 2026 06:23:55 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 131


{
    "description": "The browser (or proxy) sent a request that this server could not understand.",
    "message": "Invalid window size: -1"
}
```

#### GET::/v1/iss/stream

| Resource | Description | Type | Request Headers | Path parameters | Query parameters |
| ---- | ---- | ---- | ---- | ---- | ---- |
| /v1/iss/stream | Retrieve rolling updates for ISS location. | GET | **Accept:** `text/event-stream` media type. <br /> **Cache-Control:** `no-cache` | N/A | N/A |

| Status code | Description                                             |
| ----------- | ------------------------------------------------------- |
| 200         | When a unidirectional HTTP connection to the client is accepted |
| 400         | Miscellaneous client failure                            |
| 500         | Miscellaneous service failure                           |

##### Example Usage
The Accept and Content-Type headers are important. The `text/event-stream` MIME type enables us to send back events based on the format outlined [here](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format).

###### Client successfully streams ISS location data from application server.

**Request**
```
GET /v1/iss/stream HTTP/1.1
Host: localhost
User-Agent: curl/8.1.2
Accept: */*
```

**Response**
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Tue, 24 Feb 2026 06:40:28 GMT
Connection: keep-alive
Transfer-Encoding: chunked
Content-Type: text/event-stream; charset=utf-8

event:iss_location
data:{"pos_la": "-19.5750", "pos_lo": "-131.9883", "ts": 1771915228}

event:iss_location
data:{"pos_la": "-18.6509", "pos_lo": "-131.2160", "ts": 1771915247}

event:iss_location
data:{"pos_la": "-18.2360", "pos_lo": "-130.8734", "ts": 1771915255}

event:iss_location
data:{"pos_la": "-17.9917", "pos_lo": "-130.6728", "ts": 1771915260}

event:iss_location
data:{"pos_la": "-17.7472", "pos_lo": "-130.4728", "ts": 1771915265}

event:iss_location
data:{"pos_la": "-17.5024", "pos_lo": "-130.2734", "ts": 1771915270}

event:iss_location
data:{"pos_la": "-17.2574", "pos_lo": "-130.0746", "ts": 1771915275}

event:iss_location
data:{"pos_la": "-17.0120", "pos_lo": "-129.8763", "ts": 1771915280}

event:iss_location
data:{"pos_la": "-16.7665", "pos_lo": "-129.6787", "ts": 1771915285}

event:iss_location
data:{"pos_la": "-16.5207", "pos_lo": "-129.4816", "ts": 1771915290}

event:iss_location
data:{"pos_la": "-16.2254", "pos_lo": "-129.2457", "ts": 1771915296}

event:iss_location
data:{"pos_la": "-15.9792", "pos_lo": "-129.0498", "ts": 1771915301}

```
