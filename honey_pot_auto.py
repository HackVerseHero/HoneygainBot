import asyncio
from datetime import datetime, timedelta
from pyHoneygain import HoneyGain
from Messages.honeygain_messages import HoneyGaneMessages


class HoneypotCatchBot:
    def __init__(self, user, password, storage, handler=None, wait_to_recheck_status=1, awake_to_catch_time=6):
        self.storage = storage
        self.handler = handler
        self.user = user
        self.password = password
        self.honeygain_user = HoneyGain()
        self.wait_to_recheck_status = wait_to_recheck_status
        self.awake_to_catch_time = awake_to_catch_time

    async def wait(self, awake_time):
        current_date = datetime.now()
        awake_to_catch_time = current_date + timedelta(hours=awake_time)
        old_awake_to_catch_time = datetime.min
        try:
            old_awake_to_catch_time = self.storage.get_data("timestamps", "awake_to_catch_time")
            old_awake_to_catch_time = datetime.strptime(old_awake_to_catch_time, '%Y-%m-%d %H:%M:%S.%f')
        except:
            pass
        if old_awake_to_catch_time < awake_to_catch_time:
            try:
                self.storage.set_data("timestamps", "awake_to_catch_time", awake_to_catch_time)
            except:
                self.storage.update_data("timestamps", "awake_to_catch_time", awake_to_catch_time)
        else:
            awake_to_catch_time = old_awake_to_catch_time
        if self.handler:
            formatted_awake_time = awake_to_catch_time.strftime("%Y-%m-%d %H:%M:%S")
            message = await HoneyGaneMessages.wait_to_message(formatted_awake_time)
            await self.handler(message)
        while True:
            try:
                awake_to_catch_time = self.storage.get_data("timestamps", "awake_to_catch_time")
                awake_to_catch_time = datetime.strptime(awake_to_catch_time, '%Y-%m-%d %H:%M:%S.%f')
            except:
                pass
            if awake_to_catch_time <= datetime.now():
                break
            await asyncio.sleep(1)

    async def reset_timers(self):
        new_awake_time = datetime.now() + timedelta(hours=self.awake_to_catch_time)
        try:
            self.storage.set_data("timestamps", "awake_to_catch_time", new_awake_time)
        except:
            self.storage.update_data("timestamps", "awake_to_catch_time", new_awake_time)

    async def get_honeypot_status(self):
        try:
            last_open_time = self.storage.get_data("timestamps", "last_open_time")
            last_open_time = datetime.strptime(last_open_time, '%Y-%m-%d %H:%M:%S.%f')
            last_open_time = last_open_time.strftime("%Y-%m-%d %H:%M:%S")
        except:
            last_open_time = None
        try:
            next_open_time = self.storage.get_data("timestamps", "awake_to_catch_time")
            next_open_time = datetime.strptime(next_open_time, '%Y-%m-%d %H:%M:%S.%f')
            next_open_time = next_open_time.strftime("%Y-%m-%d %H:%M:%S")
        except:
            next_open_time = None
        try:
            status = self.honeygain_user.get_honeypot_status()
            message = await HoneyGaneMessages.build_honeypot_status_message(status=status,
                                                                            last_open_time=last_open_time,
                                                                            next_open_time=next_open_time)
        except:
            try:
                self.honeygain_user.login(self.user, self.password)
                status = self.honeygain_user.get_honeypot_status()
                message = await HoneyGaneMessages.build_honeypot_status_message(status=status, last_open_time=last_open_time,
                                                                          next_open_time=next_open_time)
            except:
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
        except:
            try:
                self.honeygain_user.login(self.user, self.password)
                stats_today = self.honeygain_user.stats_today()
                stats_today_jt = self.honeygain_user.stats_today_jt()
                wallet_stats = self.honeygain_user.wallet_stats()
                message = await HoneyGaneMessages.build_statistics_message(wallet_stats=wallet_stats,
                                                                           stats_today=stats_today,
                                                                           stats_today_jt=stats_today_jt)
            except:
                message = HoneyGaneMessages.service_unavailable
        if self.handler:
            await self.handler(message)

    async def __unsafe_open_honeypot(self, status):
        if (status['progress_bytes'] == status['max_bytes']) & (status['winning_credits'] is None):
            result = self.honeygain_user.open_honeypot(retry_count=5, delay=2)
            winning_credits = result['credits']['credits']
            message = await HoneyGaneMessages.successful_opening(winning_credits=winning_credits)
            last_open_time = datetime.now()
            try:
                self.storage.set_data("timestamps", "last_open_time", last_open_time)
            except:
                self.storage.update_data("timestamps", "last_open_time", last_open_time)
            if self.handler:
                await self.handler(message)
            return True
        elif status['progress_bytes'] < status['max_bytes']:
            await self.wait(self.wait_to_recheck_status)
            await self.open_honeypot()
            return False
        elif status['winning_credits'] > 0:
            if self.handler:
                winning_credits = status['winning_credits']
                message = await HoneyGaneMessages.opened_earlier(winning_credits=winning_credits)
                await self.handler(message)
            return False

    async def open_honeypot(self):
        try:
            self.honeygain_user.login(self.user, self.password)
            status = self.honeygain_user.get_honeypot_status()
            return await self.__unsafe_open_honeypot(status=status)
        except:
            try:
                status = self.honeygain_user.get_honeypot_status()
                return await self.__unsafe_open_honeypot(status=status)
            except:
                if self.handler:
                    message = HoneyGaneMessages.service_unavailable_with_timer(self.awake_to_catch_time)
                    await self.handler(message)

    async def start(self):
        await self.wait(0)
        while True:
            await self.open_honeypot()
            await self.wait(self.awake_to_catch_time)
