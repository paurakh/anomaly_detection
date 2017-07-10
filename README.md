# Table of Contents
1. [Program Description](README.md#program-description)
2. [Input and Output](README.md#input-and-output)
3. [Pseudocode](README.md#pseudocode)
4. [Data Structure](README.md#data-structure)
5. [Optimized Features](README.md#optimized-features)
6. [Contact](README.md#contact)


# Program Description

This python scripts flags purchases that are anomalous or outlier among recent `T` purchases made in buyer's network (exluding self purchases). The script first builds undirected graph from the file `batch_log.json`. `batch_log.json` is also used to create the purchase history of the network. `stream_log.json` is used to mutate the state of the graph as new activities (friend, unfriend, or purchase) are read from this file. Purchases that are anomalous (> 3 `sd` than the `mean`) are flagged and stored in `flagged_purchases.json` along with calculated mean and the standard deviation.

# Input and Output

## Input File: 
`batch_log.json`
`stream.json`
## Output File: 
`flagged_purchases.json`

## Dependencies
1. The script assumes that the first two lines of `batch_log.json` contains parameters `D` and `T`
2. All functions written in the filename `NetworkGraph.py` are stored inside .\src\ folder and imported in the main script file `process_log.py`

# Pseudocode
1. Open file `batch_log.json` and read `D` and `T` value
2. Read a line at a time from `batch_log.json` after reading D and T value
3. If activity is friend or unfriend, create or erase edges between the nodes
4. If activity is purchase:
    1. Store in a master purchase history
    2. Store its index in master purchase history information in that user's node
    3. Check and store no more than T purchases from that user
5. Keep track of the last befriending/unfriending activity    
6. Open file `stream_log.json`
7. Read a line at a time
8. Condition on Activities: 
    1. If befreinding/unnfriending do as step 3., while keeping track of the last befriending/unfriending activity
    2. If purchase
        1. Find the purchasing users network 
        2. Compute the mean and sd from the network's last T transcations (excluding the user's transactions)
        3. Determine if current purchase amount > `mean` + 3 * `sd`. If so, save the transaction, mean and sd value
        4. Populate this transaction in all the network nodes for next round of computation


# Optimized Features
1. We only store last `T` transaction from each user or node. We know thats the worse case scenario when a network is limited to being just one user. This prevents memory overflow
2. We pass the current purchases made to all the network users for future use. We also check and use the previously sorted `T` values from the network if there are no befriending/unfriending activity. This reduces the number of processing including sorting required
3. Timestamps are sorted out but if there is same time stamp, the later occurence is queued later

# Contact
paurakh[at]gmail[dot]com



