text = 'how do I preheat the oven'
technique = text.split("how do I")[-1].strip()

print(technique)