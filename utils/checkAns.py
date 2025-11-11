class CheckAns:
    def __init__(self, input, answer):
        self.input = input
        self.answer = answer
    def result(self):
        return True if self.input in self.answer else False
