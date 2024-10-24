### Here are the attributes of the items setup in a class


class Item:
    def __init__(self,name,input_materials,production_facility,production_rate,power_use) -> None:
        self.name = name
        self.input_materials = input_materials
        self.production_facility = production_facility
        self.production_rate = production_rate
        self.power_use = power_use
    
    

    def __str__(self):
        return f"{self.name}: {self.input_materials}, Facility: {self.production_facility}, Rate: {self.production_rate}, Power Use: {self.power_use} MW"