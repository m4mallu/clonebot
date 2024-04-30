echo "Credits: m4mallu> https://github.com/m4mallu"
sleep 1
clear >$(tty)
virtualenv -p python3 venv > /dev/null
. ./venv/bin/activate > /dev/null
echo "Installing requirements, please wait..."
pip3 install -r requirements.txt > /dev/null
sleep 1
clear >$(tty)
echo "Starting the bot, please wait..."
sleep 1
clear >$(tty)
python3 main.py