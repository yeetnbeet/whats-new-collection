
import requests as req
import os 

class MetaFieldsPy :
    STORE_NAME = os.getenv("STORE_NAME")
    H = {"X-Shopify-Access-Token":os.getenv("SECRET_TOKEN"),
    "Content-Type":"application/json"}


    def getMetafields(self,productId) :
        res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/products/"+str(productId)+"/metafields.json",headers=self.H)
        resdata = res.json()
        return resdata["metafields"]

    def modifyExistingMetaField(self,metaFieldId,productId,value,type):
        d = {"metafield":{
            "id":metaFieldId,
            "value":value,
            "type":type
        }} 
        res = req.put("https://"+self.STORE_NAME+"/admin/api/2022-10/products/"+str(productId)+"/metafields/"+str(metaFieldId)+".json",headers=self.H,json=d)
        print(res.text)
        print(str(d))

    def createNewMetafield(self,productId,namespace,key,value,type):
        d = {"metafield":{
            "namespace":namespace,
            "key":key,
            "value":value,
            "type":type
        }}
        res = req.post("https://"+self.STORE_NAME+"/admin/api/2022-10/products/"+str(productId)+"/metafields.json",headers=self.H,json=d)
        print(res.status_code)

    def productHasMetaField(self,productId,metaFieldKey):
        metaFields = self.getMetafields(productId)
        for item in metaFields:
            if item["key"]== metaFieldKey :
                return int(item["id"])
        return False

class ProductsPy :
    STORE_NAME = os.getenv("STORE_NAME")
    H = {"X-Shopify-Access-Token":os.getenv("SECRET_TOKEN"),
        "Content-Type":"application/json"}
    PRODUCT_LIST = []

    def getAllProductsFromCollection(self,collectionID="",URL=None):
        if URL is None :
            print("Recursive1")
            res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/products.json?collection_id="+str(collectionID),headers=self.H)
            resdata = res.json()
            for item in resdata ["products"]:
                self.PRODUCT_LIST.append(item)
            if res.links != {}:
                url = res.links['next']['url']
                self.getAllProductsFromCollection(URL=url)

        elif URL is not None:
            print("Recursive2")
            res = req.get(URL,headers=self.H)
            resdata = res.json()
            for item in resdata ["products"]:
                self.PRODUCT_LIST.append(item)
            if res.links != {} and len(res.links) == 2:
                url = res.links['next']['url']
                self.getAllProductsFromCollection(URL=url)

    def getAllProductsByStatus(self,status="",URL=None):
        if URL is None :
            print("Recursive1")
            res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/products.json?status="+str(status),headers=self.H)
            resdata = res.json()
            for item in resdata ["products"]:
                self.PRODUCT_LIST.append(item)
            if res.links != {}:
                url = res.links['next']['url']
                self.getAllProductsFromCollection(URL=url)

        elif URL is not None:
            print("Recursive2")
            res = req.get(URL,headers=self.H)
            resdata = res.json()
            for item in resdata ["products"]:
                self.PRODUCT_LIST.append(item)
            if res.links != {} and len(res.links) == 2:
                url = res.links['next']['url']
                self.getAllProductsFromCollection(URL=url)

    def getSingleProduct(self,productID) :
        res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/products/"+str(productID)+".json",headers=self.H)
        return res.json()

    def deleteProduct(self,productId) :
        res = req.delete("https://"+self.STORE_NAME+"/admin/api/2022-10/products/"+str(productId)+".json",headers=self.H)
        return res.json(), res.status_code
        
class CollectionPy :
    STORE_NAME = os.getenv("STORE_NAME")
    H = {"X-Shopify-Access-Token":os.getenv("SECRET_TOKEN"),
        "Content-Type":"application/json"}

    def addItemToExistingCollection(self,productId,collectionId):
        data = {
            "collect":{
                "product_id":productId,
                "collection_id":collectionId
            }
        }

        res = req.post("https://"+self.STORE_NAME+"/admin/api/2022-10/collects.json",headers=self.H,json=data)
        return res.json()

    def removeFromCollection(self,productId,collectionId):
        res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/collects.json?product_id="+str(productId)+"&collection_id="+str(collectionId),headers=self.H)
        response = res.json()
        collectId = response['collects'][0]['id']
        res = req.delete("https://"+self.STORE_NAME+"/admin/api/2022-10/collects/"+str(collectId)+".json",headers=self.H)
        
        return res.status_code

class RedirectPy :
    STORE_NAME = os.getenv("STORE_NAME")
    H = {"X-Shopify-Access-Token":os.getenv("SECRET_TOKEN"),
        "Content-Type":"application/json"}
    REDIRECT_LIST = []
    
    def getAllRedirects(self,URL=None):
        if URL is None :
            print("Recursive1")
            res = req.get("https://"+self.STORE_NAME+"/admin/api/2022-10/redirects.json?limit=250",headers=self.H)
            resdata = res.json()
            for item in resdata ["redirects"]:
                self.REDIRECT_LIST.append(item)
            if res.links != {}:
                url = res.links['next']['url']
                self.getAllRedirects(URL=url)
            

        elif URL is not None:
            print("Recursive2")
            res = req.get(URL,headers=self.H)
            resdata = res.json()
            for item in resdata ["redirects"]:
                self.REDIRECT_LIST.append(item)
            if res.links != {} and len(res.links) == 2:
                url = res.links['next']['url']
                self.getAllRedirects(URL=url)
                

    

            