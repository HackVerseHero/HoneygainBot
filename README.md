# HoneygainBot
Honeygain Bot is an automated tool on Telegram that collects daily bonuses from the Honeygain platform. It provides manual and automatic bonus collection, along with earnings statistics. Can be deployed in a Docker container for convenience.

## The Honeygain bot, based on the aiogram framework and the pyHoneygain library, provides the following functionality and features with a Telegram interface:

1. Manual bonus collection: Users can utilize the bot to manually collect daily bonuses from the Honeygain platform. The bot offers a Telegram interface where users can activate the bonus collection option and receive instructions on the process. For example, they can press the "Collect Bonus" button in the bot's chat to initiate the bonus collection process.

2. Automatic bonus collection: The bot also offers the capability of automatic collection of daily bonuses from the Honeygain platform. It regularly checks for available bonuses and automatically collects them without requiring user intervention. For instance, the bot can initiate the automatic bonus collection once a day or according to user-defined settings.

3. Earnings statistics from Honeygain: The bot provides users with statistics regarding their earnings on the Honeygain platform. It can provide information about total earnings, the amount of data contributed by users, and other relevant indicators. This assists users in tracking their progress, evaluating the effectiveness of their platform utilization, and analyzing their earnings in a convenient format.

4. Additionally, it's worth noting that the Honeygain bot can be deployed within a Docker container, enabling easy installation and management across different environments. Containerization facilitates seamless deployment of the bot and ensures its independence from specific execution environments.

<p align="center">
  <img src="https://github.com/NickolaiHula/HoneygainBot/assets/93491542/67540bf8-43c7-499b-9ce6-e26aef465f7c" alt="Зображення" style="border: 1px solid black; padding: 5px; width: 30%; height: auto;">
</p>

<span>docker-compose.yml example:</span>
<p align="center">
<pre>
version: "2"
volumes:
    honeypot:
services:
  honey_pot:
    build: ./HoneygainBot
    volumes:
      - honeypot:/user/app/honey_pot/Storage
    environment:
      - BOT_TOKEN=[your bot token]
      - USER_ID=[your user_id]
      - HONEYGAIN_USER=[your email]
      - HONEYGAIN_PASS=[your password]
    ports:
      - 8088:80
    restart: always
</pre>
</p>

The PyHoneygain library has provided us with simplicity and convenience in interacting with the Honeygain platform API, enabling us to effectively utilize its functional capabilities in our project. We would like to extend our special thanks to <a href="https://github.com/coder-amogh">coder-amogh</a>, the author of PyHoneygain, for their contribution. You can find the library at: https://github.com/coder-amogh/pyHoneygain.


