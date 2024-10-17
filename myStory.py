import random

# Defining list of phrases which will help to build a story
def storyPrompt():

    Sentence_starter = ['About 100 years ago,', ' In the 20 BC,', 'Once upon a time,', 'Quite recently,']
    character = [' there lived a king.',' there was a man named Jack.',' there lived a farmer.', ' there was once a beautiful man named Mutton.', ' there was once a girl named Mutton-Chan.']
    time = [' One day,', ' One full-moon night,', ' On a bright sunny afternoon,', ' On one horrible day,' ]
    story_plot = [' they accidentally slipped off from a cliff',' they were killed after a robbery', ' they got knocked down by a car']
    place = [' near the mountains.', ' at the garden.', ' at the city center.', ' in your house.']
    second_character = [' They saw a strange man', ' There was a suspicious lady']
    age = [' who seemed to be in their late 20s', ' who seemed very old and feeble']
    work = [' searching for something.', ' digging a well on the roadside.', ' getting ready to chop off their limbs.', ' crying.', ' eating rats.']
    end = [' The strange individual rushed towards them and started chewing on their skin.', ' The strange individual suddenly grabbed and stuffed them into a brown bear suit.', ' The strange individual out of the blue started singing and cursing them.']
    true_end = [' Turns out the strange individual was Mutton_Chan, you can never escape me :wink:',]

    return random.choice(Sentence_starter)+random.choice(character)+random.choice(time)+random.choice(story_plot) +random.choice(place)+random.choice(second_character)+random.choice(age)+random.choice(work)+random.choice(end)+random.choice(true_end)