import json
class ItemManager:
    def __init__(self, knight):
        itemsPath = "JSON/Items/Items.json"
        itemsEffectPath = "JSON/Items/Item_Effects.json"

        file = open(itemsPath, "r")
        file2 = open(itemsEffectPath, "r")

        self.itemJson = json.load(file)
        self.itemEffectJson = json.load(file2)
        self.knight = knight
        file.close()
        file2.close()

    def get_all_purchasable(self):
        purchasableItems = {}
        for item, itemInfo in self.itemJson.items():  # Loop through all item and key pairs
            # if the item is deemed purchasable add it to the dictionary
            if itemInfo["Purchasable"] and self.determine_limited(item, itemInfo):
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

    def determine_limited(self, item, itemInfo):
        flag = False
        # if the item is limited and knight doesn't have it, it is purchasable
        if itemInfo["Limited"] and self.knight.Inventory.get(item) is None:
            flag = True
        # if the item isn't limited, it's purchasable
        elif not itemInfo["Limited"]:
            flag = True
        return flag
