import requests
from bs4 import BeautifulSoup
import random
import streamlit as st
from time import sleep

# Function to scrape quotes
def scrape_quotes():
    all_quotes = []
    base_url = "http://quotes.toscrape.com/"
    url = "/page/1"
    while url:
        res = requests.get(f"{base_url}{url}")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(1)
    return all_quotes

# Main function for the Streamlit app
def main():
    st.title("Quote Guessing Game")

    if "quotes" not in st.session_state:
        st.session_state.quotes = scrape_quotes()
        st.session_state.quote = random.choice(st.session_state.quotes)
        st.session_state.remaining_guesses = 4
        st.session_state.hints = []

    quote = st.session_state.quote
    remaining_guesses = st.session_state.remaining_guesses

    st.write("Here's a quote:")
    st.write(quote["text"])

    guess = st.text_input(f"Who said this quote? Guesses remaining: {remaining_guesses}", "")

    if guess:
        if guess.lower() == quote["author"].lower():
            st.success("CONGRATULATIONS!!! YOU GOT IT RIGHT")
        else:
            st.session_state.remaining_guesses -= 1
            remaining_guesses = st.session_state.remaining_guesses
            if remaining_guesses == 3:
                res = requests.get(f"http://quotes.toscrape.com{quote['bio-link']}")
                soup = BeautifulSoup(res.text, "html.parser")
                birth_date = soup.find(class_="author-born-date").get_text()
                birth_place = soup.find(class_="author-born-location").get_text()
                st.session_state.hints.append(f"Hint: The author was born on {birth_date} {birth_place}.")
            elif remaining_guesses == 2:
                st.session_state.hints.append(f"Hint: The author's first name starts with: {quote['author'][0]}.")
            elif remaining_guesses == 1:
                last_initial = quote["author"].split(" ")[1][0]
                st.session_state.hints.append(f"Hint: The author's last name starts with: {last_initial}.")
            else:
                st.error(f"Sorry, you ran out of guesses. The answer was {quote['author']}.")
    
    if st.session_state.hints:
        for hint in st.session_state.hints:
            st.write(hint)

    if remaining_guesses == 0 or guess.lower() == quote["author"].lower():
        if st.button("Play Again"):
            st.session_state.quote = random.choice(st.session_state.quotes)
            st.session_state.remaining_guesses = 4
            st.session_state.hints = []

# Run the Streamlit app
if __name__ == "__main__":
    main()
