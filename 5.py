from hashlib import md5


class Advent5(object):
    def find(self):
        while len(self.result) < self.iterations:
            hash = md5("{}{}".format(self.input, self.index)).hexdigest()
            if hash.startswith("00000"):
                self.result.append(hash[5])

            self.index += 1

        return "".join(self.result)

    def __init__(self, input, iterations):
        self.result = []
        self.index = 0
        self.iterations = iterations
        self.input = input


#print Advent5("abc", 8).find()
print Advent5("uqwqemis", 8).find()