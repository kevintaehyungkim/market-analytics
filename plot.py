'''
https://www.python-graph-gallery.com/

# Seaborn Violin Plot
https://seaborn.pydata.org/generated/seaborn.violinplot.html
https://seaborn.pydata.org/examples/grouped_violinplots.html


# Overlap Scatter Plot on top of violin plot
https://stackoverflow.com/questions/59358115/add-one-specific-datapoint-marker-to-boxplot-or-violinplot-using-holoviews-hv

# Plotly Subtitle
https://towardsdatascience.com/a-clean-style-for-plotly-charts-250ba2f5f015
'''

import sys, time
import option_analytics as option_analytics
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

from datetime import datetime
from pytz import timezone


OI_TICK_COUNT = 0
MAX_PAIN_TICK_COUNT = 0
OPTION_ANALYTICS_TICK_COUNT = 12
Y_INTERVALS = [1, 5, 10, 20, 25, 40, 50, 100, 200]

# pio.templates.default = 'dark'


def generate_plot(symbol, days):
	option_data = option_analytics.find_all_implied_prices(symbol, 0, int(days))

	x = list(option_data.keys())
	x_rev = x[::-1]

	oi_implied_prices = []
	vol_implied_prices = []
	max_pain_prices = []

	yc, yc_upper, yc_lower = [], [], []
	yp, yp_upper, yp_lower = [], [], []

	for option_expiry in option_data.keys():
		oi_top_strikes_calls = [float(i) for i in option_data[option_expiry][0][1]]
		oi_top_strikes_puts = [float(i) for i in option_data[option_expiry][0][2]]

		oi_implied_prices.append(option_data[option_expiry][0][0])
		vol_implied_prices.append(option_data[option_expiry][1])
		max_pain_prices.append(option_data[option_expiry][2])

		yc.append(oi_top_strikes_calls[0])
		yc_upper.append(max(oi_top_strikes_calls))
		yc_lower.append(min(oi_top_strikes_calls))

		yp.append(oi_top_strikes_puts[0])
		yp_upper.append(max(oi_top_strikes_puts))
		yp_lower.append(min(oi_top_strikes_puts))

	yc_lower = yc_lower[::-1]
	yp_lower = yp_lower[::-1]

	y_dtick = find_y_dtick(yc_upper+yc_lower, yp_upper+yp_lower, OPTION_ANALYTICS_TICK_COUNT)


	fig = go.Figure()

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
	fig.update_layout(title_text=format_title(symbol_bold + " Option Chain Analytics", "Last Updated: " + get_updated_time()), title_font = {"size": 24})
	fig.update_layout(margin=dict(
		l=140, 
		r=140, 
		b=140, 
		t=140, 
		pad=4)
	)

	# # plot 2 
	# fig.add_trace(
 #    	go.Scatter(
	#         x=[1,2,3],
	#         y=[1,2,3],
	#         mode="lines",
	#         name="mining revenue"
	#     ),
	#     row=3, col=1
	# )	


	# Background Color
		#1: 61D3D3
		#2: 1E1F24
	fig.layout.plot_bgcolor = '#1E1F24'
	fig.layout.paper_bgcolor = '#1E1F24'

	fig.update_xaxes(title_font_color='#7DCDD5')
	fig.update_yaxes(title_font_color='#7DCDD5')

	fig.show()

	return 

'''
{
'2021-10-11': [
	[
		435.2319871852145, # oi implied price
		['442.0', '440.0', '443.0', '438.0', '439.0'], # oi most traded call strikes
		['430.0', '440.0', '437.0', '435.0', '428.0']  # oi most traded put strikes
	], 
	437.0], # optimal expiry

'2021-10-13': [
	[
		432.82019647376774, 
		['445.0', '440.0', '441.0', '442.0', '436.0'], 
		['430.0', '434.0', '431.0', '425.0', '415.0']
	], 
	438.0]
}
'''
def find_y_dtick(y_calls, y_puts, num_intervals):
	y_all = y_calls + y_puts
	y_gmax, y_gmin = max(y_all), min(y_all)

	y_interval = (y_gmax-y_gmin)/num_intervals
	y_dtick = find_nearest(Y_INTERVALS, y_interval)

	return y_dtick


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def format_title(title, subtitle=None, subtitle_font_size=14):
    title = f'<b>{title}</b>'
    if not subtitle:
        return title
    subtitle = f'<span style="font-size: {subtitle_font_size}px;">{subtitle}</span>'
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

ex. python3 plot.py SPY 30
'''
generate_plot(sys.argv[1], sys.argv[2])


