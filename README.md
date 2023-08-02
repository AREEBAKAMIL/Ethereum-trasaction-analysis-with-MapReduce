# Ethereum-trasaction-analysis-with-MapReduce

Analysis of Ethereum Transactions using MapReduce on Hadoop.

For details on the implementation and the results please see: https://github.com/AREEBAKAMIL/Ethereum-trasaction-analysis-with-MapReduce/blob/main/Ethereum%20transaction%20Analysis%20results.pdf

# About the dataset
Ethereum is an open-source blockchain that is known for its smart contracts and serves as a basis for the cryptocurrency Ether. 
At its core, Ethereum is a decentralized global software platform powered by blockchain technology. It is most commonly known for its native cryptocurrency, ether (ETH).

Normally, one can use a CLI tool such as GETH to access the Ethereum blockchain, however, recent tools allow scraping all block/transactions and dump these to CSVs to be processed in bulk; notably Ethereum-ETL. These dumps are uploaded daily into a repository on Google BigQuery. I have used this source as the dataset for this coursework.

The dataset consists of the following schemas:
1. Blocks
2. Transactions
3. contracts
4. scams.json

## Blocks
The blocks schema consist of the following:
number: The block number
hash: Hash of the block
miner: The address of the beneficiary to whom the mining rewards were given
difficulty: Integer of the difficulty for this block
size: The size of this block in bytes
gas_limit: The maximum gas allowed in this block
gas_used: The total used gas by all transactions in this block
timestamp: The timestamp for when the block was collated
transaction_count: The number of transactions in the block

Example of a block:
| number| hash| miner| difficulty| size|gas_limit|gas_used| timestamp|transaction_count| 

|4776199|0x9172600443ac88e...|0x5a0b54d5dc17e0a...|1765656009004680| 9773| 7995996| 2042230|1513937536| 62|

## Transactions
The transactions schema consists of the following:
block_number: Block number where this transaction was in
from_address: Address of the sender
to_address: Address of the receiver. null when it is a contract creation transaction
value: Value transferred in Wei (the smallest denomination of ether)
gas: Gas provided by the sender
gas_price : Gas price provided by the sender in Wei
block_timestamp: Timestamp the associated block was registered at (effectively timestamp of the transaction)

Example of a transaction:
|block_number| from_address| to_address| value| gas| gas_price|block_timestamp|

| 6638809|0x0b6081d38878616...|0x412270b1f0f3884...| 240648550000000000| 21000| 5000000000| 1541290680| 

## Contracts
The contracts schema consist of the following:

address: Address of the contract
is_erc20: Whether this contract is an ERC20 contract
is_erc721: Whether this contract is an ERC721 contract
block_number: Block number where this contract was created

Example of a contract:
|address|is_erc20|is_erc721|block_number| block_timestamp| 

|0x9a78bba29a2633b...| false| false| 8623545|2019-09-26 08:50:...|

## Scams
The Scams.json schema consists of the following:

id: Unique ID for the reported scam
name: Name of the Scam
url: Hosting URL
coin: Currency the scam is attempting to gain
category: Category of scam - Phishing, Ransomware, Trust Trade, etc.
subcategory: Subdivisions of Category
description: Description of the scam provided by the reporter and datasource
addresses: List of known addresses associated with the scam
reporter: User/company who reported the scam first
ip: IP address of the reporter
status: If the scam is currently active, inactive or has been taken offline

Example:
0x11c058c3efbf53939fb6872b09a2b5cf2410a1e2c3f3c867664e43a626d878c0: { id: 81, name: "myetherwallet.us", url: "http://myetherwallet.us", coin: "ETH", category: "Phishing", subcategory: "MyEtherWallet", description: "did not 404.,MEW Deployed", addresses: [ "0x11c058c3efbf53939fb6872b09a2b5cf2410a1e2c3f3c867664e43a626d878c0", "0x2dfe2e0522cc1f050edcc7a05213bb55bbb36884ec9468fc39eccc013c65b5e4", "0x1c6e3348a7ea72ffe6a384e51bd1f36ac1bcb4264f461889a318a3bb2251bf19" ], reporter: "MyCrypto", ip: "198.54.117.200", nameservers: [ "dns102.registrar-servers.com", "dns101.registrar-servers.com" ], status: "Offline" },

# About the files

## Part A - Time Analysis: Number of transactions per month
For time analysis, the Blocks scheme was used as the input for the job. The blocks table consists of the fields transaction_count and timestamp. This job consists of a mapper, a combiner and a reducer. The output of this job is the sum of transacton_count for each month-year.

## Part B - Top Ten Most Popular Services
For this part, the top 10 addresses containing the highest value received are obtained. The contracts and transactions schema was used as the input. The transactions schema consists of the to_address and value. The contracts schema consists of addresses. In this job, the value transferred  is aggregated for each to_address from the transactions table and then the addresses in the contracts table are joined with the to_addresses from the transactions schema. This job consists of a mapper and 2 reducers.

## Part C - a comparative evaluation - Spark vs MrJob
Part B was implemented in Spark. The job ran much faster in Spark than in MrJob. The results obtained with Spark and MrJob are exactly the same. For this job, spark seems appropriate since it took much less amount of time. mrJob took around 25 minutes whereas Spark took around 4 minutes to run. Spark saves time by reducing the number of read and write cycles to disk and storing
intermediate data in-memory.

## Part C - gas guzzler
To check how the gas price has changed over time, the maximum gas prices for each month-year are calculated and sorted. Then the top ten are picked out. For this, the transactions table is used as the input. For this job, one mapper and 2 reducers are used.

