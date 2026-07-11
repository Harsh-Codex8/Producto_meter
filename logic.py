
# logic.py
ACTIVITY_CONFIG = {
    "Health": {"color": "#00FF00", "status": "+ve"},
    "Academics": {"color": "#0000FF", "status": "+ve"},
    "Skills": {"color": "#800080", "status": "+ve"},
    "School": {"color": "#FFA500", "status": "0"},
    "Sleep": {"color": "#00008B", "status": "0"},
    "Other": {"color": "#FFFF00", "status": "0"},
    "Screen": {"color": "#FF0000", "status": "-ve"}
}

def get_score_for_activity(activity, count):
    if activity == "Academics": return 50
    if activity == "Health": return max(20, 80 - (count * 10))
    if activity == "Skills": 
        scores = [60, 60, 50, 50, 40, 40, 30, 30]
        return scores[min(count-1, 7)]
    if activity == "Screen": 
        penalties = [-25, -25, -35, -35, -50, -50, -70, -70, -95, -95]
        return penalties[min(count-1, 9)]
    return 0