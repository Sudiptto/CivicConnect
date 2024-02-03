# PURPOSE OF THIS PYTHON FILE

# this file contains all the prompts for each topic (these are for sending the email meaning they will have HTML/CSS within them and sent to mailto) 

environmental_protection = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
free_palestine = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
racial_redlining = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
poverty = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."


# function for all the PROMPTS FROM SUBJECT 

def subjectPrompt(prompt):
    if prompt == "Enviornmental Protection":
        txt = "Filler text (Enviornmental): Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        return txt
    elif prompt == "Free Palestine":
        txt = "Filler text (Free Palestine): Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        return txt
    elif prompt == "Poverty":
        txt = "Filler text (Poverty): Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        return txt
    elif prompt == "Racial Redlining":
        txt = "Filler text (Racial Redlining): Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        return txt
    
    # ADD WHEN MORE VALUES COME

