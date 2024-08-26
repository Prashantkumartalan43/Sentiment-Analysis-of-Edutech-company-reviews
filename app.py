#!/usr/bin/env python
# coding: utf-8

# In[6]:

!pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

file_path = 'C:/Users/pktal/Downloads/output_reviews.csv'
df = pd.read_csv(file_path)

# Page title
st.title('Review Analysis Dashboard')

df['review_datetime'] = pd.to_datetime(df['review_datetime'])
df['aspect_labels'] = df['aspect_labels'].apply(eval)

# Sidebar for platform selection
platforms = df['platform'].unique()
selected_platform = st.sidebar.selectbox('Select a platform', platforms)

# Filter DataFrame based on selected platform
df_filtered = df[df['platform'] == selected_platform]

# Visualization 1: Review Count by Month
st.subheader('Review Count by Month')
review_count_by_month = df_filtered['year_month'].value_counts().sort_index()
fig, ax = plt.subplots()
review_count_by_month.plot(kind='area', ax=ax)
ax.set_title('Review Count by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Review Count')
st.pyplot(fig)

# Visualization 3: Sentiment Distribution (Stacked Bar)
st.subheader('Sentiment Distribution')
sentiment_distribution = df_filtered.groupby(['year_month', 'sentiment']).size().unstack().fillna(0)
fig, ax = plt.subplots()
sentiment_distribution.plot(kind='area', stacked=True, ax=ax)
ax.set_title('Sentiment Distribution')
ax.set_xlabel('Month')
ax.set_ylabel('Review Count')
for p in ax.patches:
    ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() * 1.005))
st.pyplot(fig)

# Ensure the aspect_labels are evaluated properly
df_filtered.loc[:, 'aspect_labels'] = df_filtered['aspect_labels'].apply(lambda x: eval(str(x)))

# Visualization 4: Aspect Sentiment Heatmap
st.subheader('Aspect Sentiment Heatmap')
aspect_sentiment_counts = df_filtered.explode('aspect_labels').groupby(['aspect_labels', 'sentiment']).size().unstack(fill_value=0)
fig, ax = plt.subplots()
sns.heatmap(aspect_sentiment_counts, annot=True, cmap='YlGnBu', fmt='d', ax=ax)
st.pyplot(fig)


# In[ ]:




