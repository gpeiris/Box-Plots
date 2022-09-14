import dash
from dash import dcc
from dash import html
from pandas.io.formats import style
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv("data/Data-PMS.csv")

leavesArray = ['UoM2.5mm','UoM5mm','UoM10mm']
DVH_arr = ['PTVD2','PTVD98','CI_RTOG100','ALPO','MUPerGy','HI']
xLabelArray = ['Dose [%]','Dose [%]','Conformity Index','Average Leaf Pair Opening [mm]','MU per Gy [MU/Gy]', 'Homogeneity Index']

# Initialise the app
app = dash.Dash(__name__)

# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_leaf):
        dict_list = []
        for i in list_leaf:
                dict_list.append({'label':i, 'value':i})
        return dict_list

# Define the app
app.layout = html.Div(children=[
	html.Div(className='row', # define the row element
		children=[
			html.Div(className='three columns div-user-controls',
				children=[
					html.H2('Box Plots For All Targets'),
					html.P('''Pick one or more leaf width to display'''),
					html.Div(className='div-for-dropdown',
						children=[
							dcc.Dropdown(id='siteselector',
								options=get_options(df['Site'].unique()),
								placeholder="Select an anatomical site",
                                                                multi=True,
								value=[df['Site'].sort_values()[0]],
								style={'backgroundColor':'#1E1E1E'},
								className='siteselector'
							)
						],
					style={'color':'#1E1E1E'}
					),
                                        html.P('''Pick one dose metric to view'''),
                                        html.Div(className='div-for-dropdown',
						children=[
							dcc.Dropdown(id='dvhselector',
								options=get_options(DVH_arr),
                                                                placeholder="Select a dose metric",
								multi=False,
								value=DVH_arr[0],
								style={'backgroundColor':'#1E1E1E'},
								className='dvhselector'
							),
						],
					style={'color':'#1E1E1E'}
					),
                                        
				]
			), # Define the left element
			html.Div(className='nine columns div-for-charts bg-grey',
				children=[
					dcc.Graph(id='25mm',
						config={'displayModeBar':False},
						animate=True
					),
                                        dcc.Graph(id='volumePlot',
                                                config={'displayModeBar':False},
						animate=True
                                        ),
				]
			), # Define the 2.5mm Box Plot 
		]
	)
])

@app.callback(Output('25mm','figure'),
			[Input('siteselector','value'),
                        Input('dvhselector','value')
			]
)
def update_25mm(site_dropdown_val, dose_met):
	trace = []
	for site in site_dropdown_val:
                df_sub = df[df['Site'] == site]
	for leaf in leavesArray:
                trace.append(go.Box(x=df_sub[df_sub['PlanID'] == leaf][dose_met],
                                opacity=0.7,
                                name=leaf,
					)
		)
                traces = [trace]
	data = [val for sublist in traces for val in sublist]
	figure={'data':data,
			'layout':go.Layout(
				colorway=[],
				template='plotly_dark',
				paper_bgcolor='rgba(0,0,0,0)',
				plot_bgcolor='rgba(0,0,0,0)',
				margin={'b':15},
				hovermode='x',
				autosize=True,
				title={'text': 'Box and Whisker Plot for '+dose_met+' (2.5mm leaf Width)','font':{'color':'white'},'x':0.5},
				xaxis={'title': xLabelArray[DVH_arr.index(dose_met)]},
	),
	}
	return figure

@app.callback(Output('volumePlot','figure'),
			[Input('siteselector','value'),
                        Input('dvhselector','value')
			]
)
def update_VolPlot(site_dropdown_val, dose_met):
	trace = []
	df_sub = pd.DataFrame([[0,0,0,0,0,0,0,0,0]],columns = ['PlanID','Site','PTVD2','PTVD98','CI_RTOG100','ALPO','MUPerGy','Volume','HI'])
	for site in site_dropdown_val:
                df_sub = df_sub.append(df[df['Site'] == site])
	for leaf in leavesArray:
                trace.append(go.Scatter(x=df_sub[df_sub['PlanID'] == leaf]['Volume'],
                                        y=df_sub[df_sub['PlanID'] == leaf][dose_met],
                                        mode='markers',
                                        opacity=0.7,
                                        name=leaf,
                                        textposition='bottom center'
					)
		)
                traces = [trace]
                min_vol = df_sub['Volume'][list(df_sub['Volume']).index(sorted(df_sub['Volume'])[1])]
                min_dmt = df_sub[dose_met][list(df_sub[dose_met]).index(sorted(df_sub[dose_met])[1])]
	data = [val for sublist in traces for val in sublist]
	figure={'data':data,
			'layout':go.Layout(
				colorway=[],
				template='plotly_dark',
				paper_bgcolor='rgba(0,0,0,0)',
				plot_bgcolor='rgba(0,0,0,0)',
				margin={'b':15},
				hovermode='x',
				autosize=True,
				title={'text': 'Volume v '+dose_met+' for Leaf Width','font':{'color':'white'},'x':0.5},
				yaxis={'title': xLabelArray[DVH_arr.index(dose_met)], 'range':[min_dmt*0.8,df_sub[dose_met].max()*1.2]},
                                xaxis={'title': 'Volume [cc]','range':[min_vol*0.8,df_sub['Volume'].max()+20]},
	),
	}
	return figure


if __name__ == "__main__":
    app.run_server()
