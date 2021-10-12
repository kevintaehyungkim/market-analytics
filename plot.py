'''
https://www.python-graph-gallery.com/

# Seaborn Violin Plot
https://seaborn.pydata.org/generated/seaborn.violinplot.html
https://seaborn.pydata.org/examples/grouped_violinplots.html

# Overlap Scatter Plot on top of violin plot
https://stackoverflow.com/questions/59358115/add-one-specific-datapoint-marker-to-boxplot-or-violinplot-using-holoviews-hv

Plotly 

# Subtitle
https://towardsdatascience.com/a-clean-style-for-plotly-charts-250ba2f5f015

# Subplots 
https://plotly.com/python/subplots/
https://plotly.com/python/v3/table-subplots/

# Pie Chart
https://plotly.com/python/pie-charts
'''

import sys, time
import option_analytics as option_analytics
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

from datetime import datetime
from plotly.subplots import make_subplots
from pytz import timezone


OI_TICK_COUNT = 0
MAX_PAIN_TICK_COUNT = 0
OPTION_ANALYTICS_TICK_COUNT = 12
OI_TICK_COUNT = 15
MAX_PAIN_TICK_COUNT = 20
INTERVALS = [1, 5, 10, 20, 25, 40, 50, 100, 200]

COLORS = {
	'AQUA': '#7DCDD5',
	'DARK1': '#1E1F24',
	'DARK2': '#61D3D3',
	'GREEN': 'rgb(108,189,191)',
	'ORANGE': 'rgb(242,165,103)',
	'RED': 'rgb(219,119,132)',
	'BLUE_LIGHT': 'rgb(132,198,245)',
	'WHITE': 'rgb(255,255,255)'
}

# pio.templates.default = 'dark'

def generate_plots(symbol, days=30):
	option_chain_data = option_analytics.find_all_implied_prices(symbol, 0, int(days))

	# option chain - analytics plot
	generate_option_analytics_plot(symbol, option_chain_data)

	# option chain - oi by strike and max pain plot
	generate_oi_plot(symbol, option_chain_data)

	return 


def generate_option_analytics_plot(symbol, option_data):

	x = list(option_data.keys())
	x_rev = x[::-1]

	oi_implied_prices = []
	vol_implied_prices = []
	max_pain_prices = []

	yc, yc_upper, yc_lower = [], [], []
	yp, yp_upper, yp_lower = [], [], []

	for option_expiry in option_data.keys():
		oi_top_strikes_calls = [float(i) for i in option_data[option_expiry][0][1][0]]
		oi_top_strikes_puts = [float(i) for i in option_data[option_expiry][0][2][0]]

		oi_implied_prices.append(option_data[option_expiry][0][0])
		vol_implied_prices.append(option_data[option_expiry][1])
		max_pain_prices.append(option_data[option_expiry][2][0])

		yc.append(oi_top_strikes_calls[0])
		yc_upper.append(max(oi_top_strikes_calls))
		yc_lower.append(min(oi_top_strikes_calls))

		yp.append(oi_top_strikes_puts[0])
		yp_upper.append(max(oi_top_strikes_puts))
		yp_lower.append(min(oi_top_strikes_puts))

	yc_lower = yc_lower[::-1]
	yp_lower = yp_lower[::-1]

	all_y = yc_upper+yc_lower+yp_upper+yp_lower
	y_min, y_max = min(all_y), max(all_y)
	y_dtick = find_dtick(y_min, y_max, OPTION_ANALYTICS_TICK_COUNT)


	fig = go.Figure()

    #########################
    #########################

	fig.add_trace(go.Scatter(
	    x=x+x_rev,
	    y=yc_upper+yc_lower,
	    fill='toself',
	    fillcolor='rgba(108,189,191,0.15)',
	    line_color='rgba(255,255,255,0)',
	    showlegend=False,
	    mode='lines',
	    name='Call OI',
	))
	fig.add_trace(go.Scatter(
	    x=x+x_rev,
	    y=yp_upper+yp_lower,
	    fill='toself',
	    fillcolor='rgba(219,119,132,0.15)',
	    line_color='rgba(255,255,255,0)',
	    mode='lines',
	    name='Put OI',
	    showlegend=False,
	))

	fig.add_trace(go.Scatter(
	    x=x, y=yc,
	    line_color='rgb(108,189,191)',
	    mode='lines+markers',
	    name='Call Wall',
	    marker=dict(symbol="circle", size=3)
	))
	fig.add_trace(go.Scatter(
	    x=x, y=yp,
	    line_color='rgb(219,119,132)',
	    mode='lines+markers',
	    name='Put Wall',
	    marker=dict(symbol="circle", size=3)
	))
	fig.add_trace(go.Scatter(
	    x=x, y=oi_implied_prices,
	    line_color='rgb(132,198,245)',
		mode='lines+markers',
	    name='OI Implied Price',
	    marker=dict(
	    	size=7.5
            # line=dict(
            #     color='white',
            #     width=0.75
            # )
        )
	))
	fig.add_trace(go.Scatter(
	    x=x, y=vol_implied_prices,
	    line_color='rgb(242,165,103)',
		mode='lines+markers',
	    name='Vol Implied Price',
	    marker=dict(
	    	size=7.5
            # line=dict(
            #     color='#F9E5AD',
            #     width=0.75
            # )
        )
	))
	fig.add_trace(go.Scatter(
	    x=x, y=max_pain_prices,
	    line_color='rgb(255,255,255)',
		mode='markers',
	    name='Max Pain',
	    marker=dict(symbol="diamond", size=7)
	))

	#########################
    #########################

	# fig.update_traces(mode='lines')

	# Fix Zoom Ratio 
	fig.update_yaxes(scaleanchor = "x", scaleratio = 1)
	fig.update_yaxes(
		dtick=y_dtick,
		tickprefix="$",
        title_text="Strike",
        title_font={"size": 20},
        title_standoff = 25
	)

	fig.update_xaxes(
        title_text = "Option Expiry",
        title_font = {"size": 20},
        title_standoff = 25)

	# Set figure title
	symbol_bold = '<b>' + symbol + "</b>"
	fig.update_layout(template='plotly_dark')
	fig.update_layout(title_text=format_title(symbol_bold + " Option Analytics", "Updated: " + get_updated_time()), title_font = {"size": 24})
	fig.update_layout(margin=dict(
		l=140, 
		r=140, 
		b=140, 
		t=140, 
		pad=4)
	)

	fig.layout.plot_bgcolor = '#1E1F24'
	fig.layout.paper_bgcolor = '#1E1F24'

	fig.update_xaxes(title_font_color='#7DCDD5')
	fig.update_yaxes(title_font_color='#7DCDD5')

	# Display Plot
	fig.show()

	return 



def generate_oi_plot(symbol, option_data):

	major_expiry = ""
	max_oi_sum = 0
	call_strikes, call_strike_oi = [], []
	put_strikes, put_strike_oi = [], []
	max_pain_strikes, max_pain_premiums = [], []

	for option_expiry in option_data.keys():
		call_oi = option_data[option_expiry][0][1][1].values()
		put_oi = option_data[option_expiry][0][2][1].values()
		oi_sum = sum(call_oi) + sum(put_oi)

		if oi_sum > max_oi_sum:
			max_oi_sum = oi_sum
			major_expiry = option_expiry

	major_expiry_data = option_data[major_expiry][0]

	for call_strike in major_expiry_data[1][1].keys():
		call_strikes.append(int(float(call_strike)))
		call_strike_oi.append(major_expiry_data[1][1][call_strike])

	for put_strike in major_expiry_data[2][1].keys():
		put_strikes.append(int(float(put_strike)))
		put_strike_oi.append(major_expiry_data[2][1][put_strike])

	for strike in option_data[major_expiry][2][1].keys():
		max_pain_strikes.append(strike)
		max_pain_premiums.append(option_data[major_expiry][2][1][strike])

	expiry_date = major_expiry[:2] + '/' + major_expiry[3:5]
	max_pain_strike = option_data[major_expiry][2][0]

	fig = make_subplots(
	    rows=2, cols=1,
	    subplot_titles=(
	    	"<b>" + symbol + " " + expiry_date +  " Open Interest By Strike</b>", 
	    	"<b>" + symbol + " " + expiry_date + " Max Pain</b>")
	    )

	#################
	# Open Interest #
	#################
	fig.add_trace(
		go.Bar(
			x=call_strikes, 
			y=call_strike_oi,
			marker_color='#5CC99A',
			name='Call OI',
            marker_line_width=0.2,
			width=0.6,
			showlegend=False,
		), row=1, col=1)
	fig.add_trace(
		go.Bar(
			x=put_strikes, 
			y=put_strike_oi,
			name='Put OI',
			marker_color='rgb(219,119,132)',
			marker_line_width=0.2,
			width=0.6,
			showlegend=False
		), row=1, col=1)

	############
	# Max Pain #
	############
	fig.add_trace(
		go.Scatter(
			x=max_pain_strikes, 
			y=max_pain_premiums, 
			name='Total Premium',
			showlegend=False,
		), 
		row=2, col=1
	)
	fig.add_vline(
		x=max_pain_strike, 
		name='Max Pain',
		line_width=0.5,
		line_color=COLORS['ORANGE'],
		row=2, col=1
	)


	fig.update_layout(height=850, width=950)

	fig.update_yaxes(
		tickprefix="$",
	    title_text="Total Premium",
	    title_font={"size": 16},
	    title_standoff = 20,
	    row=2, col=1
	)

	fig.update_xaxes(
		dtick=find_dtick(min(call_strikes), max(call_strikes), MAX_PAIN_TICK_COUNT),
        title_text="Strike",
        title_font={"size": 16},
        title_standoff = 20,
        row=2, col=1
	)

	fig.update_yaxes(
	    title_text="Open Interest",
	    title_font={"size": 16},
	    title_standoff = 20,
	    row=1, col=1
	)

	fig.update_xaxes(
		dtick=find_dtick(min(call_strikes), max(call_strikes), OI_TICK_COUNT),
        title_text="Strike",
        title_font={"size": 16},
        title_standoff = 20,
        row=1, col=1
	)

	symbol_bold = '<b>' + symbol + "</b>"

	fig.layout.plot_bgcolor = '#1E1F24'
	fig.layout.paper_bgcolor = '#1E1F24'

	fig.update_layout(template='plotly_dark')
	fig.update_layout(title_text=format_title(symbol_bold + " Option Analytics", "Updated: " + get_updated_time()), title_font = {"size": 24})

	fig.update_xaxes(title_font_color='#7DCDD5')
	fig.update_yaxes(title_font_color='#7DCDD5')

	fig.update_layout(margin=dict(
		l=130, 
		r=60, 
		b=100, 
		t=140, 
		pad=4)
	)

	fig.show()

	return


#########
# utils #
#########

def find_dtick(min_val, max_val, num_intervals):
	interval = (max_val-min_val)/num_intervals
	dtick = find_nearest(INTERVALS, interval)

	return dtick


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def format_title(title, subtitle=None, subtitle_font_size=13):
    title = f'<b>{title}</b>'
    if not subtitle:
        return title
    subtitle = f'<span style="color:#D6D6D6; font-size: {subtitle_font_size}px;">{subtitle}</span>'
    return f'{title}<br>{subtitle}'


def get_updated_time():
	tz = timezone('US/Eastern')
	date_now = datetime.now(tz) 
	time_str = date_now.strftime("%b %d %Y %H:%M UTC-4").upper()

	return time_str



########################
### temporary script ###
########################
'''
- stock symbol
- days until expiry

ex. python3 plot.py SPY 21
'''
generate_plots(sys.argv[1], sys.argv[2])


