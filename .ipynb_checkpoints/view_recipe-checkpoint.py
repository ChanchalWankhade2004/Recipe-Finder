from flask import Flask,render_template,request
import requests
from urllib.parse import unquote

#create the flask app
app=Flask(__name__)

#our API key
API_KEY='2331be72b15c48feb5bfb94269ea00dd'

#Define the root for the home button
@app.route('/home',methods=['GET'])
def home():
    return render_template('index.html',recipe=[],search_query='')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        #if a form is submitted
        query=request.form.get('serach_query','') 
        #perform a search for recipes with the given query
        recipes=search_recipes(query)
        #render the main page with the search results and the serach query
        return render_template('index.html',recipes=recipes,search_query=query)

    #if it's a GET request or no form submitted
    search_query=request.args.get('search_query','')
    decoded_search_query=unquote(search_query)
    #perform a search for recipes with the decoded search query
    recipes=search_recipes(decoded_search_query)
    #render the main page
    return render_template('index.html',recipes=recipes,search_query=decoded_search)

#Function to search for recipes based on the provided query
def search_recipes(quersy):
    url=f'https://api.spoonacular.com/recipes/complexSearch'
    params={
        'apiKey':API_KEY,
        'query':query,
        'number':10,
        'instructionsRequired':True,
        'addRecipeInformation':True,
        'fillIngredients':True,
    }
    
    #Send a GET request to the spoonacular API with the query parameters
    response=requests.get(url,params=params)
    #if the API call is successful
    if response.status_code==200:
        #parse the API response as JSON data
        data=response.json()
        #Return the list of recipe results
        return data['results']
    #If the API call is not successful
    return []

#Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipes_id>')
def view_recipe(recipe_id):
   #Get the search query from the url query params
   search_query=request.args.get('search_query','')
   #Build the url to get info about the specific recipe ID from Spoonacular API
   url=f'https://api.spoonacular.com/recipes/{recipes_id}/information'
   params={
      'apiKey':API_KEY
   }
   #Send a GET request to the spoonacular API to get the recipe info
   response=requests.get(url,params=params)
   #if the API call is successful
   if response.status_code==200:
      recipe=response.json()
      return render_template('view_recipe.html',recipe=recipe,search_query=search_query)
   return "Recipe not found",404

#Run the app in debug mode if executed directly
if __name__ == '__main__':
   app.run(debug=True)
