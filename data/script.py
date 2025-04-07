# to store the wikipedia articles
import wikipediaapi


def get_wikipedia_text(title):
    wiki_wiki = wikipediaapi.Wikipedia("MyProjectName (merlin@example.com)", "en")
    page = wiki_wiki.page(title)

    if not page.exists():
        print(f"The page '{title}' does not exist.")
        return None

    return page.text


if __name__ == "__main__":

    films = [
        "The_Color_of_Money",
        "The_Last_Temptation_of_Christ",
        "Goodfellas",
        "Cape_Fear",
        "The_Age_of_Innocence",
        "Casino",
        "Kundun",
        "Bringing_Out_the_Dead",
        "Gangs_of_New_York",
        "The_Aviator",
        "The_Departed",
        "Shutter_Island",
        "Hugo",
        "The_Wolf_of_Wall_Street",
        "Silence",
        "The_Irishman",
        "Killers_of_the_Flower_Moon",
        "Italianamerican",
        "American_Boy_A_Profile_of_Steven_Prince",
        "The_Last_Waltz",
        "My_Voyage_to_Italy",
        "Public_Speaking",
        "George_Harrison_Living_in_the_Material_World",
        "Rolling_Thunder_Revue_A_Bob_Dylan_Story_by_Martin_Scorsese",
        "What's_a_Nice_Girl_Like_You_Doing_in_a_Place_Like_This",
    ]

    for title in films:
        text = get_wikipedia_text(title)

        if text:
            with open(f"{title}.txt", "w", encoding="utf-8") as file:
                file.write(text)
            print("Wikipedia article saved as 'martin_scorsese.txt'")
