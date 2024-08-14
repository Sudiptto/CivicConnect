import os
import json

# function to load JSON data
def load_prompts():
    with open(os.path.join('UpdatePrompt', 'prompts.json'), 'r', encoding='utf-8') as file:
        return json.load(file)
    
allPrompts = load_prompts()

# function for all the prompts from /causes (INCLUDES HTML)
def getAllPrompts(name):
    allPromptsDict = {}
    # ADD THIS TO END: <p>Sincerely,<br>{name}</p>
    for prompt in allPrompts:
        allPromptsDict[prompt] = (allPrompts[prompt]['htmlText'] + f' <p>Sincerely, <br>{name}</p>')
        
    return allPromptsDict

# function for all the prompts from /email (NO HTML) -> so loop through 
def subjectPrompt(promptName, name, represenative, zip):
    # the first message is the prompt with the HTML (send through us), second is the prompt without the HTML (for emails)
    message = []
    
    sendThroughUsPrompt = allPrompts[promptName]['htmlText']
    sendThroughYou = allPrompts[promptName]['emailText'] + " Sincerely, " + name + " ZipCode: " + zip

    message.append(sendThroughUsPrompt)
    message.append(sendThroughYou)

    return message


