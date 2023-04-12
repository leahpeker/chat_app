<h3 align="center">chat app</h3>


<!-- ABOUT THE PROJECT -->
## About The Project
This project was an exciting way to get a basic insight into how chat apps work. The app includes
all models, forms, and views required to put the app together. It also includes unit testing and integration
testing. I did my best to create a holistic testing framework. I also added some CSS to get a general flow. 


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

These steps will guide you through project setup. This project utilizes sqlite.

### Prerequisites

Homebrew
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
You may be prompted to do a few additional steps to add brew to your PATH. Follow the steps given in the terminal.

Python3.10
```shell
brew install python@3.10
```


### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/leahpeker/chat_app.git
   ```
2. Open the chat_app directory
   ```sh
   cd chat_app
   ```
3. Create virtual environment
   ```sh
   python3.10 -m venv myenv
   ```
4. Activate virtual environment
* Mac
  ```sh
  source venv/bin/activate
  ```
* Windows
  ```sh
   myenv\Scripts\Activate
  ```
   
5. Install requirements
   ```sh
   pip3 install -r requirements.txt
   ```
6. Make migrations to set up the database
   ```shell
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

With the virtual environment activated, run the server.
```shell
python3 manage.py runserver
```
At this point, you should be able to access the application and see all conversations, messages, and thoughts. Users can 
also start new conversations, send new messages, and reply with new thoughts. On the homepage,
users can also search for conversations by title and search for messages by content. 

The start date for each new conversation is automatically added to the database and is displayed
under the conversation title when you click into a conversation. The user is inputting the date info without 
even knowing.

The send date and time for both messages and message thoughts are automatically recorded in the 
database and are displayed within the conversation. The user is inputting the datetime info without 
even knowing.

The app will be delivered with some conversations pre-loaded into the Sqlite database. Enjoy!  
