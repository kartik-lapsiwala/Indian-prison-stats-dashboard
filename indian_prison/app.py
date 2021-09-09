import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("/Users/user/Desktop/python_stuff/dashboard/Experiments/dash_experiment/indian_prison/Caste.csv")
df.head()

def dropdown():
    return html.Div([dcc.Dropdown(id='dropdown',
                                  options=[{'label': i, 'value': i} for i in df["state_name"].unique()],
                                  value="Gujarat")]
                    ,className="dropdown")

app.layout = dbc.Container([dcc.Store(id="store"),
                            dbc.Row([dbc.Col([html.Div("Indian Prison Stats between 2001-2013", className="heading")])]),
                            dbc.Row([dbc.Col(dropdown())]),
                            dcc.Tabs(id="tabs", value="convicts", className="custom-tabs-container", children=[dcc.Tab(label="Convicts", value="convicts"),
                                                                                                               dcc.Tab(label="under_trial",value="under_trial"),
                                                                                                               dcc.Tab(label="detenues", value="detenues")]),
                            dbc.Row(dbc.Col(html.Div(id="tab-content")))])


@app.callback(Output("tab-content", "children"),
             [Input("tabs", "value"),
              Input("store", "data")])

def render_tabs(value, data):
    if value == "convicts":
        return dcc.Graph(id="graph1_convicts", figure=data["gender_convicts"]),html.Br(), dcc.Graph(id="graph2_convicts", figure=data["caste_convicts"])
    elif value=="under_trial":
        return dcc.Graph(id="graph1_under_trial", figure=data["gender_under_trial"]), html.Hr(), dcc.Graph(id="graph2_under_trial", figure=data["caste_under_trial"])
    elif value=="detenues":
        return dcc.Graph(id="graph1_detenues", figure=data["gender_detenues"]), html.Hr(), dcc.Graph(id="graph2_detenues", figure=data["caste_detenues"])

@app.callback(Output("store", "data"),
              Input("dropdown", "value"))

def generate_graphs(dropdown):
    # df1_convicts has only convicts column kept, rest all removed, and groupby is done on gender column
    df1_convicts = df[df["state_name"]==dropdown]
    df1_convicts = df1_convicts.drop(["is_state", "caste", "under_trial", "detenues", "others"], axis=1)
    df1_convicts = df1_convicts.groupby(['state_name', "year", "gender"])['convicts'].sum().reset_index()

    # df2_convicts has only convicts column kept, rest all removed, and groupby is done on caste column
    df2_convicts = df[df["state_name"]==dropdown]
    df2_convicts = df2_convicts.drop(["is_state", "gender", "under_trial", "detenues", "others"], axis=1)
    df2_convicts = df2_convicts.groupby(["state_name", "year", "caste"])["convicts"].sum().reset_index()

    # df1_under_trial has only under_trial column kept, rest all removed, and groupby is done on gender column
    df1_under_trial = df[df["state_name"]==dropdown]
    df1_under_trial = df1_under_trial.drop(["is_state", "caste", "convicts", "detenues", "others"], axis=1)
    df1_under_trial = df1_under_trial.groupby(['state_name', "year", "gender"])['under_trial'].sum().reset_index()

    # df2_under_trial has only under_trial column kept, rest all removed, and groupby is done on caste column
    df2_under_trial = df[df["state_name"]==dropdown]
    df2_under_trial = df2_under_trial.drop(["is_state", "gender", "convicts", "detenues", "others"], axis=1)
    df2_under_trial = df2_under_trial.groupby(["state_name", "year", "caste"])["under_trial"].sum().reset_index()

    # df1_detenues has only detenues column kept, rest all removed, and groupby is done on gender column
    df1_detenues = df[df["state_name"]==dropdown]
    df1_detenues = df1_detenues.drop(["is_state", "caste", "convicts", "under_trial", "others"], axis=1)
    df1_detenues = df1_detenues.groupby(['state_name', "year", "gender"])['detenues'].sum().reset_index()

    # df2_under_trial has only under_trial column kept, rest all removed, and groupby is done on caste column
    df2_detenues = df[df["state_name"]==dropdown]
    df2_detenues = df2_detenues.drop(["is_state", "gender", "convicts", "under_trial", "others"], axis=1)
    df2_detenues = df2_detenues.groupby(["state_name", "year", "caste"])["detenues"].sum().reset_index()


    gender_convicts = px.bar(df1_convicts, x="year", y="convicts", color="gender", title="gender distribution of convicts",
                            color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)
    caste_convicts = px.bar(df2_convicts, x="year", y="convicts", color="caste", title="caste distribution of convicts",
                            color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)

    gender_under_trial = px.bar(df1_under_trial, x="year", y="under_trial", color="gender", title="gender distribution of under_trial",
                                color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)
    caste_under_trial = px.bar(df2_under_trial, x="year", y="under_trial", color="caste", title="caste distribution of under_trial",
                                color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)

    gender_detenues = px.bar(df1_detenues, x="year", y="detenues", color="gender", title="gender distribution of detenues",
                            color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)
    caste_detenues = px.bar(df2_detenues, x="year", y="detenues", color="caste", title="caste distribution of detenues",
                            color_discrete_sequence=px.colors.qualitative.Set1, opacity=0.6)

    return {"gender_convicts":gender_convicts, "caste_convicts":caste_convicts,
            "gender_under_trial":gender_under_trial, "caste_under_trial":caste_under_trial,
            "gender_detenues":gender_detenues, "caste_detenues":caste_detenues}


if __name__ == '__main__':
    app.run_server(debug=True, port=5050)
