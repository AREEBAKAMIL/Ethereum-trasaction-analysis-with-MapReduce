"""Ethereum analysis
"""
from mrjob.job import MRJob
import re
import time

# Create a bar plot showing the number of transactions occurring every month between the start and end of the dataset.

class partA(MRJob):

    def mapper(self, _, line):
        fields = line.split(",")
        try:
            if(len(fields) == 9):
                time_epoch = int(   fields[7])
                month_year = time.strftime("%B-%Y",time.gmtime(time_epoch)) #returns month and year
                transaction_count = int(fields[8])
                yield (month_year, transaction_count)
        except:
            pass

    def combiner(self, month_y, transation_no):
         yield(month_y, sum(transation_no))

    def reducer(self, month_y, transation_no):
        yield(month_y, sum(transation_no))



if __name__ == '__main__':
    #Lab2.JOBCONF= { 'mapreduce.job.reduces': '3' }
    partA.run()
