import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

palette = ['#00f5c4','#4da6ff','#f5a623','#ff4d6d','#a78bfa','#34d399','#fb7185']

def build_pie_chart(df):
    fig1 = px.pie(df, names="category", values="amount", hole=0.55, color_discrete_sequence=palette)
    fig1.update_traces(
        textposition='inside', textinfo='percent',
        pull=[0.04]*len(df['category'].unique()),
        marker=dict(line=dict(color='rgba(10,13,20,0.4)', width=2)),
        hovertemplate="<b>%{label}</b><br>₹%{value}<br>%{percent}<extra></extra>"
    )
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='DM Sans'),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(color='#6b7a99')),
        margin=dict(t=20,b=20,l=20,r=20),
        hoverlabel=dict(bgcolor="#141926", font_color="#00f5c4", font_size=14, font_family="Space Mono"),
        transition={'duration': 600, 'easing': 'cubic-in-out'}
    )
    return fig1

def build_bar_chart(df):
    monthly = df.groupby('category')['amount'].sum().reset_index()
    fig2 = px.bar(monthly, x="category", y="amount", text="amount",
                    color="category", color_discrete_sequence=palette)
    fig2.update_traces(
        texttemplate='₹%{text:.2s}', textposition='outside',
        marker=dict(line=dict(color='rgba(0,0,0,0.2)', width=1)),
        hovertemplate="<b>%{x}</b><br>₹%{y}<extra></extra>"
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='DM Sans'), showlegend=False,
        xaxis=dict(showgrid=False, title="", tickfont=dict(color='#6b7a99')),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', title="", tickfont=dict(color='#6b7a99')),
        margin=dict(t=30,b=10,l=0,r=0),
        hoverlabel=dict(bgcolor="#141926", font_color="#00f5c4", font_size=14),
        transition={'duration': 600, 'easing': 'cubic-in-out'}
    )
    return fig2

def build_trend_chart(df):
    trend = df.reset_index()
    fig3 = px.line(trend, x="index", y="amount", markers=True)
    fig3.update_traces(
        line=dict(width=3, color='#00f5c4', shape='spline'),
        marker=dict(size=7, color='#00f5c4', line=dict(width=2, color='#0a0d14')),
        fill='tozeroy', fillcolor='rgba(0,245,196,0.07)',
        hovertemplate="Entry %{x} · ₹%{y}<extra></extra>"
    )
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='DM Sans'),
        xaxis=dict(showgrid=False, title="", showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', title="", tickfont=dict(color='#6b7a99')),
        hovermode="x unified", margin=dict(t=10,b=10,l=0,r=0),
        hoverlabel=dict(bgcolor="#141926", font_color="#00f5c4", font_size=14, font_family="Space Mono"),
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    return fig3

def build_anomaly_chart(df, thr):
    fig_dist = px.histogram(df, x="amount", nbins=20, color_discrete_sequence=['#00f5c4'])
    fig_dist.add_vline(x=thr, line_dash="dash", line_color="#ff4d6d", annotation_text="Danger Zone", annotation_position="top right")
    fig_dist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#6b7a99', family='Space Mono'),
        xaxis=dict(showgrid=False, title="Amount Density"), yaxis=dict(showgrid=False, title="", showticklabels=False),
        margin=dict(t=30,b=10,l=0,r=0), height=220, showlegend=False,
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    return fig_dist

def build_forecast_chart(df):
    # Using real ML with polyfit
    base = df['amount'].mean()
    y = df['amount'].values
    x = np.arange(len(y))
    
    if len(y) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        next_x = np.arange(len(y), len(y) + 14)
        preds = p(next_x)
        # ensure positive 
        preds = np.clip(preds, a_min=1, a_max=None)
    else:
        # fallback if not enough points
        preds = [base]*14
        
    momentum = ((preds[-1] - base) / base) * 100 if base > 0 else 0
    pf = pd.DataFrame({'Day': [f"+{i}" for i in range(1,15)], 'Predicted': preds})
    
    fp = px.line(pf, x="Day", y="Predicted", markers=True)
    fp.update_traces(
        line=dict(width=2.5, color='#f5a623', shape='spline'),
        marker=dict(size=6, color='#f5a623', line=dict(width=2, color='#0a0d14')),
        fill='tozeroy', fillcolor='rgba(245,166,35,0.07)'
    )
    fp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='DM Sans'),
        xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', title=""),
        margin=dict(t=10,b=10,l=0,r=10), hovermode="x unified", height=200,
        hoverlabel=dict(bgcolor="#141926", font_color="#f5a623", font_size=14),
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    return fp, momentum

def build_drift_chart(drift_df):
    fig_drift = px.bar(drift_df, x="category", y="Drift", color="Drift", 
                        color_continuous_scale=[[0, '#00f5c4'], [0.5, '#141926'], [1, '#ff4d6d']],
                        text_auto='.2s')
    fig_drift.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8ecf4', family='DM Sans'), coloraxis_showscale=False,
        xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', title=""),
        margin=dict(t=10,b=10,l=0,r=0), height=240,
        transition={'duration': 800, 'easing': 'cubic-in-out'}
    )
    return fig_drift

def build_gauge_chart(spent, budget):
    pct = (spent / budget)*100 if budget > 0 else 0
    gauge_col = "#00f5c4" if pct <= 100 else "#ff4d6d"

    fig_gauge = go.Indicator(
        mode = "gauge+number+delta",
        value = spent,
        delta = {'reference': budget, 'position': "top", 'relative': False, 'valueformat': '.0f'},
        number = {'valueformat': '.0f', 'font': {'size': 44, 'family': "Space Mono", 'color': gauge_col}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, max(spent, budget)*1.1], 'tickwidth': 1, 'tickcolor': "#6b7a99"},
            'bar': {'color': gauge_col},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, budget], 'color': 'rgba(255,255,255,0.03)'},
                {'range': [budget, max(spent, budget)*1.1], 'color': 'rgba(255,77,109,0.1)'}
            ],
            'threshold': {
                'line': {'color': "#ff4d6d", 'width': 4},
                'thickness': 0.75,
                'value': budget
            }
        }
    )
    layout_gauge = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#6b7a99", 'family': "DM Sans"},
        margin=dict(t=40, b=0, l=40, r=40), height=300,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    return go.Figure(data=[fig_gauge], layout=layout_gauge)

def build_burn_chart(df, budget):
    burn_df = df.copy()
    burn_df['cumulative'] = burn_df['amount'].cumsum()
    burn_df['status'] = burn_df['cumulative'].apply(lambda x: 'Safe' if x <= budget else 'Breached')
    
    fig_burn = px.area(burn_df.reset_index(), x="index", y="cumulative", 
                        color="status", color_discrete_map={'Safe': '#00f5c4', 'Breached': '#ff4d6d'})
    
    fig_burn.add_shape(
        type="line", line=dict(color="rgba(255,255,255,0.4)", width=2, dash="dash"),
        x0=0, x1=len(burn_df)-1, y0=budget, y1=budget
    )
    
    fig_burn.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#6b7a99', family='DM Sans'),
        xaxis=dict(showgrid=False, title="Transaction Timeline"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', title="Total Spent (₹)"),
        margin=dict(t=20,b=10,l=0,r=0), height=240, showlegend=False,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    return fig_burn
