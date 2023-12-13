class ListeningTest:
    def __init__(self, testName, id, sound_samples, src_dir):
        self.testName = testName
        self.id = id
        self.sound_samples = sound_samples
        self.src_dir = src_dir
        self.ratings = {sample:None for sample in sound_samples}
        