from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from ChatBot import ChatBot
import time, sys

class WhatsAppBotGPT:
    def __init__(self, Number:str, chatbot):
        self.number = Number
        self.service = Service(ChromeDriverManager().install())
        self.service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=self.service)
        self.msgbreak = ""
        self.conversation = chatbot

    def run(self):
        """
        Method that starts the conversation with the specified number.
        """
        self.driver.get(f"https://web.whatsapp.com/send?phone={self.number}")  # Navigate to the chat page
        while len(self.driver.find_elements(By.ID, 'side')) < 1: # Wait until the page is fully loaded
            time.sleep(1)
        time.sleep(2)
        print("Synchronizing messages...")
        while (len(self.driver.find_elements(By.XPATH,r"/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[2]/div[2]/button"))) > 0: # Wait for messages to be synchronized
            time.sleep(1)
        time.sleep(2)
        print("Messages synchronized")
        self.messages = list() # Initialize message list
        while True: # Infinite loop to check for new messages
            time.sleep(1)  # Wait 1 second between each check
            elements = self.driver.find_elements(By.XPATH, f"//span[@data-testid='conversation-info-header-chat-title']") # Find element containing the person's name
            name = f"{elements[0].text}:" # Extract the person's name
            divs = self.driver.find_elements(By.XPATH, f"//div[contains(@data-pre-plain-text, '{name}')]") # Get the divs that contain the user's messages
            if divs:
                last_parent = divs[-1] # Get the most recent div
                child_elements = last_parent.find_elements(By.XPATH, "./*[not(contains(@class, '_1hl2r'))]") # Get the child elements of the div
                last_child = child_elements[-1] # Get the most recent element
                text = last_child.text.replace("\n","") # Extract the text from the most recent element (most recent message from user)
                if text in self.messages: # Check if the text is in the self.messages list
                    response = self.conversation.question(text) # Send the user's last message to the "question" method of the "ChatBot" class
                    if response: # Check if the "question" method returned a response
                        time.sleep(2) # Wait for 2 seconds, making the script more human-like
                        element = self.driver.find_element(By.XPATH, f'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p') # Get element responsible for sending messages
                        element.clear() # Clear the message (common practice to avoid unintended messages)
                        element.send_keys(response) # Write the message to the element
                        time.sleep(1) # Wait for another 1 second
                        element.send_keys(Keys.ENTER) # Send the message
                    continue # Restart message checking
                else:
                    self.messages.append(text) # Add the last message to the self.messages list
            else:
                print("No user messages.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Phone number and API_KEY is mandatory and must be passed as an argument.")
    phone_number = sys.argv[1]  # Obtains the phone number of the recipient from the command line
    Api_key = sys.argv[2] # Obtains the API KEY from the command line
    Chatbot = ChatBot(API_KEY="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")
    WhatsappBot = WhatsAppBotGPT(Number=phone_number, chatbot=Chatbot)
    WhatsappBot.run


