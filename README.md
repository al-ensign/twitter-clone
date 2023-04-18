# Twitter Clone 

## Overview :memo:

This repository contains a clone of Twitter built using Django Rest Framework, FastAPI, PostgreSQL, AWS DynamoDB, AWS S3, AWS SES, and RabbitMQ. The system supports three types of users, namely administrators, moderators, and regular users. The project follows GitHub Flow, and all non-functional requirements, such as database and cloud storage, are hosted on AWS.

## Main Functionality :rocket: 

The system is built using microservices architecture and provides a wide range of features that allow users to create and manage their own pages, follow other users' pages, and write and interact with posts.

The application is designed with three different user roles: Administrator, Moderator, and User. Each role is assigned specific permissions to manage the system and maintain its security. Users can sign up, log in, and perform various actions such as creating and editing pages, writing posts, and subscribing to other users' pages. Additionally, the app includes functionalities such as cloud storage for user and page avatars, email notifications for subscribers, and automatic blocking of pages in case a user is blocked.

Furthermore, the app provides detailed statistics of page performance, such as the number of posts, followers, and likes, generated by the microservice, which is only visible to page owners.

## Technology Stack :computer:

- **Web Frameworks :globe_with_meridians: :** **Django** and **Django Rest Framework** for the core app and **FastAPI** for the microservice
- **Databases :ledger: :** **PostgreSQL** for the core app and **AWS DynamoDB** for microservice
- **Cloud :cloud: :** **AWS S3** for storing files and avatars and **AWS SES** for email notifications
- **Message Broker :briefcase: :** **RabbitMQ** for both microservice and **Celery**
- **Authentication :key: :** custom **JWT** authentication with **PyJWT**
- **Unit Testing :mag_right: :** mock and fixture with **pytest**
- **Containerization:** **Docker** and **docker-compose** 
- **Version Control:** **Git** and **Git Flow**

## How to use this app? 

### Step 1: Clone this repository to your machine

> You can check here how to clone repositories from GitHub ➜ [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) 

### Step 2: Install Docker and Docker Compose 

> You can check here how to install docker for your OS ➜ [Get Docker](https://docs.docker.com/get-docker/) 

### Step 3: Start the Environment and Install the Packages

```
pipenv install
pipenv shell
```

### Step 4: Build and Run the Application in Docker-Compose

```
docker compose up --build
```

