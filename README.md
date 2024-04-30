# Clonebot

[![Clonebot Logo](http://www.randomnoun.com/wpf/shell32-avi/tshell32_160.gif)](#)

#### An [opensource](https://choosealicense.com/licenses/gpl-3.0/) Telegram robot can clone media & text from any chat to your own chat.
Read the [documentation](https://space4renjith.blogspot.com/2022/05/clonebot-technical-documentation.html) to know how to use the bot

---

**DUE TO SOME SECURITY REASONS, DEPLOY TO HEROKU FROM THIS REPOSITORY HAS BEEN ABOLISHED!**
<br>
*This repository is no longer supporting Heroku deployment. Use a paid VPS / Raspberry Pi / Local PC instead. See the documentation for more.*

[@M4Mallu](https://t.me/rmprojects)

<details>
    <summary><b>Deploy Using Docker</b></summary>

1. **Deploying on VPS Using Docker**

    - Start Docker daemon (skip if already running), if installed by snap then use 2nd command:
    
        ```bash
        sudo dockerd
        sudo snap start docker
        ```

        Note: If not started or not starting, run the command below then try to start.

        ```bash
        sudo apt install docker.io
        ```

    - Build Docker image:

        ```bash
        sudo docker build . -t clone-bot
        ```

    - Run the image:

        ```bash
        sudo docker run clone-bot
        ```

    - To stop the image:

        ```bash
        sudo docker ps
        sudo docker stop id
        ```

    - To clear the container:

        ```bash
        sudo docker container prune
        ```

    - To delete the images:

        ```bash
        sudo docker image prune -a
        ```

2. **Deploying on VPS Using docker-compose**

    **NOTE**: If you want to use a port other than 80, change it in docker-compose.yml

    ```bash
    sudo apt install docker-compose
    ```

    - Build and run Docker image:

    ```bash
    sudo docker-compose up
    ```

    - After editing files with nano for example (nano start.sh):

    ```bash
    sudo docker-compose up --build
    ```

    - To stop the image:

    ```bash
    sudo docker-compose stop
    ```

    - To run the image:

    ```bash
    sudo docker-compose start
    ```

</details>
