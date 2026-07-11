import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from logic import ACTIVITY_CONFIG, get_score_for_activity

st.set_page_config(layout="wide")
st.title("Daily Productivity Tracker (18h Active)")

# Initialize state
if 'timeline' not in st.session_state:
    st.session_state.timeline = ["Other"] * 36

# The "Bar" UI
# Replace your column loop with this logic:
for i, col in enumerate(cols):
    with col:
        if i >= 24: # Last 6 hours (12 slots)
            st.selectbox("", ["Sleep"], key=f"slot_{i}", disabled=True)
        else:
            st.session_state.timeline[i] = st.selectbox(
                "", list(ACTIVITY_CONFIG.keys()), 
                key=f"slot_{i}", 
                index=list(ACTIVITY_CONFIG.keys()).index(st.session_state.timeline[i]),
                label_visibility="collapsed"
            ) 
# Calculation Logic
data = []
counts = {act: 0 for act in ACTIVITY_CONFIG}
curr_score = 0
for act in st.session_state.timeline:
    counts[act] += 1
    score = get_score_for_activity(act, counts[act])
    curr_score += score
    data.append({"Activity": act, "Score": score, "Cumulative": curr_score})

df = pd.DataFrame(data)

# Visualization
fig = go.Figure()
fig.add_trace(go.Bar(x=list(range(36)), y=df["Score"], 
                     marker_color=[ACTIVITY_CONFIG[a]["color"] for a in df["Activity"]], 
                     name="Score Change"))
fig.add_trace(go.Scatter(x=list(range(36)), y=df["Cumulative"], 
                         mode='lines+markers', line=dict(color='white', width=3), 
                         name="Cumulative Trend"))

fig.update_layout(template="plotly_dark", title="Productivity Progress", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Metric Display
st.metric("Total Daily Score", curr_score)

# Add this after the visualization section
st.subheader("Data Management")
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Today's Log as CSV",
    data=csv,
    file_name='daily_productivity_log.csv',
    mime='text/csv',
)

# Insert this into your Plotly figure setup in app.py
fig.add_hline(y=500, line_dash="dash", line_color="green", annotation_text="Daily Goal")
