#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Feature-processing" data-toc-modified-id="Feature-processing-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Feature processing</a></span></li><li><span><a href="#Create-Sankey-Diagram" data-toc-modified-id="Create-Sankey-Diagram-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Create Sankey Diagram</a></span></li></ul></div>

# In[1]:


import plotly.graph_objects as go
import pandas as pd 


# In[8]:


df = pd.read_csv('/Users/aurelie.giraud/Downloads/migrations.csv')


# ## Feature processing

# In[11]:


df.rename(columns= {'from':'source', 'to':'target'}, inplace=True)
df2 = df.groupby(['source', 'target']).agg({'company':'count'}).reset_index()
df2 = df2[df2['source'] != '?']
df2 = df2[df2['source'] != 'Unknown']
df2 = df2[~df2['source'].str.contains('/')]
df2 = df2[~df2['target'].str.contains('/')]
df2['target'] = df2['target'].replace('TypeScript+Prisma+tRPC', 'TypeScript')
df2['target'] = df2['target'].replace('PostgreSQL+Kubernetes', 'PostgreSQL')
df2['target'] = df2['target'].replace('NodeJS+PostgreSQL', 'NodeJS')
df2['source'] = df2['source'].replace('ElsticSearch+LogStash+Kibana', 'ElasticSearch')
df2['source'] = df2['source'].replace('Golang+MongoDB','Golang')
df2['source'] = df2['source'].replace('C/C++', 'C++')


# ## Create Sankey Diagram

# In[66]:


# Define the nodes and links for the Sankey diagram
nodes = list(set(df2['source'].unique()) | set(df2['target'].unique()))
links = []
for i, row in df2.iterrows():
    links.append(dict(
        source=row['source'],
        target=row['target'],
        value=row['company']
    ))



# Define the Sankey diagram layout
layout = go.Layout(
    font=dict(size=10),
    width=800,
    height=800,
)

# Create the Sankey diagram figure
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
    ),
    link=dict(
        source=[nodes.index(link['source']) for link in links],
        target=[nodes.index(link['target']) for link in links],
        value=[link['value'] for link in links],
    )
)], layout=layout)

# Display the Sankey diagram
fig.show()

