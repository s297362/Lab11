from dataclasses import dataclass
@dataclass
class Colore:
    Product_color: str

    def __hash__(self):
        return hash(self.Product_color)
    def __eq__(self, other):
        return self.Product_color == other.Product_color
