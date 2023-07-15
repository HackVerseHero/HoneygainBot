
class Messages:
    hello_message = 'Hello! I am a bot for collecting Honeygain bonuses. With my help, you can automatically gather' \
                    'bonuses and track your earnings statistics.\n\n' \
                    'Key features of the bot:' \
                    '\n - Automatic bonus collection: I perform routine tasks of collecting Honeygain bonuses for ' \
                    'you, so you can earn even more.' \
                    '\n - Earnings statistics: I provide you with detailed statistics of your earnings, allowing you' \
                    ' to monitor your progress and identify the most profitable moments.' \
                    '\n - Last activity timestamp: I also display the time of your last activity, helping you control' \
                    ' your engagement and find the optimal working schedule.\n\n' \
                    'I\'m ready to get started!\n' \
                    'Happy earning!'

    honeypot_opening = 'Trying to open honeypot...'
    getting_honeypot_status = 'Trying to get honeypot status...'
    getting_statistics = 'Trying to get statistics...'

    @staticmethod
    async def starting_message(first_name):
        return f'Hello, {first_name}! To start working, please execute the command /start.'

    @staticmethod
    async def unrecognised_command_message(first_name):
        return f'What, {first_name}?'
