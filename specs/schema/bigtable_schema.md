# Overview
This markdown is created to document the schema design for our wide column store.
## Why wide column storage is being used
We are using a wide column store for the following reasons:
- **We have a write-heavy workload:** This is because we are storing time series data for ISS location indefinitely. Wide column storage is good for this because (as long as our schema is designed correctly) writes will be fast due to being sequential on disk. Range queries with an effective row key will also be fast since our data could be stored contiguously on disk and not require inefficient table scans.
- **Our query patterns are simple:** We care about adding new time series data points for ISS location (upsert) and reading time series on a rolling window (range query). Bigtable is good at supporting simple access patterns like this.
- **Durability is important for us:** It depends on the chosen wide column storage, but data stored tends to be durable. Bigtable specifically is built on top [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system), which uses write ahead logging and replication to prevent data loss.

For our use case, Bigtable is the chosen wide column storage, since it's natively supported in GCP and won't require self-managing a solution on GKE/GCP or a multi-cloud architecture.

## Data access patterns
As mentioned above, we need to support the following querying patterns:
1. **Upsert a new time series data point for ISS location:** Every *K* seconds, our lead replica in our ingestion service does the following:
   1. **Call the Open Notify API for ISS location data:** Short polling on just the lead replica removes unnecessary trafic on the Open Notify API.
   2. **Upsert the new location data into Bigtable:** This prevents redundant time series data from being added to Bigtable (due to multiple nodes polling similar data in a short window of time), reduces our storage and bandwidth cost (fewer rows needed in Bigtable), and reduces the latency for updates to clients (our range query below needs to scan fewer rows).
2. **Read time series data on ISS location for a rolling window W:** Every *K* seconds, nodes in our streaming API do the following for a rolling window ```[now - W, now]```:
   1. **Get the ISS datapoints between ```[now - W, now]```:** This is effectively a range query which we can optimize based on our row key.
   2. **If there are updates to the ISS datapoints sent, send a new event to clients:** We only need to send a new event to clients if the ISS data has since changed.

## Bigtable schema
Since we need to query based on time series data, we define our schema as follows. Some things to note:
- **Row key is defined using the reverse timestamp of each data point (revts):** This can be calculated using the maximum integer size on our node's architecture minus the actual timestamp value (2^63 - 1 - timestamp). This is done because row keys in Bigtable are ordered lexicographically, which means that the time series data on a rolling window will otherwise be stored at the end of our table. This is not ideal because it would require a [reverse scan which is slower than forward scans](https://docs.cloud.google.com/bigtable/docs/reads#reverse-scan).
- **We will use one column family called position:** Data for position (latitude, longitude) are always going to be accessed together. Since column families are stored in the same place on disk with Bigtable, it's best for us to couple these columns into one column family.
- **Cells will have one and only one value:** Bigtable allows cells to have more than one value with an associated timestamp. However, cells have a [size limit of 10MB](https://docs.cloud.google.com/bigtable/docs/schema-design#cells). Since we are upserting new rows for new ISS location data (and since reads/writes in Bigtable are atomic at the row level), we guarantee cells will have one and exactly one value at a time.
- **Rows will have a TTL of one year:** We will adjust this value if needed.

The concern Bigtable has for using [timestamp in a row key](https://docs.cloud.google.com/bigtable/docs/schema-design#cells) without another high-cardinality attribute is hotspots. Hotspots happen when we frequently access one part of our table in a short period of time. This would be a concern if we had multiple replicas in our ingestion service trying to upsert values at around the same time. But since we enforce at most one writer in our distributed coordination service every K seconds, this is not a concern for our use case.
```
Row key: iss#{revts}

Column families:
  position: Represents position for latitude longitude at a given timestamp

Columns:
  la: Represents latitude position
  lo: Represents longitude position

Table: iss_positions

| Row key (STRING) | position:la (FLOAT64) | position:lo (FLOAT64) |
|------------------|------------------------|------------------------|
| iss#381728272    | 78.6897                | 33.1734                | <- Latest time series data
| iss#381728277    | 79.6562                | 33.9509                |
| iss#381728282    | 80.0645                | 34.2722                | <- Older time series data

```
