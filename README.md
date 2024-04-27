<h1 align="left">
    <a target="_blank">
        Clonebot
        <img src="http://www.randomnoun.com/wpf/shell32-avi/tshell32_160.gif" width="272" height="60">
    </a>
</h1>

#### An <a href="https://choosealicense.com/licenses/gpl-3.0/"  target="_blank"> opensource </a> Telegram robot can clone media & text from any chat to your own chat.<br>
Read the <a href="https://space4renjith.blogspot.com/2022/05/clonebot-technical-documentation.html" target="_blank"> documentation </a>to know how to use the bot
<br>
<p align="left">
    <br>
        <b>DUE TO SOME SECURITY REASONS, DEPLOY TO HEROKU FROM THIS REPOSITORY HAS BEEN ABOLISHED !</b>
    <br>
        <u>This repository is no longer supporting Heroku deployment. Use a paid VPS / Raspberry Pi / Local pc instead. See the documentation for more.</u>
    <br><br>
    <a href="https://t.me/rmprojects" target="_blank">@M4Mallu</a>
</p>

<details>
    <summary><b>Deploy Using Docker</b></summary>
1. Deploying on VPS Using Docker

- Start Docker daemon (skip if already running), if installed by snap then use 2nd command:
    
        sudo dockerd
        sudo snap start docker

     Note: If not started or not starting, run the command below then try to start.

        sudo apt install docker.io

- Build Docker image:

        sudo docker build . -t clone-bot

- Run the image:

        sudo docker run clone-bot

- To stop the image:

        sudo docker ps
        sudo docker stop id

- To clear the container:

        sudo docker container prune

- To delete the images:

        sudo docker image prune -a

2. Deploying on VPS Using docker-compose

    **NOTE**: If you want to use port other than 80, change it in docker-compose.yml

```
sudo apt install docker-compose
```
- Build and run Docker image:
```
sudo docker-compose up
```
- After editing files with nano for example (nano start.sh):
```
sudo docker-compose up --build
```
- To stop the image:
```
sudo docker-compose stop
```
- To run the image:
```
sudo docker-compose start
```

</details>










