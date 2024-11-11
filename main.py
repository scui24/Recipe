import requests
from bs4 import BeautifulSoup

# Recipe retrieval and display
def get_recipe_details(url):
    response = requests.get(url)
    html_data = response.text
    soup = BeautifulSoup(html_data, "html.parser")
    title = soup.title.text

    ingredient_list = soup.find_all(class_="mm-recipes-structured-ingredients__list")
    ingredients = []
    for _ in ingredient_list:
        for __ in _:
            if __.text != "" and __.text.isspace() == False:
                ingredients.append(__.text.strip()) 

    step_list = soup.select('.comp.mm-recipes-steps.mntl-block .comp.mntl-sc-block.mntl-sc-block-html')
    steps = []  
    for i in range(len(step_list)):
        steps.append(step_list[i].text.strip())
    
    return title, ingredients, steps

def show_ingredients(ingredients):
    print("Here are the ingredients:")
    for ingredient in ingredients:
        print(f"- {ingredient}")

def show_step(step_number, steps):
    if step_number <= len(steps):
        print(f"The {step_number} step is: {steps[step_number-1]}")
    else:
        print("Invalid step.")

# Navigation utterances
def navigate_steps(step_number, steps, command):
    if command == "next" or command == "continue":
        step_number += 1
    elif command == "back":
        step_number = max(0, step_number - 1)
    elif command == "repeat":
        pass  # No change, repeats current step
    elif "take me to" in command:
        try:
            target_step = int(command.split()[-2]) - 1
            if 0 <= target_step < len(steps):
                step_number = target_step
        except ValueError:
            print("Please specify a valid step number.")
    else:
        print("Unknown command.")
        
    if step_number > len(steps):
        print("No further steps.")
    return step_number

# Asking about the parameters of the current step
def ask_step_parameters(step, ingredients):
    if "temperature" in step.lower():
        print("")
    elif any(ingredient.lower() in step.lower() for ingredient in ingredients):
        ingredient = next(ing for ing in ingredients if ing.lower() in step.lower())
        print(f"For {ingredient}, you need to refer to the quantity in the ingredients list.")
    elif "how long" in step.lower():
        print("")
    elif "done" in step.lower():
        print("")
    else:
        print("No specific parameter found.")

# Main
print("Hello! I'm here to walk you through any recipe you want.")
url = input("Please specify a URL: ")
title, ingredients, steps = get_recipe_details(url)
print(f"Alright. Let's start working with \"{title}\".")

step_number = 1
positive_responses = ["yes", "y", "yeah", "yep", "sure", "of course", "affirmative", "indeed", "absolutely", "okay", "ok", "yup", "certainly", "definitely"]
negative_responses = ["no", "n", "nope", "nah", "never", "not really", "negative", "I don't think so", "absolutely not"]

while True:
    print("What would you like to do?")
    print("[1] Show me the ingredients list")
    print("[2] Go over recipe steps")
    print("[3] Exit")

    choice = input("Your choice: ")
    flag = True

    if choice == "1":
        show_ingredients(ingredients) #1
    elif choice == "2":
        if step_number < len(steps):
            show_step(step_number, steps)

            while flag:
                action = input(f"Should I continue to step {step_number + 1}?\n")
                if "What is" in action: #4
                    tool = action.split("What is")[-1].split()
                    print(f"Here's some information about {tool}. You can check this link for more details: https://www.google.com/search?q=what+is+{tool}")
                elif "How do I" in action: #5
                    technique = action.split("How do I")[-1].split()
                    print(f"You can learn more about how to {technique} here: https://www.youtube.com/results?search_query=how+to+{technique}")
                elif "How do I do that" in action: #6
                    if step_number == 1:
                        print("This is the first step, please specify your question.")
                    else:
                        last_action = steps[step_number - 1]
                        print(f"Based on what we've discussed, here's what you should do: {last_action}.")
                elif any(response in action.lower() for response in positive_responses):
                    step_number += 1
                    show_step(step_number, steps)
                elif any(response in action.lower() for response in negative_responses):
                    flag = False
                else:
                    print("I'm not sure how to help with that. Could you clarify? (Start your answer with a capital letter)")

                if step_number >= len(steps):
                    print("You have completed all the steps!")
                    break
    elif choice == "3":
        print("Goodbye! Happy cooking :)")
        break
    else:
        print("Invalid choice. Please select a valid option.")



