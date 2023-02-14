import json
import spacy

# Load the language model
nlp = spacy.load("en_core_web_lg")

# Define the questions and answers in a list
faq = [
    {
        "q": "What are the minimum requirements to drive with Grab?",
        "a": "Singaporean with valid PDVL/TDVL.\nOr Singapore PR employed under a limousine company with valid PDVL\nMinimum 1 year of driving experience.\nAccumulated less than 18 Demerit Points (DIPS).\nDrive with a 4-door car (subject to approval) with the appropriate classification and commercial insurance coverage.\nSuccessfully completed Grab Transport Driver Training & Assessment here"
    },
    {
        "q": "Is there an information session that I can attend to find out more about succeeding on the Grab platform?",
        "a": "In view of recent developments with the COVID-19 situation, the local authorities have advised businesses to take on additional precautionary measures. Hence we have put a pause to the info session program."
    },
    {
        "q": "What incentives does Grab offer?",
        "a": "As a Grab driver-partner, you will receive a weekly email regarding our incentives. For more info, click here."
    },
    {
        "q": "How and when do I get paid?",
        "a": "Our flexible payment options allow for cash jobs. This means you can receive your fare earnings at the end of each trip. Alternatively, for credit card jobs, you will receive payment via your Grab cash wallet and will be able to cash out daily (minimum $50 per transaction)."
    },
    {
        "q": "Does Grab take any commission?",
        "a": "Yes, Grab takes a maximum of 20% commission."
    },
    {
        "q": "I already have a job. Can I still drive with Grab?",
        "a": "Of course! We have a lot of part-time drivers on our platform. This is because there are no minimum hours required to drive with us."
    },
    {
        "q": "I don’t have a car. Can I still drive with Grab?",
        "a": "Sure thing! You have the option of renting from GrabRentals, our recommended fleets, or any other rental company. Rental rates start as low as $50/day."
    },
    {
        "q": "What is PDVL (Private Hire Car Driver’s Vocational Licence)?",
        "a": "PDVL refers to the official licence required for all drivers who wish to provide chauffeured services. This..."
    },
        {
      "q": "I have questions. How can I reach you?",
      "a": "Find out more at grab.com/sg/driver/drive/ or send us an inquiry via this help center form : Grab@Tampines-Online-Support. Do check via the website on the services available in Grab@Tampines and book an appointment before heading down to :\n\nGrab@Tampines\n18 Tampines Industrial Crescent\n#01-12C Space@Tampines\nSingapore 528605\n\nOur opening hours are as follows:\n\nMonday – Friday: 10am – 6pm\nSaturdays, Sundays & PH: Closed"
    },
    {
      "q": "I’m ready to sign up to drive with Grab. What are my next steps?",
      "a": "We’re thrilled that you’re taking your first steps with Grab! Please click on the buttons below for a step-by-step guide for driving with Grab."
    },
    {
      "q": "I have other commitments on weekdays. Can I submit my application online?",
      "a": "Yes, of course! For drivers who are new to Grab, simply visit register.grab.com at your convenience to submit your application along with your supporting documents."
    },
    {
      "q": "Why does my car need to be registered as Z10/Z11?",
      "a": "This is a requirement by LTA. A Z10/Z11 vehicle log refers to private hire cars."
    },
    {
      "q": "Why does my car need to be commercially insured?",
      "a": "With commercial insurance, both you and your rider will be adequately protected should an accident happen."
    },
    {
      "q": "Does the ownership of my car need to be changed to my new business prior to driving with Grab?",
      "a": "No, as of 1st October 2017, drivers can simply log on to ONE.MOTORING to convert the vehicle scheme for Private hire (Chauffeur) with a fee of $100 (before GST)."
    }
]

def removeStopWords(doc):
    withoutstwords =  [token.text for token in doc if not token.is_stop]
    return nlp(" ".join(withoutstwords))

# Process the questions with spaCy
questions = [removeStopWords(nlp(dic['q'])) for dic in faq]
answers = [removeStopWords(nlp(dic['a'])) for dic in faq]



def get_answer(text):
    doc = removeStopWords(nlp(text))
    similarities = [doc.similarity(question) for question in questions]
    similarities_answers = [doc.similarity(answer) for answer in answers]
    index = similarities.index(max(similarities))
    index_answer = similarities_answers.index(max(similarities_answers))
    return json.dumps({ "a":faq[index]['a'],"score":max(similarities), "q": faq[index]['q'], "aa":faq[index_answer]['a'],"scorea":max(similarities_answers)})


import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        print("Received message:", message)
        # message = json.loads(message)
        # question = message["question"]
        response = get_answer(message)
        await websocket.send(response)

start_server = websockets.serve(handler, 'localhost', 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()