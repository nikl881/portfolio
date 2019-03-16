import os
import json
from flask import Flask, render_template, request, flash

app = Flask (__name__)
app.secret_key = 'some_secret'

@app.route('/') 
def index():
    return render_template("index.html")
    
@app.route('/') 
def help():
    return render_template("help.html")
    
    
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
    
        
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks, {}, I have recieved your message!".format(request.form["name"]))
    return render_template("contact.html", page_title="Contact")
        
        

@app.route('/recipes')
def recipes():
        return render_template("recipes.html", page_title="Recipes")  
        
@app.route('/detailpage')
def detailpage():
        return render_template("detailpage.html", page_title="Detailpage")                  


@app.route('/instruction')
def instruction():
        return render_template("instruction.html", page_title="Instruction")   

@app.route('/addrecipes')
def addrecipes():
        return render_template("addrecipes.html", page_title="Add recipes")            

@app.route('/recipesfollow')
def recipesfollow():
        return render_template("recipesfollow.html", page_title="Second page")             
        
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
    
    
    