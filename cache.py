class Cache:
    def __init__(self, size, policy):
        self.size = size
        self.policy = policy
        self.pages = {}

    def access(self, address):
        if address in self.pages:
            self.policy.update_on_hit(address, self.pages)
            return True
        else:
            if len(self.pages) >= self.size:
                victim = self.policy.choose_victim(self.pages)
                del self.pages[victim]
            
            self.pages[address] = {}
            self.policy.update_on_miss(address, self.pages)
            return False