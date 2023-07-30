import asyncio
from datetime import datetime, timedelta
from pyHoneygain import HoneyGain
from Messages.honeygain_messages import HoneyGaneMessages
from colorama import Fore


class HoneypotCatchBot:
    def __init__(self, user, password, storage, handler=None, wait_to_recheck_status=1):
        self.storage = storage
        self.handler = handler
        self.user = user
        self.password = password
        self.honeygain_user = HoneyGain()
        self.wait_to_recheck_status = wait_to_recheck_status

    async def wait(self, awake_time):
        awake_to_catch_time = awake_time
        old_awake_to_catch_time = datetime.min
        try:
            old_awake_to_catch_time = self.storage.get_data("timestamps", "awake_to_catch_time")
            old_awake_to_catch_time = datetime.strptime(old_awake_to_catch_time, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(Fore.RED + "Failed to read data from the database; they may be missing.")
            print(e)
        if old_awake_to_catch_time < awake_to_catch_time:
            try:
                self.storage.update_data("timestamps", "awake_to_catch_time", awake_to_catch_time)
            except Exception as e:
                print(Fore.RED + "Failed to update the record in the database; attempting to create a new one.", e)
                self.storage.set_data("timestamps", "awake_to_catch_time", awake_to_catch_time)
        else:
            awake_to_catch_time = old_awake_to_catch_time
        if self.handler:
            formatted_awake_time = awake_to_catch_time.strftime("%Y-%m-%d %H:%M:%S")
            message = await HoneyGaneMessages.wait_to_message(formatted_awake_time)
            await self.handler(message)
        try:
            awake_to_catch_time = self.storage.get_data("timestamps", "awake_to_catch_time")
            awake_to_catch_time = datetime.strptime(awake_to_catch_time, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(Fore.RED + "Failed to read data from the database; they may be missing.")
            print(e)
        if not (awake_to_catch_time <= datetime.now()):
            time_difference = awake_to_catch_time - datetime.now()
            await asyncio.sleep(time_difference.total_seconds())

    async def reset_timers(self):
        if 0 <= datetime.now().hour < 3:
            new_awake_time = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)
        else:
            new_awake_time = (datetime.now() + timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0)
        try:
            self.storage.update_data("timestamps", "awake_to_catch_time", new_awake_time)
        except Exception as e:
            print(Fore.RED + "Failed to update the record in the database; attempting to create a new one.", e)
            self.storage.set_data("timestamps", "awake_to_catch_time", new_awake_time)

    async def get_honeypot_status(self):
        try:
            last_open_time = self.storage.get_data("timestamps", "last_open_time")
            last_open_time = datetime.strptime(last_open_time, '%Y-%m-%d %H:%M:%S')
            last_open_time = last_open_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(Fore.RED + "Failed to read data from the database; they may be missing.", e)
            last_open_time = None
        try:
            next_open_time = self.storage.get_data("timestamps", "awake_to_catch_time")
            next_open_time = datetime.strptime(next_open_time, '%Y-%m-%d %H:%M:%S')
            next_open_time = next_open_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(Fore.RED + "Failed to read data from the database; they may be missing.", e)
            next_open_time = None
        try:
            status = self.honeygain_user.get_honeypot_status()
            message = await HoneyGaneMessages.build_honeypot_status_message(status=status,
                                                                            last_open_time=last_open_time,
                                                                            next_open_time=next_open_time)
        except Exception as e:
            print(Fore.RED + "The user Honeygane was not previously authenticated. Performing authentication now.", e)
            try:
                self.honeygain_user.login(self.user, self.password)
                status = self.honeygain_user.get_honeypot_status()
                message = await HoneyGaneMessages.build_honeypot_status_message(status=status,
                                                                                last_open_time=last_open_time,
                                                                                next_open_time=next_open_time)
            except Exception as e:
                print(Fore.RED + "Failed to authenticate the Honeygane user. Please check the connection and "
                                 "authorization credentials.", e)
                message = HoneyGaneMessages.service_unavailable
        if self.handler:
            await self.handler(message)

    async def get_statistics(self):
        try:
            stats_today = self.honeygain_user.stats_today()
            stats_today_jt = self.honeygain_user.stats_today_jt()
            wallet_stats = self.honeygain_user.wallet_stats()
            message = await HoneyGaneMessages.build_statistics_message(wallet_stats=wallet_stats,
                                                                       stats_today=stats_today,
                                                                       stats_today_jt=stats_today_jt)
        except Exception as e:
            print(Fore.RED + "The user Honeygane was not previously authenticated. Performing authentication now.", e)
            try:
                self.honeygain_user.login(self.user, self.password)
                stats_today = self.honeygain_user.stats_today()
                stats_today_jt = self.honeygain_user.stats_today_jt()
                wallet_stats = self.honeygain_user.wallet_stats()
                message = await HoneyGaneMessages.build_statistics_message(wallet_stats=wallet_stats,
                                                                           stats_today=stats_today,
                                                                           stats_today_jt=stats_today_jt)
            except Exception as e:
                print(Fore.RED + "Failed to authenticate the Honeygane user. Please check the connection and "
                                 "authorization credentials.", e)
                message = HoneyGaneMessages.service_unavailable
        if self.handler:
            await self.handler(message)

    async def __unsafe_open_honeypot(self, status):
        if (status['progress_bytes'] == status['max_bytes']) & (status['winning_credits'] is None):
            result = self.honeygain_user.open_honeypot(retry_count=5, delay=2)
            winning_credits = result['credits']['credits']
            message = await HoneyGaneMessages.successful_opening(winning_credits=winning_credits)
            last_open_time = datetime.now()
            last_open_time = datetime.strptime(last_open_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            try:
                self.storage.update_data("timestamps", "last_open_time", last_open_time)
            except Exception as e:
                print(Fore.RED + "Failed to update the record in the database; attempting to create a new one.", e)
                self.storage.set_data("timestamps", "last_open_time", last_open_time)
            if self.handler:
                await self.handler(message)
            return True
        elif status['progress_bytes'] < status['max_bytes']:
            return False
        elif status['winning_credits'] > 0:
            if self.handler:
                winning_credits = status['winning_credits']
                message = await HoneyGaneMessages.opened_earlier(winning_credits=winning_credits)
                await self.handler(message)
            return True

    async def open_honeypot(self):
        try:
            status = self.honeygain_user.get_honeypot_status()
            return await self.__unsafe_open_honeypot(status=status)
        except Exception as e:
            print(Fore.RED + "The user Honeygane was not previously authenticated. Performing authentication now.", e)
            try:
                self.honeygain_user.login(self.user, self.password)
                status = self.honeygain_user.get_honeypot_status()
                return await self.__unsafe_open_honeypot(status=status)
            except Exception as e:
                print(Fore.RED + "Failed to authenticate the Honeygane user. Please check the connection and "
                                 "authorization credentials.", e)
                if self.handler:
                    message = HoneyGaneMessages.service_unavailable_with_timer(self.wait_to_recheck_status)
                    await self.handler(message)
                return False

    async def start(self):
        await self.wait(datetime.min)
        while True:
            is_opened = await self.open_honeypot() is True
            if is_opened:
                if 0 <= datetime.now().hour < 3:
                    next_open = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)
                else:
                    next_open = (datetime.now() + timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0)
            else:
                next_open = datetime.now() + timedelta(hours=self.wait_to_recheck_status)
                next_open = datetime.strptime(next_open.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            await self.wait(next_open)
