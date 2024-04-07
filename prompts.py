# PURPOSE OF THIS PYTHON FILE

# this file contains all the prompts for each topic (these are for sending the email meaning they will not have HTML/CSS within them and sent to mailto) 
southernBorder = """American conduct concerning the Southern Border has been to the displeasure of myself and a large portion of the American population. The U.S. Border Patrol detailed anywhere from 2.2 to  2.4 million encounters with migrants attempting to enter the country in 2022, compared to under 1.7 million encounters in 2021. 149,000 unaccompanied children and 483,000 family units made the difficult and dangerous trek through the Central American Subcontinent in search of a freer life run by democracy, liberty, and freedom. The number of migrants seeking asylum from violence and autocracy and those in search of economic freedom is multiplying. These figures are only set to continue their climb as Latin American nations are plunged into further and further turmoil.The corridors migrants are forced to enter have become increasingly dangerous as rural pathways are selected as alternatives to entrances closer to urban areas. This shift in where migrants are crossing is making an already exhausting journey further life-threatening. Routes across rivers and expansive deserts are causing hundreds of people to die on migration routes per year. The number of migrants found dead in the US-Mexico has been increasing dramatically for decades without any sign of that trend slowing down.The American people have not witnessed a government attempting to save the lives of the people who are making a tireless journey to become citizens as they are. Instead, resources have been devoted to further militarism of the border instead of to the assistance of fellow human beings. Americans don’t want to see their resources going towards the prosecution of disadvantaged individuals or the creation of a border mirroring the Korean DMZ. Prosecutions and militarism have done nothing to prevent migrant attempts to make better lives for themselves.The citizens of the United States of America, the citizens of an immigrant nation, want to see our government honor the men, women, and children who built this country by increased acceptance of asylum-seekers, a healthy processing of migrants that doesn’t subject them to cruel and dehumanizing facilities and staff, and an affirmation that further resources will not be allocated to create a dangerous or hostile environment for those looking to build a fulfilling life in a foreign land."""

freePalestine = """The American people have continued in support of the citizens of Gaza with calls for a ceasefire. Our cries have fallen on deaf ears as Congress has maintained pumping funds and weapons into the Israeli war machine. The actions taken by Hamas on October 7th were deplorable and impossible to condone. However, the citizens of the United States cannot and will not disregard the deaths of over 25,000 Gazan citizens, injuries to over 63,000, and the displacement of over 1.7 million more. There are less than 10 functioning hospitals left in the region as violence continues and disease spreads. Only 15 bakeries remain to feed millions. Water, fuel, and other vital resources are restricted from reaching those who most need them. Communication is shut down for days at a time, preventing Gazans from communicating in their time of need. Over $300 billion of American’s tax dollars has been sent to fund over 15% of Israel’s defense budget. That budget is not spent solely for defense, but for the slaughter and genocide of young Gazan children. The United States has tied itself in an unhealthy relationship with the state of Israel that looks to jeopardize not only Gaza but the Middle East and American relations with the rest of the world. In January of 2024, the International Court of Justice demanded Israel take all measures within its power to prevent the, “killings, serious physical or mental harm, the deliberate infliction of conditions of life calculated to bring about the physical destruction of the population in whole or in part, and the imposition of measures intended to prevent births;” For months the Israeli military has ignored those demands.Hamas will not crumble quickly, and the number of innocent people paying the price for a crime they did not commit is rising. Commerce, manufacturing, and agriculture will cease to exist if violence persists. The injury to critical aspects of civilian life, the displacement, the depopulation—will continually worsen as the United States promotes this genocide. The American people demand our Congressional representatives call for an immediate ceasefire. We demand our tax dollars no longer be spent propping up violent regimes. We demand aid and relief be brought to Gaza immediately. We demand an America founded and built upon representation and democracy be returned to its people. We demand an end to the war in Gaza."""

affordableHousing = """Our nation lacks affordable housing, and the American people will no longer stand for it. In the United States, there are over 11 million families with extremely low incomes to jockey over 7 million units of affordable housing for renters with such an economic status. There is not a single state in the union with an adequate number of affordable housing units for their extremely low income population; no state even comes close. This disparity is only exacerbated by individuals with higher incomes occupying 3.3 million of the 7 million available units. Our housing supply is being dished out in ways that actively put American families at risk. Families who are disproportionately Black, Latino American, or American Indian/Alaska Native. 19% of Black households, 14% of Latino households, and 17% of American Indian or Alaska Native households who rent have extremely low incomes, compared with only 6 percent of white households. Millions of low-income families live in houses that are not affordable for their wages. Households with extremely low incomes are spending exuberant amounts on housing. 86% of extremely low-income Americans spend over 30% of their wealth on housing, and 73% spend over 50%.A majority of low-income Americans are being punished by a lack of housing meant for them. The pool of housing they have no control over is increasing because of state and local zoning and land-use policies. There is a complacency in the response to combat the housing crisis plaguing lower-income Americans that allows affordable housing to fall further and further behind the eight ball. Our nation commits an astonishingly small amount of money towards developing new affordable units, which only slightly increases as costs rise significantly. Our states and local governments spend less on housing and community development than we do on the police or corrections.The American people can no longer sit in silence as our most vulnerable citizens are punished for their limited income. They are penalized by inaction from all levels of government to increase the amount of housing and the amount available to each family. Zoning and land use laws bound the land supply that can be built upon. American minorities are suffering from this crisis more and more as the years go on. We demand our representatives call for increased spending on affordable and public housing. We demand more land be made available for development. We demand a conscious effort from our government to lift Americans out of this housing crisis."""


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
    southern_border = f"""<p>American conduct concerning the Southern Border has been to the displeasure of myself and a large portion of the American population. The U.S. Border Patrol detailed anywhere from 2.2 to 2.4 million encounters with migrants attempting to enter the country in 2022, compared to under 1.7 million encounters in 2021. 149,000 unaccompanied children and 483,000 family units made the difficult and dangerous trek through the Central American Subcontinent in search of a freer life run by democracy, liberty, and freedom. The number of migrants seeking asylum from violence and autocracy and those in search of economic freedom is multiplying. These figures are only set to continue their climb as Latin American nations are plunged into further and further turmoil.</p><p>The corridors migrants are forced to enter have become increasingly dangerous as rural pathways are selected as alternatives to entrances closer to urban areas. This shift in where migrants are crossing is making an already exhausting journey further life-threatening. Routes across rivers and expansive deserts are causing hundreds of people to die on migration routes per year. The number of migrants found dead in the US-Mexico has been increasing dramatically for decades without any sign of that trend slowing down.</p><p>The American people have not witnessed a government attempting to save the lives of the people who are making a tireless journey to become citizens as they are. Instead, resources have been devoted to further militarism of the border instead of to the assistance of fellow human beings. Americans don’t want to see their resources going towards the prosecution of disadvantaged individuals or the creation of a border mirroring the Korean DMZ. Prosecutions and militarism have done nothing to prevent migrant attempts to make better lives for themselves.</p><p>The citizens of the United States of America, the citizens of an immigrant nation, want to see our government honor the men, women, and children who built this country by increased acceptance of asylum-seekers, a healthy processing of migrants that doesn’t subject them to cruel and dehumanizing facilities and staff, and an affirmation that further resources will not be allocated to create a dangerous or hostile environment for those looking to build a fulfilling life in a foreign land.</p><p>Sincerely,<br>{name}</p>"""


    free_palestine =  f"""<p>The American people have continued in support of the citizens of Gaza with calls for a ceasefire. Our cries have fallen on deaf ears as Congress has maintained pumping funds and weapons into the Israeli war machine. The actions taken by Hamas on October 7th were deplorable and impossible to condone. However, the citizens of the United States cannot and will not disregard the deaths of over 25,000 Gazan citizens, injuries to over 63,000, and the displacement of over 1.7 million more.</p><p>There are less than 10 functioning hospitals left in the region as violence continues and disease spreads. Only 15 bakeries remain to feed millions.Water, fuel, and other vital resources are restricted from reaching those who most need them. Communication is shut down for days at a time, preventing Gazans from communicating in their time of need.</p><p>Over $300 billion of American’s tax dollars has been sent to fund over 15% of Israel’s defense budget. That budget is not spent solely for defense, but for the slaughter and genocide of young Gazan children. The United States has tied itself in an unhealthy relationship with the state of Israel that looks to jeopardize not only Gaza but the Middle East and American relations with the rest of the world.</p><p>In January of 2024, the International Court of Justice demanded Israel take all measures within its power to prevent the, “killings, serious physical or mental harm, the deliberate infliction of conditions of life calculated to bring about the physical destruction of the population in whole or in part, and the imposition of measures intended to prevent births;” For months the Israeli military has ignored those demands.</p><p>Hamas will not crumble quickly, and the number of innocent people paying the price for a crime they did not commit is rising. Commerce, manufacturing, and agriculture will cease to exist if violence persists. The injury to critical aspects of civilian life, the displacement, the depopulation—will continually worsen as the United States promotes this genocide.</p><p>The American people demand our Congressional representatives call for an immediate ceasefire. We demand our tax dollars no longer be spent propping up violent regimes. We demand aid and relief be brought to Gaza immediately. We demand an America founded and built upon representation and democracy be returned to its people. We demand an end to the war in Gaza.</p><p> Sincerely,<br>{name}</p>"""

    affordable_housing = f"""<p>Our nation lacks affordable housing, and the American people will no longer stand for it. In the United States, there are over 11 million families with extremely low incomes to jockey over 7 million units of affordable housing for renters with such an economic status. There is not a single state in the union with an adequate number of affordable housing units for their extremely low income population; no state even comes close.</p><p>This disparity is only exacerbated by individuals with higher incomes occupying 3.3 million of the 7 million available units. Our housing supply is being dished out in ways that actively put American families at risk. Families who are disproportionately Black, Latino American, or American Indian/Alaska Native. 19% of Black households, 14% of Latino households, and 17% of American Indian or Alaska Native households who rent have extremely low incomes, compared with only 6 percent of white households.</p><p>Millions of low-income families live in houses that are not affordable for their wages. Households with extremely low incomes are spending exuberant amounts on housing. 86% of extremely low-income Americans spend over 30% of their wealth on housing, and 73% spend over 50%. A majority of low-income Americans are being punished by a lack of housing meant for them. The pool of housing they have no control over is increasing because of state and local zoning and land-use policies.</p><p>There is a complacency in the response to combat the housing crisis plaguing lower-income Americans that allows affordable housing to fall further and further behind the eight ball. Our nation commits an astonishingly small amount of money towards developing new affordable units, which only slightly increases as costs rise significantly. Our states and local governments spend less on housing and community development than we do on the police or corrections.</p><p>The American people can no longer sit in silence as our most vulnerable citizens are punished for their limited income. They are penalized by inaction from all levels of government to increase the amount of housing and the amount available to each family. Zoning and land use laws bound the land supply that can be built upon. American minorities are suffering from this crisis more and more as the years go on. We demand our representatives call for increased spending on affordable and public housing. We demand more land be made available for development. We demand a conscious effort from our government to lift Americans out of this housing crisis.</p><p>Sincerely,<br>{name}</p>"""

    poverty = "Filler text: Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    

    return [southern_border, free_palestine, affordable_housing, poverty]

# prompt function for the /email page 
def subjectPrompt(prompt,name,represenative, zip):
    message = []
    # get the LIST of prompts
    allPrompts = getAllPrompts(name, represenative)
    if prompt == "Southern Border":
        #message = allPrompts[0]
        message.append(allPrompts[0])
        message.append(southernBorder + "Sincerely, " + name + " ZipCode: " + zip)

    elif prompt == "Free Palestine":
        #message = allPrompts[1]
        message.append(allPrompts[1])
        message.append(freePalestine  + "Sincerely, " + name + " ZipCode: " + zip)

    elif prompt == "Affordable Housing":
        #message = allPrompts[2]
        message.append(allPrompts[2])
        message.append(affordableHousing  + "Sincerely, " + name + " ZipCode: " + zip)

    elif prompt == "Racial Redlining":
        #message = allPrompts[3]
        message.append(allPrompts[3])
        message.append(racialRedlining)

    return message
    
    