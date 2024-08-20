import streamlit as st

st.write("Let's try loading in a variable from the previous page.")

with st.expander("Click here to see the code that made the homepage"):
    st.code("""
            import streamlit as st

st.set_page_config(layout="wide", page_title="Homepage")

st.title("Welcome to the penguin app!")

species_options = ["Gentoo", "Chinstrap", "Adelie"]

chosen_species = st.selectbox("Which penguin species are you interested in finding out more about?", species_options)

if chosen_species == "Gentoo":
    st.write(
        '''
        The gentoo penguin (JEN-too) (Pygoscelis papua) is a penguin species (or possibly a species complex) in the genus Pygoscelis, most closely related to the Adélie penguin (P. adeliae) and the chinstrap penguin (P. antarcticus). The earliest scientific description was made in 1781 by Johann Reinhold Forster with a type locality in the Falkland Islands. The species calls in a variety of ways, but the most frequently heard is a loud trumpeting, which the bird emits with its head thrown back.
        '''
    )
elif chosen_species == "Chinstrap":
    st.write(
        '''
The chinstrap penguin (Pygoscelis antarcticus) is a species of penguin that inhabits a variety of islands and shores in the Southern Pacific and the Antarctic Oceans. Its name stems from the narrow black band under its head, which makes it appear as if it were wearing a black helmet, making it easy to identify.[2] Other common names include ringed penguin, bearded penguin, and stonecracker penguin, due to its loud, harsh call.[3]
        '''
    )

elif chosen_species == "Adelie":
    st.write(
        '''
        The Adélie penguin (Pygoscelis adeliae) is a species of penguin common along the entire coast of the Antarctic continent, which is the only place where it is found. It is the most widespread penguin species, and, along with the emperor penguin, is the most southerly distributed of all penguins. It is named after Adélie Land, in turn, named for Adèle Dumont d'Urville, who was married to French explorer Jules Dumont d'Urville, who first discovered this penguin in 1840. Adélie penguins obtain their food by both predation and foraging, with a diet of mainly krill and fish.
        '''
    )

st.markdown("*All information from wikipedia*")
""")

st.write("We're going to try loading the `species_options` list in, which just contains the strings 'Gentoo', 'Adelie' and 'Chinstrap'.")

st.write("What we'll see is that it doesn't work and instead returns an error. This is because the variables on the other pages are completely separate and can't be accessed on this page.")

st.write("This is a key thing to be aware of within multipage apps. Without using things like session state, we can't use information from other pages on this page, and vice-versa")

chosen_species = st.selectbox("Which penguin species are you interested in finding out more about?", species_options)
