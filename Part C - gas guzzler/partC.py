"""Ethereum analysis
"""
from mrjob.job import MRJob
import re
import time
from mrjob.job import MRJob
from mrjob.step import MRStep

class partC(MRJob):

    def steps(self):
        return [MRStep(mapper=self.mapper_1,
                       reducer=self.reducer_1),
                 MRStep(reducer=self.reducer_2)]

    def mapper_1(self, _, line):
        fields = line.split(",")
        try:
            if(len(fields) == 7):
                time_epoch = int(fields[6])
                month_year = time.strftime("%B-%Y",time.gmtime(time_epoch)) #returns month and year
                gas_price = int(fields[5])
                yield (month_year, gas_price)
        except:
            pass

    # def combiner_1(self, combiner_1, gas_p):
    #     yield (None, [month_y, max(gas_p)])

    def reducer_1(self, month_y, gas_p):
        yield (None, [month_y, max(gas_p)])

    def reducer_2(self, key, values):
        #values = [month-year : max(gas_price)]
        sorted_values = sorted(values, reverse=True, key=lambda t: t[1])
        i = 0
        for val in sorted_values:
            month_year = val[0]
            gas_price = val[1]
            yield ("{}: {}".format(month_year, gas_price), None)
            i = i + 1
            if i >= 10:
                break



if __name__ == '__main__':
    partC.run()
