import json
from data import classes

def getItems(urlPrefix):
    obj=json.loads(classes)
    items={}
    for r in obj["firstLevelCategoryList"]:
        items[r["id"]]={
            "name":r["name"],
            "id":r["id"],
            "subItems":[]}
    for r in obj["secondLevelCategoryList"]:
        key=r["supId"]
        if( key not in items):
            print("{0} not in the result",key)
            continue
        items[key]["subItems"].append({
            "id":r["id"],
            "name":r["name"],
            "url":"/category/{1}".format(urlPrefix,r["id"])
            })
    return items