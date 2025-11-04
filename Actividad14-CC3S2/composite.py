from typing import List, Dict

class CompositeModule:
    def __init__(self):
        self.children: List[Dict] = []

    def add(self, block: Dict):
        self.children.append(block)

    def export(self) -> Dict:
        merged: Dict = {"resource": {}}
        for child in self.children:
            for rtype, resources in child.get("resource", {}).items():
                merged["resource"].setdefault(rtype, {}).update(resources)
        return merged