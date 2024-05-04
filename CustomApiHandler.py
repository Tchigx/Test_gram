from flask import Flask, jsonify, request
import json 
import requests
import time 

app = Flask(__name__)

@app.route('/GetAssetBySearch', methods=['GET'])
def handle_endpoint():
    # Access query parameters
    param1 = request.args.get('Category', default=None, type=str)
    param2 = request.args.get('CreatorID', default=None, type=str)
   # param3 = request.args.get('param2', default=None, type=str)
    AllData=[]
    page_number=1
    while True:
        FinalStr=f"https://search.roblox.com/catalog/json?CreatorID={param2}&SortType=3&PageNumber={page_number}&Category={param1}"
        page=requests.get(FinalStr)
        StatusCode=page.status_code

        if StatusCode== 429:
            break
    
        page=page.json()
        if not page:

            break
        
        AllData.extend(page)
        time.sleep(0.5)
        page_number+=1
    # Use the query parameters in your response or processing
    
    return jsonify(AllData), StatusCode
    

@app.route('/GetAssetByInv', methods=['GET'])
def handle_endpoint2():
    # Access query parameters
    userId = request.args.get('userId', default=None, type=str)
    assetTypeId = request.args.get('assetTypeId', default=None, type=str)
    limit=request.args.get('limit', default=None, type=str)
    MySecondTime=request.args.get('MySecondTime', default=None, type=str)
    ChosenAsset = []
    cursor = ''
    
    if limit=="All":
        limit=str(100)

    while True:
        url=f"https://inventory.roblox.com/v2/users/{userId}/inventory/{assetTypeId}?limit={limit}&sortOrder=Desc&cursor={cursor}"
        response = requests.get(url)
        data = response.json()
        ChosenAsset.extend(data['data'])
        cursor = data['nextPageCursor']
        if not cursor or MySecondTime=="True":
            break

        if int(limit)!=100:
            #got the number of assets we wanted
            break
         
   
    return jsonify(ChosenAsset), response.status_code

@app.errorhandler(404)
def page_not_found(e):
    # your error handling logic here
    return 'Message from seismic that something went wrong....', 404  

if __name__ == '__main__':
    app.run(debug=True)
