# Mr. Cleve Bot

This project serves as a Telegram Bot that is aimed to enhance patients' experiences during their treatment and recovery in the clinic.

> Implementation for the **Cleveland Clinic Hackathon 2025**, which was hosted by **42 Abu Dhabi**.

## Collaborators

* [Timur Mazitov](https://github.com/tmazitov)
* [Igor Mile](https://github.com/IqMent)

## Tech Stack

- 🐍 **Python 3.9** - programming language
- 📱 **aiogram** - library as a Telegram API wrapper
- 🧠 **openai** - library as a OpenAI API wrapper
- 🌐 **playwright** - library for web scraping

Check `requirements.txt` for more details.

## Features

- `AI Doctor Search` - helps to connect patients and appropriate doctors using patients' cases descriptions. How does it works? Example:

```text

    $ Step 1. User write his case explaination to the Bot. 
    
    Example: I feel bad, becouse of the pain in my back. Yesterday I was riding the bicycle and I fell down on the ground once. Could you help me?

    $ Step 2. The bot tries to extract symptoms from the text and, if it isn’t an emergency case, it prepares a list of short questions to get more details.

    $ Step 3. After receiving all answers, the bot tries to guess what disease the patient might have using the entire input context.

    $ Step 4. Based on the disease name, the bot replies to the patient with a list of doctors who can help, along with an option to book a session.

```

- `First Aid Guidelines` - explains how to make first aid step by step with pictures. 

## How to run

### Installation and Running the Project

1. **Clone the Repository**  
    ```bash
    git clone https://github.com/your-username/cleveland-clinic-bot.git
    cd cleveland-clinic-bot
    ```

2. **Set Up a Virtual Environment**  
    It is recommended to use a virtual environment to manage dependencies.  
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**  
    Use `pip` to install the required libraries from `requirements.txt`.  
    ```bash
    pip install -r requirements.txt
    ```
4. **Setup .env file**  
    Setup projects credentials to the `.env` file and api keys following this structure:
    ```bash
    OPENAI_API_KEY="your-openai-key"
    BOT_API_KEY="your-telegram-key"
    ```

5. **Run the Bot**  
    Start the bot using the following command:  
    ```bash
    python3 main.py
    ```

    Now the bot is ready to use!
