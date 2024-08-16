import streamlit as st
import pandas as pd
import geopandas
import altair as alt
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_extras.stylable_container import stylable_container
from wordcloud import WordCloud, STOPWORDS
import string
import matplotlib.pyplot as plt
from io import StringIO
from datetime import datetime
import pytz
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
# from transformers import pipeline

nltk.download('punkt')

st.set_page_config(
    page_title="L'hotel HSMA",
    page_icon="💻",
    layout="wide")


##################################
# Data wrangling                 #
##################################
# This could be done in a separate file!

@st.cache_data
def get_hotel_data():
    hotel_df = pd.read_csv('hotels_subset.csv')

    min_date = datetime.strptime(hotel_df["reviews.date"].min(), '%Y-%m-%dT00:00:00Z')
    max_date = datetime.strptime(hotel_df["reviews.date"].max(), '%Y-%m-%dT00:00:00Z')

    hotel_df['reviews.date'] =  pd.to_datetime(hotel_df['reviews.date'])

    hotel_df['month_year'] = hotel_df['reviews.date'].dt.strftime('%Y-%m-01')

    hotel_df['reviews_stars'] = hotel_df["reviews.rating"].case_when([
        (hotel_df["reviews.rating"] == 1, "⭐"),
        (hotel_df["reviews.rating"] == 2, "⭐⭐"),
        (hotel_df["reviews.rating"] == 3, "⭐⭐⭐"),
        (hotel_df["reviews.rating"] == 4, "⭐⭐⭐⭐"),
        (hotel_df["reviews.rating"] == 5, "⭐⭐⭐⭐⭐")
    ])

    hotel_df['reviews_stars_date'] = hotel_df.apply(lambda x: f"{x['reviews_stars']} \n {x['reviews.date'].strftime('%d %b %Y')}", axis=1)

    hotel_df['reviews.text'] = hotel_df['reviews.text'].str.wrap(40)

    return hotel_df, min_date, max_date


hotel_df, min_date, max_date = get_hotel_data()

hotel_df_full = hotel_df.copy()

def get_topics(lda_model, num_words=10):

    topic_list = []
    for idx, topic in lda_model.print_topics(-1, num_words):
        words = [(word.split("*")[1].replace('"', '').strip(), float(word.split("*")[0]))
                 for word in topic.split(" + ")]
        word_list = []
        for word, weight in words:
            word_list.append(word)

        topic_list.append(f"Topic {idx+1}: {', '.join(word_list)}")

    return "\n\n".join(topic_list)


def make_wordcloud(text_input, **kwargs):
    tokens = text_input.split()
    punctuation_mapping_table = str.maketrans('', '', string.punctuation)
    tokens_stripped_of_punctuation = [token.translate(punctuation_mapping_table)
                                  for token in tokens]
    lower_tokens = [token.lower() for token in tokens_stripped_of_punctuation]

    joined_string = (" ").join(lower_tokens)

    plt.figure(figsize=(30,40))
    wordcloud = WordCloud(width=1800,
                height=1800,
                stopwords=stopwords,
                **kwargs).generate(joined_string)
    plt.imshow(wordcloud)

    # Turn off axes
    plt.axis("off")

    return plt.gcf()


##################################
# Dashboard Code                 #
##################################

# Setup styling with CSS

st.markdown(
'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@200&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');

html, body, st-emotion-cache [class*="css"] {
    font-family: 'Lexend', sans-serif;
    font-size: 12px;
    font-weight: 200;
    color: #091747;
}

h1, h2, h3, h4 {
    font-family: "Audiowide", sans-serif;
}

.block-container {
    width: 100%;
    padding: 1rem 2rem 2rem;
    min-width: auto;
    max-width: initial;
}

</style>
''' , unsafe_allow_html= True)

st.title("L'hotel HSMA - Brand Performance")

col_input_1, col_input_2, col_input_3 = st.columns([0.4, 0.1, 0.5])

with col_input_1:
    hotel_filter = st.selectbox("Filter to an Individual Hotel", hotel_df.name.unique(), index=None)

with col_input_3:
    date_filter = st.slider("Filter to a Date Range",
                            min_date,
                            max_date,
                            (min_date,
                            max_date)
                            )

if hotel_filter is not None:
    hotel_df = hotel_df[hotel_df['name'] == hotel_filter]

hotel_df = hotel_df[
    (hotel_df["reviews.date"] <= date_filter[1].astimezone(pytz.timezone('US/Eastern')).isoformat()) &
    (hotel_df["reviews.date"] >= date_filter[0].astimezone(pytz.timezone('US/Eastern')).isoformat())]

#############################################
# Update data for filter                    #
#############################################

review_summaries_all = (hotel_df_full.groupby(['name', 'latitude', 'longitude'])[['reviews.rating']]
                    .agg(['mean', 'count'])
                    .droplevel(0, axis=1).reset_index()
                    )
if hotel_filter is not None:
    review_summaries = review_summaries_all[review_summaries_all["name"] == hotel_filter]
else:
    review_summaries = review_summaries_all.copy()

review_summary_gdf = geopandas.GeoDataFrame(
    review_summaries, # Our pandas dataframe
    geometry = geopandas.points_from_xy(
        review_summaries['longitude'], # Our 'x' column (horizontal position of points)
        review_summaries['latitude'] # Our 'y' column (vertical position of points)
        ),
    crs = 'EPSG:4326' # the coordinate reference system of the data - use EPSG:4326 if you are unsure
    )

geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in review_summary_gdf.geometry]

# Map
# Make the empty map
if hotel_filter is None:
    hotel_map_interactive = folium.Map(
        location=[33, -100],
        zoom_start=4,
        tiles='cartodbdark_matter',
        )
else:
    hotel_map_interactive = folium.Map(
        location=[hotel_df.head(1).latitude.values[0], hotel_df.head(1).longitude.values[0]],
        zoom_start=6,
        tiles='cartodbdark_matter',
        )

# Add markers to the map
for coordinates in geo_df_list:
    hotel_map_interactive = hotel_map_interactive.add_child(
        folium.Marker(
            location=coordinates,
            icon=folium.Icon(icon="bed", prefix='fa', color="purple")
            )
    )


###########################################
# Build out the dashboard                 #
###########################################

tab1, tab2, tab3 = st.tabs(["Overview", "Review Summaries", "All Reviews"])

with tab1:

    col1, col2, col3 = st.columns([0.15, 0.5, 0.35])


    with col1:
        min_date = hotel_df_full['reviews.date'].max() - pd.DateOffset(months=6)
        hotel_df_full_recent = hotel_df_full[hotel_df_full['reviews.date'] >= min_date]
        review_summaries_recent = (hotel_df_full_recent.groupby(['name', 'latitude', 'longitude'])[['reviews.rating']]
                        .agg(['mean', 'count'])
                        .droplevel(0, axis=1).reset_index()
                        )

        with stylable_container(key="best_p", css_styles="""
                                body {background-color: lightblue;
                                padding: 20px;
                                border-radius: 10px;}
                                """):

            st.subheader("Worst 5 performers in last 6 months")
            bottom_5 = review_summaries_recent.sort_values('mean').reset_index().head(5)
            for idx, item in bottom_5.iterrows():
                st.write(f":orange[{idx+1}:  {item["name"]}: {item["mean"]:.2f}]")

        with stylable_container(key="worst_p", css_styles="""
                                background-color: lightblue;
                                padding: 20px;
                                border-radius: 10px;
                                """):
            st.subheader("Best 5 performers in last 6 months")
            top_5 = review_summaries_recent.sort_values('mean').reset_index().tail(5).sort_values('mean', ascending=False)
            for idx, item in top_5.iterrows():
                st.write(f":green[{idx+1}:  {item["name"]}: {item["mean"]:.2f}]")

    with col2:
        good_reviews = hotel_df[hotel_df["reviews.rating"] >=4]
        bad_reviews = hotel_df[hotel_df["reviews.rating"] <=2]
        neutral_reviews = hotel_df[hotel_df["reviews.rating"] ==3]

        st.write(f"{len(good_reviews)} good reviews, {len(neutral_reviews)} neutral reviews and {len(bad_reviews)} bad reviews")

        st.subheader("Review Distribution")
        if hotel_filter is None:
            st.plotly_chart(
                px.histogram(
                    hotel_df,
                    x='reviews.rating',
                    range_x=[1,5],
                    nbins=5,
                    height=300
                    )
            )
        else:
            hotel_df["What"] = hotel_filter
            hotel_df_full["What"] = "All Hotels"
            st.plotly_chart(
                px.histogram(
                    pd.concat([hotel_df, hotel_df_full]),
                    x='reviews.rating',
                    barmode="overlay",
                    histnorm='probability',
                    opacity=0.7,
                    range_x=[1,5],
                    color="What",
                    nbins=5,
                    height=300
                    )
            )



        reviews_monthly = pd.DataFrame(hotel_df.groupby('month_year')['reviews.rating'].mean().round(2)).reset_index()

        st.subheader("Average Monthly Reviews Over Time")
        if hotel_filter is None:
            st.plotly_chart(
                px.line(reviews_monthly,
                        x='month_year',
                        y="reviews.rating",
                        range_y=[1,5],
                        markers=True,
                        height=300)
            )
        else:
            reviews_monthly_all = pd.DataFrame(hotel_df_full.groupby('month_year')['reviews.rating'].mean().round(2)).reset_index()
            reviews_monthly_all["What"] = "All Hotels"
            reviews_monthly["What"] = hotel_filter
            st.plotly_chart(
                px.line(pd.concat([reviews_monthly, reviews_monthly_all]),
                        x='month_year',
                        y="reviews.rating",
                        color="What",
                        range_y=[1,5],
                        markers=True,
                        height=300)
            )

        st_folium(hotel_map_interactive, use_container_width=True)



    with col3:
        st.subheader("Most Recent Reviews")

        review_display = hotel_df.sort_values('reviews.date', ascending=False).head(10).reset_index()[['name', 'reviews_stars_date', 'reviews.text']]
        review_display.rename(columns={"name": "Hotel", "reviews_stars_date": "Rating", "reviews.text":"Review"}, inplace=True)
        review_display.index += 1
        st.table(review_display)

with tab2:
    stopwords = list(STOPWORDS)
    stopwords.extend(["hotel", "room", "stay", "us", "I"])
    stopwords = set(stopwords)

    # @st.cache_resource
    # def get_summarizer_model():
    #     summarizer_model = pipeline("summarization", "mabrouk/amazon-review-summarizer-bart")
    #     return pipeline("summarization", model=summarizer_model)

    # summarizer = get_summarizer_model()

    if hotel_filter is not None:
        wc_cols = st.columns(3)
        review_dfs = [bad_reviews, neutral_reviews, good_reviews]
        what = ["Bad Reviews (2 stars or below)", "Neutral Reviews (3 star)", "Good Reviews (4 or above)"]

        for idx, col in enumerate(wc_cols):
            col.text(f"{len(review_dfs[idx])} {what[idx]}")

            col.pyplot(
                make_wordcloud(text_input=" ".join(review_dfs[idx]['reviews.text'].astype('str').tolist()))
            )

            reviews_list = review_dfs[idx]["reviews.text"].tolist()
            def preprocess(text):
                tokens = word_tokenize(text.lower())
                return [token for token in tokens if token.isalnum() and token not in stopwords]
            processed_docs = [preprocess(doc) for doc in reviews_list]
            dictionary = corpora.Dictionary(processed_docs)
            corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
            num_topics = 2
            lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42)

            col.write("Topics found by LDA model:")
            col.write(get_topics(lda_model))

            # st.write(summarizer(" ".join(reviews_list), min_length = 60, max_length=250))

            temp_df = review_dfs[idx].rename(columns={"name": "Hotel", "reviews_stars_date": "Rating", "reviews.text":"Review"}).sort_values('reviews.date', ascending=False).reset_index()[["Hotel", "Rating", "Review"]]
            temp_df.index += 1
            col.table(temp_df)
    else:
        st.write("Please select a single hotel to generate wordclouds")

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        star_filter = st.slider("Select the number of stars", 1, 5, (1, 5))
        hotel_df = hotel_df[hotel_df['reviews.rating'] >= star_filter[0]]
        hotel_df = hotel_df[hotel_df['reviews.rating'] <= star_filter[1]]

    with col_b:
        city_filter = st.selectbox("Select a city", hotel_df.city.unique(), index=None)
        if city_filter is not None:
            hotel_df = hotel_df[hotel_df['city'] == city_filter]

    st.write(f"Hotels Selected: {len(hotel_df.name.unique())} ")
    st.write(f"Total Reviews: {len(hotel_df)} ")

    st.dataframe(hotel_df.sort_values('reviews.date', ascending=False)[['name', 'city', 'reviews.date', 'reviews.text', 'reviews_stars']], use_container_width=True)
