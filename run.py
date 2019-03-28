import os
import json
from flask import Flask, render_template, request, flash, redirect, request, url_for, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask (__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = 'mongodb+srv://root:pwvanr00t1@mycluster-yaqc7.mongodb.net/recipe_book?retryWrites=true'

mongo = PyMongo(app)


### routing the index page ###


@app.route('/') 
def index():
    
    return render_template("index.html", page_title="Home", recipes=mongo.db.recipes.find())
    
    
### routing the about page ###    

@app.route('/about')
def about():
    data = [1]
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        return render_template("about.html", page_title="About", company=data)
        
@app.route('/about/<member_name>')
def about_member(member_name):
    member = {}
    
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
        return render_template("member.html", member=member)
  
  

### show recipe on detailpage (single recipe page)  ###     
        
@app.route('/')
@app.route('/detailpage')
def detailpage():
    return render_template("detailpage.html", recipes=mongo.db.recipes.find())   
    
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("detailpage.html", recipes=mongo.db.recipes.find())
    
    
    
### show all recipes and filter categories on recipes.html page  ###   


@app.route('/recipes')
def recipes():
        return render_template("recipes.html", page_title="Recipes", recipes=mongo.db.recipes.find())
    
              
### Follow page (show all recipes) ###                  
              
@app.route('/recipesfollow')
def recipesfollow():
        return render_template("recipesfollow.html", page_title="Second recipe page")               
              



### add a new recipe on addrecipes.html ###

@app.route('/addrecipes')
def addrecipes():
        return render_template("addrecipes.html", page_title="Add recipes")
        
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe = mongo.db.recipes
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))    
            

###  edit recipe ###

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes =  mongo.db.recipes.find()
    return render_template('editrecipe.html', recipe=the_recipe,
    recipes=all_recipes)
 
### update recipe ###

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
       'recipe_name':request.form.get('recipe_name'),
        'recipe_description':request.form.get('recipe_description'),
        'author_name': request.form.get('author_name'),
        'cuisine_region': request.form.get('cuisine_region'),
        'difficulty':request.form.get('difficulty'),
        'allergens':request.form.get('allergens'),
        'ingredients':request.form.get('ingredients'),
        'cooking_time':request.form.get('cooking_time'),
        'dish_type':request.form.get('dish_type'),
      
    })
    return redirect(url_for('get_recipes'))


  
### routing for the contact page ###         
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks, {}, I have recieved your message!".format(request.form["name"]))
    return render_template("contact.html", page_title="Contact")
    
  
### run location ### 
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

