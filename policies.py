import collections
import joblib
import pandas as pd

class LRU_Policy:
    def __init__(self):
        self.access_order = collections.OrderedDict()
    def choose_victim(self, pages):
        victim, _ = self.access_order.popitem(last=False)
        return victim
    def update_on_hit(self, address, pages):
        self.access_order.move_to_end(address)
    def update_on_miss(self, address, pages):
        self.access_order[address] = None

class FIFO_Policy:
    def __init__(self):
        self.queue = collections.deque()
    def choose_victim(self, pages):
        return self.queue.popleft()
    def update_on_hit(self, address, pages):
        pass
    def update_on_miss(self, address, pages):
        self.queue.append(address)

class AI_Policy:
    def __init__(self, model_path="cache_model.joblib"):
        print("Initializing AI Policy...")
        self.model = joblib.load(model_path)
        print("Model loaded successfully.")
        self.recency = collections.defaultdict(int)
        self.frequency = collections.defaultdict(int)
        # NEW: Store metadata (like stride) for each page
        self.metadata = {} 
        self.previous_address = 0

    def choose_victim(self, pages):
        feature_list = []
        page_order = []
        for page in pages:
            # NOW, each page uses its OWN stride from when it was cached
            page_stride = self.metadata.get(page, {}).get('stride', 0)
            feature_list.append({
                'recency': self.recency[page],
                'frequency': self.frequency[page],
                'stride': page_stride 
            })
            page_order.append(page)
        
        df = pd.DataFrame(feature_list)[['recency', 'frequency', 'stride']]
        predictions = self.model.predict(df)
        
        try:
            victim_index = list(predictions).index(1)
            victim = page_order[victim_index]
        except ValueError:
            victim = min(pages, key=lambda p: self.frequency[p])

        # Clean up all data for the victim
        del self.recency[victim]
        del self.frequency[victim]
        del self.metadata[victim]
        return victim

    def _update_features(self, address_str):
        address_int = int(address_str, 16)
        # The stride is the difference from the PREVIOUS access
        stride = address_int - self.previous_address
        self.previous_address = address_int

        for page in self.recency:
            self.recency[page] += 1
        
        self.recency[address_str] = 0
        self.frequency[address_str] += 1
        # Return the calculated stride so it can be stored
        return stride

    def update_on_hit(self, address_str, pages):
        self._update_features(address_str)

    def update_on_miss(self, address_str, pages):
        stride = self._update_features(address_str)
        self.frequency[address_str] = 1
        # STORE the stride when the page is added
        self.metadata[address_str] = {'stride': stride}