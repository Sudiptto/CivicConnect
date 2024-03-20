# PURPOSE OF THIS PYTHON FILE

# this file contains all the prompts for each topic (these are for sending the email meaning they will not have HTML/CSS within them and sent to mailto) 
envProtec = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
freePalestine = """The American people have continued in support of the citizens of Gaza with calls for a ceasefire. Our cries have fallen on deaf ears as Congress has maintained pumping funds and weapons into the Israeli war machine. The actions taken by Hamas on October 7th were deplorable and impossible to condone. However, the citizens of the United States cannot and will not disregard the deaths of over 25,000 Gazan citizens, injuries to over 63,000, and the displacement of over 1.7 million more. There are less than 10 functioning hospitals left in the region as violence continues and disease spreads. Only 15 bakeries remain to feed millions. Water, fuel, and other vital resources are restricted from reaching those who most need them. Communication is shut down for days at a time, preventing Gazans from communicating in their time of need. Over $300 billion of American’s tax dollars has been sent to fund over 15% of Israel’s defense budget. That budget is not spent solely for defense, but for the slaughter and genocide of young Gazan children. The United States has tied itself in an unhealthy relationship with the state of Israel that looks to jeopardize not only Gaza but the Middle East and American relations with the rest of the world. In January of 2024, the International Court of Justice demanded Israel take all measures within its power to prevent the, “killings, serious physical or mental harm, the deliberate infliction of conditions of life calculated to bring about the physical destruction of the population in whole or in part, and the imposition of measures intended to prevent births;” For months the Israeli military has ignored those demands.Hamas will not crumble quickly, and the number of innocent people paying the price for a crime they did not commit is rising. Commerce, manufacturing, and agriculture will cease to exist if violence persists. The injury to critical aspects of civilian life, the displacement, the depopulation—will continually worsen as the United States promotes this genocide. The American people demand our Congressional representatives call for an immediate ceasefire. We demand our tax dollars no longer be spent propping up violent regimes. We demand aid and relief be brought to Gaza immediately. We demand an America founded and built upon representation and democracy be returned to its people. We demand an end to the war in Gaza."""
povertyPrompt = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
racialRedlining = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."

# function for all the PROMPTS FROM /causes
def getAllPrompts(name, represenatives):
    # turn the represenative name from a list to a string
    allRepName = ""
    for names in represenatives:
        # all names from 1 - n - 1 (second to last)
        if names != represenatives[-1]:
            allRepName += ("<b> " +names + "</b>" + ", ")
        # last name
        else:
            allRepName += ("<b> " + names + "</b>")
    # ALL PROMPTS
    environmental_protection = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    free_palestine =  f"""<p>The American people have continued in support of the citizens of Gaza with calls for a ceasefire. Our cries have fallen on deaf ears as Congress has maintained pumping funds and weapons into the Israeli war machine. The actions taken by Hamas on October 7th were deplorable and impossible to condone. However, the citizens of the United States cannot and will not disregard the deaths of over 25,000 Gazan citizens, injuries to over 63,000, and the displacement of over 1.7 million more.</p><p>There are less than 10 functioning hospitals left in the region as violence continues and disease spreads. Only 15 bakeries remain to feed millions.Water, fuel, and other vital resources are restricted from reaching those who most need them. Communication is shut down for days at a time, preventing Gazans from communicating in their time of need.</p><p>Over $300 billion of American’s tax dollars has been sent to fund over 15% of Israel’s defense budget. That budget is not spent solely for defense, but for the slaughter and genocide of young Gazan children. The United States has tied itself in an unhealthy relationship with the state of Israel that looks to jeopardize not only Gaza but the Middle East and American relations with the rest of the world.</p><p>In January of 2024, the International Court of Justice demanded Israel take all measures within its power to prevent the, “killings, serious physical or mental harm, the deliberate infliction of conditions of life calculated to bring about the physical destruction of the population in whole or in part, and the imposition of measures intended to prevent births;” For months the Israeli military has ignored those demands.</p><p>Hamas will not crumble quickly, and the number of innocent people paying the price for a crime they did not commit is rising. Commerce, manufacturing, and agriculture will cease to exist if violence persists. The injury to critical aspects of civilian life, the displacement, the depopulation—will continually worsen as the United States promotes this genocide.</p><p>The American people demand our Congressional representatives call for an immediate ceasefire. We demand our tax dollars no longer be spent propping up violent regimes. We demand aid and relief be brought to Gaza immediately. We demand an America founded and built upon representation and democracy be returned to its people. We demand an end to the war in Gaza.</p><p>Sincerely,<br>{name}</p>"""

    racial_redlining = """Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."""
    poverty = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    

    return [environmental_protection, free_palestine, racial_redlining, poverty]

# prompt function for the /email page 
def subjectPrompt(prompt,name,represenative):
    message = []
    # get the LIST of prompts
    allPrompts = getAllPrompts(name, represenative)
    if prompt == "Enviornmental Protection":
        #message = allPrompts[0]
        message.append(allPrompts[0])
        message.append(envProtec)
    elif prompt == "Free Palestine":
        #message = allPrompts[1]
        message.append(allPrompts[1])
        message.append(freePalestine)
    elif prompt == "Poverty":
        #message = allPrompts[2]
        message.append(allPrompts[2])
        message.append(povertyPrompt)
    elif prompt == "Racial Redlining":
        #message = allPrompts[3]
        message.append(allPrompts[3])
        message.append(racialRedlining)

    return message
    
    