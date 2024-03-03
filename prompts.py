# PURPOSE OF THIS PYTHON FILE

# this file contains all the prompts for each topic (these are for sending the email meaning they will have HTML/CSS within them and sent to mailto) 


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
    free_palestine = f"""<div style='color: black;'><p>Dear {allRepName}</p> <p>The American people have continued to cry out in support of the citizens of Gaza with calls for a ceasefire. 65% of Americans say war between Israel and Gaza is important to them personally. Our screams have fallen on deaf ears as our Congress has continued to pump funds and weapons into the Israeli war machine. The actions taken by <letter>Hamas</letter> on October 7th were deplorable and impossible to condone. However, the citizens of the United States cannot and will not condone the deaths of over 25,000 Gazan citizens, injuries to over 63,000, and the displacement of over 1.7 million more. There are less than 10 functioning hospitals left in the region as disease spreads and violence continues. Only 15 remaining bakeries to feed millions of fleeing people. Water, fuel, and other vital resources are limited and restricted by Israel from reaching those that need it most. Communication is shut down for days at a time, preventing Gazans from communicating internally and with the outside world in their time of need.</p> <p>Over $300 billion in foreign aid has been sent to Israel over its short history and Congress continues to increase that number as time goes on. American tax dollars are spent to fund over 15% of Israel’s defense budget. A budget that is spent not remotely for defense but for the slaughter and genocide of young Gazan children, the elderly, and everyone in between. We fund every aspect of their military that could be used domestically or in a campaign to foster diplomatic relations between the two parties.</p> <p>The United States has tied themselves in an unhealthy relationship with the state of Israel that looks to jeopardize not only Gaza but the Middle East and American relations with the rest of the world. In January of 2024, the International Court of Justice demanded Israel take all measures within its power to prevent the, “killings, serious physical or mental harm, the deliberate infliction of conditions of life calculated to bring about the physical destruction of the population in whole or in part, and the imposition of measures intended to prevent births;” For months we have seen the Israeli military do exactly the opposite of that listed as obligations under the Genocide Convention. Nations around the world have stood in awe as the United States continually vetoes bills calling for an immediate ceasefire. We stand alone in opposition in a world begging for peace. Americans continually stand in a state of shock as our glorious country loses its pedigree on the world stage and our reputation of democracy gets ripped out of clutches by our own hands.</p> <p> Hamas will not be destroyed quickly. The number of innocent people who pay the price for a crime they did not commit will rise. As conflict persists, it will expand and escalate as it has for months. Neighboring nations have economically suffered consequences and will continue to suffer as war rages on. Gaza will be leveled as housing and infrastructure gets targeted by mortar fire. Commerce, manufacturing, and agriculture are almost nonexistent in the territory and will be completely wiped out if violence persists. The injury to critical aspects of civilian life, the displacement, the depopulation—all look to get worse as the United States promotes an active genocide. Gaza is and will be dependent on humanitarian aid for decades if a ceasefire is not called for immediately. The City upon a Hill is no more as we protect a barbaric slaughtering of our fellow men, women, and children. We are no exceptional liberator of the free world, but an enabler of malice and suffering. The American people demand our Congressional representatives call for an immediate ceasefire. We demand our tax dollars no longer be spent propping up violent regimes. We demand aid and relief be brought to Gaza immediately. We demand an America founded and built upon representation and democracy be returned to its people. We demand an end to the war in Gaza.</p><p><signature>Sincerely, <br> {name}</signature></p></div>"""


    racial_redlining = """Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."""
    poverty = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    

    return [environmental_protection, free_palestine, racial_redlining, poverty]

# prompt function for the /email page 
def subjectPrompt(prompt,name,represenative):
    message = ""
    # get the LIST of prompts
    allPrompts = getAllPrompts(name, represenative)
    if prompt == "Enviornmental Protection":
        message = allPrompts[0]
    elif prompt == "Free Palestine":
        message = allPrompts[1]
    elif prompt == "Poverty":
        message = allPrompts[2]
    elif prompt == "Racial Redlining":
        message = allPrompts[3]

    return message
    
    

