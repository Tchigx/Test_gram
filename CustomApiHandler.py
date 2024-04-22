from flask import Flask, jsonify, request
import json 
import requests

app = Flask(__name__)

@app.route('/GetAssetBySearch', methods=['GET'])
def handle_endpoint():
    # Access query parameters
    param1 = request.args.get('TypeAsset', default=None, type=str)
    param2 = request.args.get('CreatorID', default=None, type=str)
   # param3 = request.args.get('param2', default=None, type=str)

    FinalStr=""
    if param1=="Decal":
        FinalStr=f"https://search.roblox.com/catalog/json?CreatorID={param2}&SortType=3&PageNumber=1&Category=8"
    elif param1=="Audio":
        FinalStr=f"https://search.roblox.com/catalog/json?CreatorID={param2}&SortType=3&PageNumber=1&Category=9"
    

    page=requests.get(FinalStr)
    page=page.json()
    print(page)
    # Use the query parameters in your response or processing
    return jsonify(page), 200
    

@app.errorhandler(404)
def page_not_found(e):
    # your error handling logic here
    return 'Page Not Found xd xd xd', 404  

if __name__ == '__main__':
    app.run(debug=True)
