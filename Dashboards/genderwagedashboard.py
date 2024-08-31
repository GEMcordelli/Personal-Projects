import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import plotly.figure_factory as ff
import dash
#import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# ourdata
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

#ourdata celanup
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

# setting up sub dfs for dashbaord dropdowns
means = gss_clean.groupby('sex').agg({'income' : 'mean', 'job_prestige' : 'mean', 'socioeconomic_index' : 'mean', 'education' : 'count'})
means = means.round(2)
mb_sex=gss_clean.groupby(['male_breadwinner','sex']).agg({'sex' : 'count'})
mb_sex = mb_sex.rename({'sex' : 'count'}, axis = 1)
mb_sex=mb_sex.reset_index()
inc_sex=gss_clean.groupby(['income','sex', 'job_prestige', 'education']).agg({'sex' : 'count'})
inc_sex = inc_sex.rename({'sex' : 'count'}, axis = 1)
inc_sex=inc_sex.reset_index()
gss_subset = gss_clean[["income", "sex","job_prestige"]]
bins = [16, 29, 42, 55, 68, 81]
labels = ["low", "moderate", "high", "very high", "top tier"]
gss_subset["job_prestige_rating"] = pd.cut(gss_subset.job_prestige, bins, labels = labels)

# initialize dashboard

myapp = dash.Dash(__name__, external_stylesheets = external_stylesheet)


# Initial Population (empty tabs)

myapp.layout = html.Div(
    [
        html.H1("GSS: The Gender-Pay Gap"),

        dcc.Tabs(
            [dcc.Tab(label = "Demographic-Gender Statistics: Foundations of Disparity", children = [
                dcc.Markdown("According to the Pew Research Institute, the gender-wage gap is a very real phenomena; one whose metrics have changed little in the last 20 eyars. That is to say, in 2002, women earned an average of 80% of that which men earned, based on the median income salary, and in 2022, according to Pew Research, that gap has jumpe donly to 82%. The disparity between male-female compensation is widest when looking at employees of all ages (16 and up), however we see a shrinking of the gap when isolating to the ages of 25-34. The gender-pay gap has been historically sited to many measureable factors such as education and job-gender segrgeation. This is indicative of the interaction between social norms, historical systems of sexism, and the gender-pay gap. While the criminalization of pay discrimmination initiated over a half century ago, the existence and effects of the gender-pay gap persist. The severity of the effects exist on a race-based gradient and , according to the American Association of University Women, projections for the move towrds pay equality exist at extremely different rates across race. Whith Black and Hispanic women seeing change as a markedley slower rate than WHite and Asian women. Additonally, the AAUW undescores the importance of where you live and what you do. There are regional trends in overall income, ad the strength of disparity across gender. Occupation and its perceived importance and required skill level are also importnant factoer, which may be interepreted differently for men and women. The General Social Survey is a full-probability, personal survey meant to measure the complexity of American social characteristics and attitudes. It has been in operation for the last 5 decades, and here, we will utilize the 2022 iteration to delve deeper into the gender-pay gap. The questions surveyed by the GSS have been optimized after each iteration for the last 80 years, to garner the most accurate and comparative information about behavioral, attitudinal and social behaviors in the United States. The GSS strives to provide easily accessible data for scholars, students, policymakers and more."),
                dcc.Markdown("Please Select a Variable:"),
                dcc.Dropdown(id='varselect', 
                             options = means.columns,
                             value = "Variable of Interest"),

             html.Div([dcc.Graph(id = "table")],
                      style = {'width' : '60%', 'float' : 'right'})]),

             dcc.Tab(label = "Male Breadwinner: How do people feel about the notion of women in the home and men in the office?", children = [
                dcc.Markdown("Please Select 'sex':"),
                dcc.Dropdown(id='varselect2', 
                             options = mb_sex.columns,
                             value = "Variable of Interest"),
             
             html.Div([dcc.Graph(id = "bar")], 
                      style = {'width' : '60%', 'float' : 'left'})]),

             dcc.Tab(label = "Income & Prestige Across Gender: How are jobs percieved and compensated?", children = [
                dcc.Markdown("Please Select 'sex':"),
                dcc.Dropdown(id='varselect3', 
                             options = gss_clean.columns,
                             value = "Variable of Interest"),

             html.Div([dcc.Graph(id = "scatter"), 
                 dcc.Graph(id = "box")],
                 style = {'width' : '60%', 'float' : 'left'})]),

             dcc.Tab(label = "Do Prestigous Jobs Look Different for Men and Women?", children = [
                dcc.Markdown("Please Select 'job_prestige_rating':"),
                dcc.Dropdown(id='varselect4', 
                             options = gss_subset.columns,
                             value = "Variable of Interest"),

             html.Div([dcc.Graph(id = "box2")],
                 style = {'width' : '60%', 'float' : 'left'})])

            ]
        )
    ]
)      

@myapp.callback(Output(component_id = "table", component_property = "figure"), [Input(component_id = "varselect", component_property = "value")])

def maketable(col):
    df = means
    table = ff.create_table(means)
    return table


@myapp.callback(Output(component_id = "bar", component_property = "figure"), [Input(component_id = "varselect2", component_property = "value")])

def makebar(col):
    df = mb_sex
    bar = px.bar(mb_sex, x = "male_breadwinner", y = "count", color = col, text = "count", labels={'male_breadwinner':'Survey Results for Agreement with Male as Sole Provider'})
    return bar

@myapp.callback(Output(component_id = "scatter", component_property = "figure"), [Input(component_id = "varselect3", component_property = "value")])

def makescatter(col):
    fig = px.scatter(gss_clean, x = "job_prestige", y = "income", color = col, hover_data = ["education", "socioeconomic_index"], trendline = "lowess", labels = {'job_prestige' : 'job prestige'})
    return fig

@myapp.callback(Output(component_id = "box", component_property = "figure"), [Input(component_id = "varselect3", component_property = "value")])

def makebox(col):
    fig = px.box(gss_clean, x = "sex", y = "income", color = col, labels = {"sex" : ""})
    fig2 = px.box(gss_clean, x = "sex", y = "job_prestige", color = col, labels = {"job_prestige" : "job prestige score", "sex" : ""})
    fig2 = fig2.update_layout(showlegend = False)
    fig = fig.update_layout(showlegend = False)
    return fig

@myapp.callback(Output(component_id = "box2", component_property = "figure"), [Input(component_id = "varselect4", component_property = "value")])

def makebox2(col):
    fig3 = px.box(gss_subset, x = "sex", y = "job_prestige", facet_col = col)
    fig3.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_rating=", "")))
    return fig3   


if __name__ == '__main__':
    myapp.run_server(debug = True, port=8008)
    