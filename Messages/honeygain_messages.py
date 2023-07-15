class HoneyGaneMessages:

    service_unavailable = "The service is currently unavailable. Try later."
    @staticmethod
    async def build_statistics_message(wallet_stats, stats_today, stats_today_jt):
        days = list(wallet_stats['data'].keys())
        last_day = wallet_stats['data'][days[len(days) - 1]]
        last_seven_days = days[len(days) - 7:]
        last_seven_hg_credits = 0
        last_seven_jt_credits = 0
        for day in last_seven_days:
            last_seven_hg_credits += wallet_stats['data'][day]['hg_credits']
            last_seven_jt_credits += wallet_stats['data'][day]['jt_credits']
        last_seven_days = {'hg_credits': round(last_seven_hg_credits, 2), 'jt_credits': round(last_seven_jt_credits,
                                                                                              2)}
        last_thirty_hg_credits = 0
        last_thirty_jt_credits = 0
        for day in days:
            last_thirty_hg_credits += wallet_stats['data'][day]['hg_credits']
            last_thirty_jt_credits += wallet_stats['data'][day]['jt_credits']
        last_thirty = {'hg_credits': round(last_thirty_hg_credits, 2), 'jt_credits': round(last_thirty_jt_credits,
                                                                                           2)}
        message = f"Wallet status 💵:\n" \
                  f"- Today's Honeygain 🍯 credits: {last_day['hg_credits']}\n" \
                  f"- Last 7 days' Honeygain 🍯 credits: {last_seven_days['hg_credits']}\n" \
                  f"- Last 30 days' Honeygain 🍯 credits: {last_thirty['hg_credits']}\n" \
                  f"- Today's JumpTask 🆙 credits: {last_day['jt_credits']}\n" \
                  f"- Last 7 days' JumpTask 🆙 credits: {last_seven_days['jt_credits']}\n" \
                  f"- Last 30 days' JumpTask 🆙 credits: {last_thirty['jt_credits']}\n" \
                  f"Stats for Honeygain 🍯 today:\n" \
                  f"- Total credits: {stats_today['total']['credits']}\n" \
                  f"- Winning credits: {stats_today['winning']['credits']}\n" \
                  f"- Referral credits: {stats_today['referral']['credits']}\n" \
                  f"- Gathering bytes: {stats_today['gathering']['bytes']}\n" \
                  f"- Gathering credits: {stats_today['gathering']['credits']}\n" \
                  f"- Other credits: {stats_today['other']['credits']}\n" \
                  f"Stats for JumpTask 🆙 today:\n" \
                  f"- Total credits: {stats_today_jt['total']['credits']}\n" \
                  f"- Winning credits: {stats_today_jt['winning']['credits']}\n" \
                  f"- Referral credits: {stats_today_jt['referral']['credits']}\n" \
                  f"- Bonus credits: {stats_today_jt['bonus']['credits']}\n" \
                  f"- Gathering bytes: {stats_today_jt['gathering']['bytes']}\n" \
                  f"- Gathering credits: {stats_today_jt['gathering']['credits']}\n" \
                  f"- Other credits: {stats_today_jt['other']['credits']}\n"
        return message

    @staticmethod
    async def build_honeypot_status_message(status, last_open_time, next_open_time):
        message = f"Progress bytes: {status['progress_bytes']}\n" \
                  f"Max bytes: {status['max_bytes']}\n" \
                  f"Winning credits: {status['winning_credits']}\n" \
                  f"Last opening time: {last_open_time}\n" \
                  f"Next opening time: {next_open_time}"
        return message

    @staticmethod
    async def wait_to_message(awake_time):
        return f"Wait to {awake_time}"

    @staticmethod
    async def successful_opening(winning_credits):
        return f"Opened successfully! Winning: {winning_credits}"

    @staticmethod
    async def opened_earlier(winning_credits):
        return f"Was opened earlier with the following profit: {winning_credits}"

    @staticmethod
    async def service_unavailable_with_timer(awake_hours):
        return f"The service is currently unavailable. The timer is set for {awake_hours} hours."
