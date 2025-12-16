# Overview
Since we cannot execute on the Bigtable schema implementation due to pricing concerns, we are instead opting to use [Firestore](https://firebase.google.com/docs/firestore) in GCP. This markdown file defines the tradeoffs, our access patterns, schema design, and our TTL.

## Why document storage is okay for our use case
We decided to go with Firestore instead, which is a document store supported natively in GCP. These are the reasons why:
- **Bigtable pricing per node, while Firestore pricing is per read/write/delete on documents:** The initial choice for wide column storage made sense since we had a write-heavy workload and simple query patterns. The lowest price per node in a Bigtable was too high for us to justify. Since we only need to store time series data for a single object over a long period of time, provisioning a Bigtable database in just one region with no replication is already overkill.
- **Our querying patterns are simple:** Document storage with proper indexing can still support our access patterns reasonably well.
- **We can add additional data beyond ISS position later if needed:** Firestore is a document store, which is schemaless and flexible to changes in the data we need to include. This is not a driving factor but a nice to have if we want to build on top of this later.

## Data access patterns
(The querying patterns do not change, so they are added again here)

As mentioned above, we need to support the following querying patterns:
1. **Upsert a new time series data point for ISS location:** Every *K* seconds, our lead replica in our ingestion service does the following:
   1. **Call the Open Notify API for ISS location data:** Short polling on just the lead replica removes unnecessary trafic on the Open Notify API.
   2. **Leader upserts the new location data into a document in Firestore:** This prevents redundant documents from being added to Firestore (due to multiple nodes polling similar data in a short window of time), reduces our storage and bandwidth cost (fewer documents needed in Firestore), and reduces the latency for updates to clients (our range query below needs to scan fewer documents).
2. **Read time series data on ISS location for a rolling window W:** Every *K* seconds, nodes in our streaming API do the following for a rolling window ```[now - W, now]```:
   1. **Get the ISS datapoints between ```[now - W, now]```:** This is effectively a range query which we can optimize based on indexing for our root collection.
   2. **If there are updates to the ISS datapoints sent, send a new event to clients:** We only need to send a new event to clients if the ISS data has since changed.

## Firestore database design
We still need to query based on time series data, so we define our database as follows. Some things to note:
- **We only have one collection under root:** Since we only care about ISS location data at a specific point in time, we have one collection called ```iss_location```.
- **We will use auto IDs for documents in iss_location**: Auto IDs prevent hotspots and make it easier for us on the client when doing upserts (biggest reason). We don't need to use timestamps for the document ID (even though it's slightly better for range queries) since it's a micro-optimization that just adds complexity.
- **Documents in the root collection will have no TTL:** We will adjust this value if needed.

```
Collection: iss_locations

Documents:
{
   "id": Auto,
   "ts": Integer,
   "pos_la": Floating-point number
   "pos_lo": Floating-point number
}
```
