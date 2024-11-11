import requests
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize

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

    step_list = soup.select('.comp.mntl-sc-block.mntl-sc-block-startgroup.mntl-sc-block-group--LI .comp.mntl-sc-block.mntl-sc-block-html')
    steps = []  
    for i in range(len(step_list)):
        sentences = sent_tokenize(step_list[i].text.strip())
        steps.extend(sentences)
    
    return title, ingredients, steps

def show_ingredients(ingredients):
    print("Here are the ingredients:")
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
    if step_number <= len(steps):
        print(f"The {ordinal(step_number)} step is: {steps[step_number-1]}")
    else:
        print("Invalid step.")

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
next_patterns = re.compile(r"\b(next|forward|continue|move ahead|advance|go on)\b")
back_patterns = re.compile(r"\b(back|previous|go back|move back|rewind|return)\b")
repeat_patterns = re.compile(r"\b(repeat|again|one more time|redo|say it again)\b")
first_patterns = re.compile(r"\b(first|beginning|start|initial|1st)\b")
last_patterns = re.compile(r"\b(last|final|end|conclude|finish)\b")
nth_step_pattern = re.compile(r"\btake me to (\d+)[a-z]{0,2} step\b|\bgo to step (\d+)\b")

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
                action = input(f"Should I continue to the {ordinal(step_number + 1)} step?\n")
                if next_patterns.search(action): #2
                    step_number += 1
                    show_step(step_number, steps)
                elif back_patterns.search(action):
                    if step_number == 1:
                        print("Sorry, this is the first step. You can't go to the previous step.")
                    else:
                        print("Happy to help! Let's go back.")
                        step_number -= 1
                        show_step(step_number, steps)
                elif repeat_patterns.search(action):
                    print("No problem! Let me repeat the step for you.")
                    show_step(step_number, steps)
                elif first_patterns.search(action):
                    print("Sure. This is the first step:")
                    step_number = 1
                    show_step(step_number, steps)
                elif last_patterns.search(action):
                    print("No problem at all. Let's go to the last step.")
                    step_number = len(steps)
                    show_step(step_number, steps)
                elif nth_step_pattern.search(action):
                    match = nth_step_pattern.search(action)
                    target_step = int(match.group(1) or match.group(2))
                    if 1 <= target_step <= len(steps):
                        step_number = target_step
                        print(f"Glad I could help! This is the {ordinal(step_number)} step:")
                        show_step(step_number, steps)
                    else:
                        print(f"Sorry, there is no step {target_step}. There are only {len(steps)} steps in this recipe.")
                elif "What is" in action: #4
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



