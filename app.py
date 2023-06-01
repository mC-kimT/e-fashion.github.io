from fastai.vision.all import *
from flask import Flask, request, render_template, redirect
import os
import json
import pathlib


app = Flask(__name__)

upload_folder = os.path.join(os.getcwd() , 'static/upload')

app.config['UPLOAD'] = upload_folder


def classification(image):
    cnn = load_learner('models/fashion_classification.pkl')

    predicted_category = cnn.predict(item = image)

    return predicted_category[0]



@app.route('/', methods=['GET'])
def index_view():
    return render_template('./Home.html')



# Allow files with extension png, jpg and jpeg
ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT



def simProduct(cnn_prediction, gender, Fdataset):
    sim_products = []

    for data in Fdataset:
        if data['Category'].lower() == cnn_prediction.lower() and data['Gender'].lower() == gender.lower():
            sim_products.append(data)
    return sim_products
    
    
mens= ['k_m_jacket', 'k_m_jeans', 'k_m_pants', 'k_m_shorts', 'k_m_t-shirt', 'k_m_belt', 'm_jackets', 'm_jeans', 'm_pants', 'm_shorts', 'm_t-shirt']
womans= ['k_w_dress', 'k_w_jeans', 'k_w_pants', 'k_w_shirt', 'k_w_short', 'k_w_skirt', 'w_belt', 'w_dress', 'w_jeans', 'w_pants', 'w_shorts', 'w_skirts', '']    
        


@app.route('/',methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # gender = request.form['gender']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join('static/upload', filename)
            file.save(file_path)
            img = classification(file_path)

            if( img.lower() == "k_m_jacket"):
                category = "Kids Jacket"
                rand=''
            elif(img.lower() == "k_m_jeans"):
                category = "Kids Jeans"
                rand=''
            elif(img.lower() == "k_m_pants"):
                category = "Kids Pants"
                rand=''
            elif(img.lower() == "k_m_shorts"):
                category = "Kids Shorts"
                rand=''
            elif(img.lower() == "k_m_t-shirt"):
                category = "Kids t-shirts"
                rand=''
            elif(img.lower() == "k_m_belt"):
                category = "Kids Belt"
                rand=''
            elif(img.lower() == "m_jackets"):
                category = "Jackets"
                rand=''
            elif(img.lower() == "m_jeans"):
                category = "Jeans"
                rand=''
            elif(img.lower() == "m_pants"):
                category = "Pants"
                rand=''
            elif(img.lower() == "m_shorts"):
                category = "Shorts"
                rand=''
            elif(img.lower() == "m_t-shirt"):
                category = "t-shirts"
                rand=''
            elif(img.lower() == "k_w_dress"):
                category = "Dress for kids"
                rand=''
            elif(img.lower() == "k_w_jeans"):
                category = "Jeans for kids"
                rand=''
            elif(img.lower() == "k_w_pants"):
                category = "Pants for kids"
                rand=''
            elif(img.lower() == "k_w_shirt"):
                category = "Shirts for kids"
                rand=''
            elif(img.lower() == "k_w_short"):
                category = "Shorts for kids"
                rand=''
            elif(img.lower() == "k_w_skirt"):
                category = "Skirt for kids"
                rand=''
            elif(img.lower() == "w_belt"):
                category = "Belt"
                rand=''
            elif(img.lower() == "w_dress"):
                category = "Dress"
                rand=''
            elif(img.lower() == "w_jeans"):
                category = "Jeans"
                rand=''
            elif(img.lower() == "w_pants"):
                category = "Pants"
                rand=''
            elif(img.lower() == "w_shorts"):
                category = "Shorts"
                rand=''
            elif(img.lower() == "w_skirts"):
                category = "Skirts"
                rand=''
            
            else: 
                category = "Random Image"
                rand=  'Not in fashion category please insert another image.'

            dataset_path = "models/Dataset.json"
            dataset = json.load(open(dataset_path))

            
        gender = 'men'
        for pcategory in mens: 
            if (img.lower() == pcategory.lower()):
                    gender='men'
        
        for pcategory in womans:
            if(img.lower() == pcategory.lower()):
                gender = 'woman'

        sim_products = simProduct(img.lower(), gender,  dataset)

        flipkart = []
        amazon = []
        walmart = []
        shein = []

        for products in sim_products:
            if products['Store'].lower() == 'amazon':
                amazon.append(products)
            if products['Store'].lower() == 'flipkart':
                flipkart.append(products)
            if products['Store'].lower() == 'walmart':
                walmart.append(products)
            if products['Store'].lower() == 'shein':
                shein.append(products)


        
        return render_template('cnn_result.html', predict=category, user_image=file_path, rdm = rand, Amazon = amazon, Flipkart=flipkart, Walmart=walmart, SHEIN=shein)
    
    else: 
        return "Unable to read the file. Please check file extension"
    


# open  recommendation file 
file = open('models/recommendations.pkl', 'rb')
recommendation_file = pickle.load(file)



@app.route("/forward/", methods=['POST'])
def display_recommendation():
    dataset_path = "models/Dataset.json"
    dataset = json.load(open(dataset_path))
    
    
    if request.method == 'POST':
        recommendations = []

        if 'fname' in request.form:
            Name = request.form['fname']

            # get the recommendation
            for Data in recommendation_file:
                if Data[0] == Name:
                    recommendations = Data[1]
                else: "Name dosent match anything."

            # get the img of click
            for Data in dataset:
                if Data['Name'] == Name:
                    img_src=Data['Image']
                    p_link=Data['Link']
                    p_store=Data['Store']
                    p_price=Data['Price']

    return render_template("display_items.html", display=recommendations, pName=Name, image=img_src, link=p_link, store=p_store, price=p_price)



@app.route('/filter/',methods=['POST', 'GET'])
def filter_store():
    prod = [] 

    if request.method == 'POST':
        store = request.form['page']
        products = request.form['f_product']
        if store.lower() == "flipkart":
            for product in products:
                if product['Store'].lower() == "flipkart":
                    prod.append(product)
        elif store.lower()=="amazon":
           for product in products:
                if product['Store'].lower() == "amazon":
                    prod.append(product)
        else: 
            for product in products:
                prod.append(product)
    
    return render_template("cnn_result.html", products= prod)



if __name__ == "__main__":
    app.run()
