import json
class ItemManager:
    def __init__(self, knight):
        itemsPath = "JSON/Items/Items.json"
        itemsEffectPath = "JSON/Items/Item_Effects.json"
        equipmentPath = "JSON/Items/Equipment.json"
        itemFusionPath = "JSON/Items/Item_Fusion.json"


        file = open(itemsPath, "r")
        file2 = open(itemsEffectPath, "r")
        file3 = open(equipmentPath, "r")
        file4 = open(itemFusionPath, "r")

        self.itemJson = json.load(file)
        self.itemEffectJson = json.load(file2)
        self.equipmentJson = json.load(file3)
        self.itemFusionJson = json.load(file4)
        self.knight = knight

        file.close()
        file2.close()
        file3.close()
        file4.close()

    def determine_limited(self, item):
        flag = False
        itemInfo = self.itemJson[item]
        # if the item is limited and knight doesn't have it, it is purchasable
        if itemInfo["Limited"] and self.knight.Inventory.get(item) is None:
            flag = True
        # if the item isn't limited, it's purchasable
        elif not itemInfo["Limited"]:
            flag = True
        return flag

    def get_all_purchasable(self):
        purchasableItems = {}
        for item, itemInfo in self.itemJson.items():  # Loop through all item and key pairs
            # if the item is deemed purchasable add it to the dictionary
            if itemInfo["Purchasable"] and self.determine_limited(item):
                purchasableItems.update({
                    item: itemInfo["Buy"]  # map the item to the purchase price
                })
        return purchasableItems

    def get_all_sellable(self):
        sellableItems = {}
        for item, itemInfo in self.itemJson.items():  # Loop through all item and key pairs
            # if the item isn't a key item add it to the dictionary
            if itemInfo["Type"] != "Key":
                sellableItems.update({
                    item: itemInfo["Sell"]  # map the item to its sell price
                })
        return sellableItems

    def get_effect(self, item):
        # returns the effect string if the item has an effect or returns empty string
        if self.itemJson[item]["Effect"]:
            return self.itemEffectJson[item]
        else:
            return ""

    def get_parsable_item_info(self, item):
        # return a dictionary that's easier to parse
        itemInfo = self.itemJson[item]  # get the dictionary describing the item
        itemInfo["Effect"] = self.get_effect(item)  # map the effect, if it exists, to the "Effect" key
        itemInfo.pop("Purchasable")  # remove Purchasable key
        itemInfo.pop("Limited")  # remove Limited key
        itemInfo.pop("Fusion")  # remove the fusion portion
        return itemInfo


    def get_usable_items(self):
        # This function returns an array of usable items from the Knights inventory
        consumables = []
        # loop through the knights inventory and find add consumable items to the list
        for item in self.knight.Inventory:
            itemInfo = self.itemJson[item]
            if itemInfo["Type"] == "Consumable":
                consumables.append(item)
        for i in range(len(consumables)):
            consumable = consumables[i]  # get the name of the consumable
            # replace the same index with the consumable x the amount
            consumables[i] = consumable + " x" + str(self.knight.Inventory[consumable])
        return consumables

    def fuse_items(self, material1, material2):
        fusionOccured = False  # indicator for if a fusion happened
        for item, fusionMaterials in self.itemFusionJson.items():
            listA = fusionMaterials[0]
            listB = fusionMaterials[1]
            if ((material1 in listA) or (material1 in listB)) and ((material2 in listA) or (material2 in listB)):
                fusionOccured = True
                if self.knight.Inventory.get(item):
                    # if the fused item exists in the inventory, get the amount and add 1 to it
                    amount = self.knight.Inventory[item]
                    self.knight.Inventory.update({item: 1 + amount})
                else:
                    # if the fused item does not exist in the inventory, create an entry for it
                    self.knight.Inventory.update({item: 1})
                # lower the amount in the inventory for the used items
                amount = self.knight.Inventory[material1]
                self.knight.Inventory.update({material1: amount - 1})
                amount = self.knight.Inventory[material2]
                self.knight.Inventory.update({material2: amount - 1})
                self.knight.correct_inventory()  # remove any items with 0 amount in inventory
        return fusionOccured

