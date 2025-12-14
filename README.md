# Open-Notify-Streaming-API
Real time updates from Open Notify with server sent events (SSEs).

## Table of contents
- [Open-Notify-Streaming-API](#open-notify-streaming-api)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [API Documentation](#api-documentation)
    - [Resources](#resources)
      - [GET::/v1/iss/events](#getv1issevents)
        - [HTTP response status codes](#http-response-status-codes)
        - [Example Usage](#example-usage)

## Overview
## API Documentation
### Resources
#### GET::/v1/iss/events
Retrieve rolling updates based on fixed interval for ISS location.


| Resource       | Description                                                      | Type | Path parameters                                               | Query parameters                                               |
| -------------- | ---------------------------------------------------------------- | ---- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| /v1/iss/events | Retrieve rolling updates based on fixed interval for ISS location. | GET  | N/A | **window** - The window size in seconds. Default value of 30. |

##### HTTP response status codes
| Status code | Description                                             |
| ----------- | ------------------------------------------------------- |
| 200         | When a unidirectional HTTP connection to the client is accepted |
| 400         | Miscellaneous client failure                            |
| 500         | Miscellaneous service failure                           |

##### Example Usage
The Accept and Content-Type headers are important. The `text/event-stream` MIME type enables us to send back events based on the format outlined [here](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format).

**Request**
```
GET /v1/iss/events?window=60 HTTP/1.1
Host: 127.0.0.1 // TBD
Accept: text/event-stream
Cache-Control: no-cache
```

**Response (200)**
```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

// Time series data for past 20 seconds
event: iss_position_update
data: {
    "iss_positions": [
        {"latitude": "-39.3659", "longitude": "178.8003"}, "timestamp": 1765691100},
        {"latitude": "-39.8824", "longitude": "179.6570"}, "timestamp": 1765691105},
        {"latitude": "-40.2980", "longitude": "-179.6347"}, "timestamp": 1765691110},
        {"latitude": "-40.7826", "longitude": "-178.7857"}, "timestamp": 1765691115},
        {"latitude": "-41.1871", "longitude": "-178.0570"}, "timestamp": 1765691120}
    ]
}

// After fixed interval, new time series series data based on window size
event: iss_position_update
data: {
    "iss_positions": [
        {"latitude": "-39.8824", "longitude": "179.6570"}, "timestamp": 1765691105},
        {"latitude": "-40.2980", "longitude": "-179.6347"}, "timestamp": 1765691110},
        {"latitude": "-40.7826", "longitude": "-178.7857"}, "timestamp": 1765691115},
        {"latitude": "-41.1871", "longitude": "-178.0570"}, "timestamp": 1765691120},
        {"latitude": "-41.6980", "longitude": "-178.0459"}, "timestamp": 1765691125}
    ]
}

// . . .
```
