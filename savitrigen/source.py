class Source(object):
    def create(self, trees:list):
        for tree in trees:
            tree.set_on_cache(False)
            tree.set_silent(False)
            tree.create()
