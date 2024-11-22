# CS337 Project 2 -- Recipe Parsing & User-Bot Conversational Interaction
# Group 3- Recipe Parsing & Conversational Interaction Project

This project uses a variety of web scraping, natural language processing (NLP), and text-processing libraries/packages for designing and building a system that (i) parses online recipes into a useful data representation and (ii) features a (basic) conversational interface for user interaction.

The following libraries/packages are included in the project:

## Libraries/Packages Overview
1. **requests**: The Requests is a Python library that allows you to send HTTP/1.1 requests extremely easily.
   
2. **re**: re is a Python built-in package, which can be used to work with Regular Expressions.
   
3. **bs4**: Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
      
4. **NLTK**: The Natural Language Toolkit (NLTK) is a comprehensive library for working with human language data (text) in Python, including text classification, tokenization, stemming, tagging, parsing, and more.
    
5. **difflib**: The difflib is the Python standard library that provides classes and functions for comparing sequences. It can be used for example, for comparing files, and can produce information about file differences in various formats, including HTML and context and unified diffs.


## Setup Instructions

Please download and install above required libraries/packages in Python.

## Group 3 Github Repository
 You can access our group's project-2 Github repository through following address: 
 https://github.com/scui24/Recipe.git
 

## Steps to run the the python file in the submission folder

Step 1:Run the python file "recipe.py", to make preparation that you can retrive any recipe you want from the recipe website: https://www.allrecipes.com

Step 2: Interact with chatbot to parse recipe ingredients, tools, methods, or steps.

**Test questions for six question answering goals:**

1.**Recipe retrieval and display:**
  <p>you can select option [1] from Main Menu:[1] Fetch a recipe from Allrecipes;</p>
  <p>OR type "show me a recipe".</p>
  And then input any recipe url link from allrecipes.com: https://www.allrecipes.com

2.**Navigation utterances:**
  <p>type "next", "next step", "repeat step", "repeat", "previous step", "previous", "show me the n-th step", "take me to the n-th step", "go to n-th step"; "n-th step", "back";</p>
  <p>OR select options from Step Navigation Options:</p>
     [N] Next step
     [B] Previous step
     [R] Repeat step
     [G] Go to a specific step
     [M] Return to Recipe Menu

3.**Asking about the parameters of the current step:**
  <p>type "how many/much [ingredient name], "how many/much [ingredient name] do i need?", "the amount of [ingredient name]", "the quantity of [ingredient name]".</p>

4.**Simple "what is" questions:**
  <p>type "what is a [tool being mentioned]?"</p>

5.**Specific "how to" questions:**
  <p>type "how to [specific technique]?"</p>
    
6.**Vague "how to" questions:**
  <p>type " how do i [specific technique/step]?"</p>









