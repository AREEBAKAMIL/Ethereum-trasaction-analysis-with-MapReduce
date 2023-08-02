import re
import pyspark

sc = pyspark.SparkContext()



# this will check the lines in the transactions source file:

def good_lines(good):
    try:
        fields = good.split(',')
        if len(fields) != 7:
            return False
        int(fields[3])
        return True
    except:
        pass


# this will check the lines in the contracts source file:

def okay_lines(good):
    try:
        fields = good.split(',')
        if len(fields) != 5:
            return False
        return True
    except:
        pass


# this will aggregate all the values according to the 'to address'
transactions = sc.textFile("/data/ethereum/transactions")
clean_lines = transactions.filter(good_lines)
joiner = clean_lines.map(lambda value: (value.split(",")[2], int(value.split(",")[3])))
file1 = joiner.reduceByKey(lambda a, b: a + b)

contracts = sc.textFile("/data/ethereum/contracts")
clean = contracts.filter(okay_lines)
file2 = clean.map(lambda address: (address.split(",")[0], address.split(",")[0]))

combined_file = file1.join(file2)

top10 = combined_file.takeOrdered(10, key=lambda x: -x[1][0])

for record in top10:
    print("{} : {}".format(record[0], record[1][0]))
