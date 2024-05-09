<h1 align="center">People's Budget :dollar:</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Statistics-FF8000?style=flat&logo=python&logoColor=white" alt="Statistics">
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=white" alt="React">
</p>

<p align="center">
  <img src="https://i.ibb.co/CHx5btZ/cover-auto-x2-colored-toned-light-ai.jpg" width="600" title="hover text">
</p>

## Demo

[![Demo Video](https://i.ibb.co/SX8yV3c/Screenshot-2023-09-05-at-23-11-06.png)](https://www.youtube.com/watch?v=2kalXcbpbh8)

You can watch our project's demo video on YouTube to get a quick overview of how it works.

## Website URL

You can access the live website by clicking the link below:

[People's Budget Website](https://budget.csariel.xyz/)

## Table of Contents

- [Project Goal](#project-goal)
- [Introduction](#introduction)
- [Key Features](#key-features)
- [Selected Approach](#selected-approach)
  - [Architecture and Design Pattern](#architecture-and-design-pattern)
  - [Application Structure](#application-structure)
  - [Algorithms](#algorithms)
  - [UX & UI](#ux--ui)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
     - [Server Installation](#server-installation)
        - [Environment Variable Configuration for the Server and Database](#environment-variable-configuration-for-the-server-and-database)
        - [Database Initialization and Running the Server](#database-initialization-and-running-the-server)
     - [Client Installation](#client-installation)
        - [Environment Variable Configuration for the Client](#environment-variable-configuration-for-the-client)
        - [Running the Client](#running-the-client)
- [Testing](#testing)
- [User Guide](#user-guide)
  - [Getting Started](#getting-started)
  - [Navigating the Application](#navigating-the-application)
  - [Revoting](#revoting)
  - [Additional Features](#additional-features)
- [License](#license)
- [Contributing](#contributing)
- [Team Information](#team-information)

## Project Goal

Our web application aims to foster active citizen participation in the state/municipality budget voting process, ensuring alignment with the will of the people. We seek to address the lack of influence and disconnection that citizens often feel regarding how their taxes are utilized. Through our intuitive and transparent platform, we empower individuals to have a direct impact on budget decisions.

## Introduction

Are you tired of feeling like your voice doesn't matter when it comes to budget decisions? Do you want to have a say in how your taxes are spent? Look no further! The People's Budget web application is here to revolutionize citizen participation. With our platform, you can actively engage in the voting process for state and municipal budgets, making your opinions count. We believe in the power of collective decision-making and strive to create a more inclusive and democratic society.

## Key Features

- **Online Voting for Budget Proposals**: Our web application allows users to vote online for the budget proposal. 
- **Revoting Capability for Updated Decisions**: Our system enables users to revise their votes accordingly.
- **Real-time Result Tracking for Transparency**: Transparency is crucial to us. We provide real-time tracking of voting results, allowing citizens to stay informed about the progress and outcomes of budget decisions.
- **Comprehensive Voter Statistics Dashboard**: To encourage informed participation, we offer a comprehensive voter statistics dashboard. It provides insights into the overall voting trends, demographics, and other relevant data.

## Selected Approach

To ensure modularity, scalability, and maintainability, we adopted a layered architecture approach. The system consists of three essential components: the presentation layer (client), the application layer (server), and the data layer (database).

### Architecture and Design Pattern

To facilitate seamless communication between the client and server, we employ a client-server pattern with RESTful APIs. This architecture enables efficient data exchange and supports a smooth user experience. Additionally, we utilize the strategy pattern to ensure flexible interaction between the server and database. The system architecture is robust and scalable, with clear component separation for easier maintenance and future enhancements.

### Application Structure

- **Client**: The client-side of our application is built using JavaScript and the React library. This choice ensures an optimal user experience, with responsive and interactive interfaces.
- **Server**: The server-side logic and information services are implemented using Python and the Flask library. This combination allows for efficient processing and handling of requests.
- **Database**: We utilize MySQL as the database management system, providing robust and reliable storage for our application data.

### Algorithms

Our web application incorporates powerful algorithms to guarantee fairness, truth-telling, Pareto-efficient, and anonymity in the voting process. These algorithms are designed to ensure that every vote is counted accurately and that user privacy is protected.

### UX & UI

User experience and user interface design are essential aspects of our project. We prioritize simplicity and ease of use, ensuring that citizens of all technical backgrounds can navigate the application effortlessly. Our design philosophy revolves around creating an intuitive interface that encourages active participation. We also provide a Guest Mode that allows users to explore the system before signing up.

## Getting Started

### Prerequisites

To run the People's Budget web application, you need to have the following installed on your system:

- MySql (8.1.0)
- Python (3.11.0)
- Node.js (18.13.0)

### Installation

To set up the People's Budget application locally, follow the steps below for both the Client and Server components:

#### Server Installation
1. Clone the repository: ```git clone https://github.com/ElhaiMansbach/Final-Project```
2. Navigate to the server directory: ```cd Final-Project/src/server```
3. Install the required Python dependencies: ```pip install -r requirements.txt```
4. Set up the necessary environment variables.

##### Environment Variable Configuration for the Server and Database
1. Create an '.env' file: Use the '.env.example' file in the server directory as a template.
```cp .env.example .env```
2. Edit the '.env' file: Open the '.env' file you've just created and modify the values if necessary.

##### Database Initialization and Running the Server
1. Install MySQL server and client packages: ```sudo apt install mysql-server mysql-client```
2. To initialize the database, navigate to the database directory and run the command: ```python3 sql_Initialization.py```
3. Navigate back to the server directory and start the server by running the command: ```python3 app.py```

#### Client Installation
1. On a new terminal, navigate to the client directory: ```cd src/client```
2. Install the required npm dependencies: ```npm install```
3. Set up the necessary environment variables.

##### Environment Variable Configuration for the Client
1. Create an '.env' file: Use the '.env.example' file in the client directory as a template.
```cp .env.example .env```
2. Edit the '.env' file: Open the '.env' file you've just created and modify the values if necessary.

##### Running the Client
1. Start the client by running the command: ```npm start```
2. The web browser will automatically initiate the client-side application.
3. You're ready to actively participate in the budget voting process!

## Testing

The project includes a dedicated test directory with subdirectories for client and server tests. These tests are designed to ensure the functionality and reliability of the application components. 

To execute the tests, follow these steps:

1. **Client Tests**:
   - Navigate to the `test/client` directory.
   - Install the required npm dependencies by running the command:
     ```bash
     npm install
     ```
   - Download and install a ChromeDriver that corresponds to your browser from [here](https://chromedriver.chromium.org/downloads).
   - Run the command to execute the client-side tests:
     ```bash
     npm run tests
     ```

   This command will run all the tests.

   To run a specific test, use the following command, replacing `"test name"` with the desired test name:
   ```bash
   node RunAllTests.js "test name"
   
2. **Server Tests**: Navigate to the `test/server` directory and run the command to execute the server-side tests:
   `pytest`
   
## User Guide

### Getting Started

1. **Accessing the Web Application**: Open your web browser and enter the URL of the People's Budget application.
2. **Creating an Account**: Click on the "Sign Up" button and follow the on-screen instructions to create your account.

   ![Create account](https://i.ibb.co/LSxsWWH/Create-account.png)

3. **Logging In**: After creating your account, click on the "Log In" button and enter your credentials to access the system.

   ![Log In](https://i.ibb.co/gS5ZK2V/log-in.png)

### Navigating the Application

1. **Home page**: Upon logging in, you will be redirected to the home page. This page provides information about the system.

   ![Home](https://i.ibb.co/QFnrF0Q/home.png)

2. **Voting**: You can easily modify the budget as per your preferences by casting your vote for a budget proposal. To vote, simply click on the "Vote" button at the bottom of the page and confirm your selection when prompted.

   ![Vote](https://i.ibb.co/fDFWZjQ/voting.png)

3. **Result Tracking**: You can monitor the progress and outcome of the budget vote in real-time by accessing the "Results" section. Our sophisticated algorithms calculate and present visualizations and updates on the voting process.

   ![Results](https://i.ibb.co/px81PKF/results.png)

4. **Dashboard**: Explore our comprehensive voter statistics dashboard to gain valuable insights into voting trends, demographics, and other relevant data. Utilize this information to make informed decisions and gain a better understanding of overall participation patterns.
   
   ![Dashboard](https://i.ibb.co/W0LqVDk/dashboard.png)

### Revoting

- **Revoting**: If you have already cast your vote but have since changed your mind, don't worry! Our system allows you to modify your vote by simply casting a new vote before the voting period ends.

### Additional Features
- **Guest Mode**: Before signing up, we recommend exploring the system and familiarizing yourself with the features in Guest Mode. This allows you to preview the application's functionalities without the need to create an account.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial (CC BY-NC) License](https://creativecommons.org/licenses/by-nc-nd/4.0/).

## Contributing

We welcome contributions to the People's Budget project! If you would like to contribute, please follow these guidelines:

1. Fork the repository and create your branch from `main`.
2. Make your desired changes and improvements to the codebase.
3. Ensure that your code adheres to the project's coding style and conventions.
4. Test your changes thoroughly to ensure they function as intended.
5. Commit your changes with clear and descriptive commit messages.
6. Push your changes to your forked repository.
7. Submit a pull request, detailing the changes you have made.

We will review the pull request and provide feedback or merge it into the main codebase if appropriate. We appreciate your contributions and look forward to collaborating with you!

Please note that by contributing to this project, you agree to license your contributions under the [Creative Commons Attribution-NonCommercial (CC BY-NC) License](https://creativecommons.org/licenses/by-nc-nd/4.0/). Your contributions must align with the license terms and restrictions.

If you have any questions or need further assistance with the contribution process, feel free to reach out to us.

## Team Information
This project was developed by:
<table align = "center">
  <tr>
    <td align="center"><a href="https://github.com/ElhaiMansbach"><img src="https://i.ibb.co/tsyV1FL/elhai-photo.jpg" width="150px;" alt=""/><br /><sub><b>Elhai Mansbach</b></sub></a><br /> </td>
    <td align="center"><a href="https://github.com/OfirOvadia96"><img src="https://i.ibb.co/cCzmpV6/ofir-ovadia.jpg" width="150px;" alt=""/><br /><sub><b>Ofir Ovadia</b></sub></a><br /> </td>
    <td align="center"><a href="https://github.com/Lioo7"><img src="https://i.ibb.co/2MCYM0m/lioz-photo.jpg" width="150px;" alt=""/><br /><sub><b>Lioz Akirav</b></sub></a><br /> </td>
  </tr>
</table>
Under the supervision of <a href="https://github.com/erelsgl">Dr. Erel Segal Halevi</a>.
