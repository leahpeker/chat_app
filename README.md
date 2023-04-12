<h3 align="center">chat app</h3>

  <p align="center">
    project_description
  </p>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

These steps will guide you through project setup. This project utilizes sqlite.

### Prerequisites

Homebrew
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

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
   ```sh
   source venv/bin/activate
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
under the conversation title when you click into a conversation.

The send date and time for both messages and message thoughts are automatically recorded in the 
database and are displayed within the conversation.

