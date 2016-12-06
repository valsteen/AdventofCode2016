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


class Advent5Part2(Advent5):
    def find(self):
        found = 0
        self.result = [None] * self.iterations

        while found < self.iterations:
            hash = md5("{}{}".format(self.input, self.index)).hexdigest()
            if hash.startswith("00000"):
                try:
                    position = int(hash[5])
                except ValueError:
                    pass
                else:
                    if position < self.iterations:
                        character = hash[6]

                        if self.result[position] is None:
                            self.result[position] = character
                            print self.result
                            found += 1

            self.index += 1

        return "".join(self.result)


#print Advent5("abc", 8).find()
print Advent5Part2("abc", 8).find()
print Advent5Part2("uqwqemis", 8).find()