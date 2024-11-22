import requests
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from difflib import get_close_matches


# Recipe retrieval and display
def get_recipe_details(url):
    try:
        # Attempt to fetch the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.MissingSchema:
        print("Invalid URL format.")
        return None
    except requests.exceptions.ConnectionError:
        print("Failed to establish a connection.")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    html_data = response.text
    soup = BeautifulSoup(html_data, "html.parser")
    title = soup.title.text.strip()

    ingredient_list = soup.find_all(class_="mm-recipes-structured-ingredients__list")
    ingredients = []
    for group in ingredient_list:
        for item in group:
            if item.text.strip() and not item.text.isspace():
                ingredients.append(item.text.strip())

    step_list = soup.select('.comp.mntl-sc-block.mntl-sc-block-startgroup.mntl-sc-block-group--LI .comp.mntl-sc-block.mntl-sc-block-html')
    steps = []
    for step in step_list:
        sentences = sent_tokenize(step.text.strip())
        steps.extend(sentences)

    return title, ingredients, steps


def show_ingredients(ingredients):
    print("\nHere are the ingredients:")
    for ingredient in ingredients:
        print(f"- {ingredient}")


def ordinal(n):
    n = int(n)
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def show_step(step_number, steps):
    if 1 <= step_number <= len(steps):
        print(f"The {ordinal(step_number)} step is: {steps[step_number - 1]}")
    else:
        print("Invalid step number.")


def extract_ingredient_quantity(user_question, ingredients):
   
    pattern = r'^\s*([\d/½¾⅓⅔]+(?:\s[\d/½¾⅓⅔]+)*)(?:\s?(ounce|cup|tablespoon|teaspoon|pound|clove|can|slice|pinch|dash|piece|quart|gallon|lb|oz|ml|l|g)?)\s+(.*)'

    
    question_words = ["how much", "how many", "quantity", "amount"]
    cleaned_question = user_question.lower()
    for phrase in question_words:
        cleaned_question = cleaned_question.replace(phrase, "")
    cleaned_question = cleaned_question.strip()

   
    close_match = get_close_matches(cleaned_question, [ing.lower() for ing in ingredients], n=1, cutoff=0.3)
    if close_match:
        matched_ingredient = close_match[0]
    else:
        print("No close match found for the ingredient in the question.")
        return False

   
    for ingredient in ingredients:
        if matched_ingredient in ingredient.lower():
            match = re.match(pattern, ingredient)
            if match:
                quantity = match.group(1).strip() if match.group(1) else "some"
                unit = match.group(2).strip() if match.group(2) else ""

                
                if unit:
                    print(f"You need {quantity} {unit}.")
                else:
                    print(f"You need {quantity}.")
                return True
            else:
                print("No quantity found in the matched ingredient.")
                return False

    
    print("Could not determine the quantity for the ingredient.")
    return False

def main():
    print("Hello, I'm a recipe chatbot!")
    print("You can fetch a recipe from Allrecipes, inquire about cooking techniques, or type 'quit' to exit.")
    title, ingredients, steps = None, None, None 

    while True:
        print("\nMain Menu:")
        print("[1] Fetch a recipe from Allrecipes")
        print("[2] Ask a cooking question")
        print("[3] Quit")
        print("Or type commands like 'show me a recipe', 'show me ingredients', 'next step', or 'how do I preheat the oven'.")

        user_input = input("What would you like to do? ").strip().lower()

      
        if "how do i" in user_input:
            handle_cooking_question(user_input)

       
        elif "ingredients" in user_input and ingredients:
            show_ingredients(ingredients)

        elif "steps" in user_input and steps:
            navigate_steps(steps)

        elif any(keyword in user_input for keyword in ["how much", "how many", "quantity", "amount"]) and ingredients:
            extract_ingredient_quantity(user_input, ingredients)

        
        elif "recipe" in user_input and any(word in user_input for word in ["show", "give", "fetch", "get"]):
            url = input("Please enter the URL of the Allrecipes recipe: ").strip()
            recipe_details = get_recipe_details(url)
            if recipe_details:
                title, ingredients, steps = recipe_details
                print(f"\nAlright. Let's start working with \"{title}\".")
                recipe_menu(title, ingredients, steps)
            else:
                print("Failed to fetch recipe. Please try again.")


        elif user_input == "1" or "fetch a recipe" in user_input:
            url = input("Please enter the URL of the Allrecipes recipe: ").strip()
            recipe_details = get_recipe_details(url)
            if recipe_details:
                title, ingredients, steps = recipe_details
                print(f"\nAlright. Let's start working with \"{title}\".")
                recipe_menu(title, ingredients, steps)
            else:
                print("Failed to fetch recipe. Please try again.")

        elif user_input == "2" or "ask a question" in user_input:
            question = input("Please enter your question: ").strip().lower()
            handle_cooking_question(question)

        elif user_input == "3" or "quit" in user_input or "exit" in user_input:
            print("Goodbye!")
            break

        else:
            print("I didn't understand that. Please try again or select an option from the menu.")

def recipe_menu(title, ingredients, steps):
    while True:
        print(f"\nRecipe Menu: {title}")
        print("[1] Show me the ingredients list")
        print("[2] Go over recipe steps")
        print("[3] Return to Main Menu")
        print("Or type commands like 'show me ingredients', 'show me steps', or 'how do I preheat the oven'.")

        user_input = input("What would you like to do? ").strip().lower()

        
        if handle_cooking_question(user_input):
            continue  

       
        if "ingredients" in user_input and ingredients:
            show_ingredients(ingredients)

        elif "steps" in user_input and steps:
            navigate_steps(steps, ingredients)  

        elif any(keyword in user_input for keyword in ["how much", "how many", "quantity", "amount"]) and ingredients:
            extract_ingredient_quantity(user_input, ingredients)

       
        elif user_input == "1":
            show_ingredients(ingredients)

        elif user_input == "2":
            navigate_steps(steps, ingredients)  

        elif user_input == "3" or "return" in user_input:
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid choice. Please try again.")


def navigate_steps(steps, ingredients):
    step_number = 1

   
    def ordinal_to_number(word):
        ordinal_map = {
            "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
            "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10
        }
        return ordinal_map.get(word.lower(), None)

    while True:
        show_step(step_number, steps)
        if step_number >= len(steps):
            print("You have completed all the steps!")
            break

        print("\nStep Navigation Options:")
        print("[N] Next step")
        print("[B] Previous step")
        print("[R] Repeat step")
        print("[G] Go to a specific step")
        print("[M] Return to Recipe Menu")
        print("Or type commands like 'next step', 'repeat step', 'how much cheese', or 'show me the 4th step'.")

        user_input = input("Your choice: ").strip().lower()

     
        if handle_cooking_question(user_input):
            continue

        if any(keyword in user_input for keyword in ["how much", "how many", "quantity", "amount"]):
            if extract_ingredient_quantity(user_input, ingredients):
                continue 
            else:
                print("I couldn't find that ingredient. Please try again.")
                continue

       
        if "ingredients" in user_input:
            show_ingredients(ingredients)
            print("\nReturning to Step Navigation...")
            continue


        if "step" in user_input:
            match = re.search(r"(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\d+)", user_input)
            if match:
                step_input = match.group(1)
                target_step = ordinal_to_number(step_input) if not step_input.isdigit() else int(step_input)
                if target_step and 1 <= target_step <= len(steps):
                    step_number = target_step
                    continue
                else:
                    print(f"Invalid step number. There are only {len(steps)} steps.")
                    continue

       
        if user_input in ["n", "next", "next step"]:
            step_number += 1

        elif user_input in ["b", "back", "previous", "previous step"]:
            if step_number > 1:
                step_number -= 1
            else:
                print("You are already at the first step.")

        elif user_input in ["r", "repeat", "repeat step"]:
            continue

        elif user_input in ["g", "goto", "go to"]:
            target = input("Enter the step number you want to go to: ").strip()
            if target.isdigit() and 1 <= int(target) <= len(steps):
                step_number = int(target)
            else:
                print("Invalid step number.")

        elif user_input in ["m", "menu", "return to menu"]:
            print("Returning to Recipe Menu...")
            break

        else:
            print("Invalid choice. Please select a valid option.")


def handle_cooking_question(user_input):
  
    if "how do i" in user_input:
        technique = user_input.split("how do i")[-1].strip()
    elif "how to" in user_input:
        technique = user_input.split("how to")[-1].strip()
   
    elif "what is" in user_input:
        technique = user_input.split("what is")[-1].strip()
    else:
        return False  

   
    technique_query = "+".join(technique.split())
    technique_string = " ".join(technique.split())
    print(f"You can learn more about {technique_string} here: https://www.google.com/search?q={technique_query}")
    return True  



if __name__ == "__main__":
    main()
