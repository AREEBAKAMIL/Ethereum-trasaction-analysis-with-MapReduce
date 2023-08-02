from mrjob.job import MRJob
from mrjob.step import MRStep


class partB(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper_1,
                       reducer=self.reducer_1),
                MRStep(reducer=self.reducer_2)]

    def mapper_1(self, _, line):
        fields = line.split(",")
        try:
            if len(fields) == 7:
                to_address = fields[2]
                values = int(fields[3])
                yield (to_address, [1, values])

            elif len(fields) == 5:
                address = fields[0]
                yield (address, [2])
        except:
            pass

    def reducer_1(self, address, values):
        exists = False
        summation = 0
        for value in values:
            if value[0] == 1:
                summation += value[1]
            elif value[0] == 2:
                exists = True
        if exists and summation > 0:
            yield (None, [address, summation])

    def reducer_2(self, key, value):
        sorted_vals = sorted(value, reverse=True, key=lambda t: t[1])
        i = 0
        for val in sorted_vals:
            address = val[0]
            total = val[1]
            yield ("{}: {}".format(address, total), None)
            i = i + 1
            if i >= 10:
                break


if __name__ == '__main__':
    partB.run()
