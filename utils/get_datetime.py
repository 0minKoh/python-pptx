from datetime import datetime, timedelta

def _get_next_sunday():
    today = datetime.today()
    next_sunday = today + timedelta((6 - today.weekday()) % 7)
    return next_sunday

def _get_week_of_month(date):
    first_day = date.replace(day=1)
    first_day_weekday = first_day.weekday()
    adjusted_dom = date.day + first_day_weekday
    return (adjusted_dom - 1) // 7 + 1

def get_sunday_text():
    next_sunday = _get_next_sunday()
    year = next_sunday.year
    month = next_sunday.month
    week_of_month = _get_week_of_month(next_sunday)
    
    week_texts = ["첫째주", "둘째주", "셋째주", "넷째주", "다섯째주"]
    week_text = week_texts[week_of_month - 1]
    
    return f"( {year}년 {month}월 {week_text} )"