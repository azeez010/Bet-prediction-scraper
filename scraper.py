import requests
from bs4 import BeautifulSoup
import bs4
from random import choice
from pdf import make_pdf
from mail import send_email_with_attachment

html_content = requests.get("https://bettingtips1x2.com/index.php?page=tipsters", headers={'User-Agent': 'Mozilla/5.0'})
html = html_content.text

games_data = dict()
games_and_tips = []
unique_games = set()

def get_games(html):
    extracted_blocks_texts = []
    soup = BeautifulSoup(html, features="lxml")
    # Iterate over all divs, you could narrow this down if you had more information
    div = soup.findAll('div', {"class": "inner"})[4]
    # Iterate over the children of each matching div
    for c in div.children:
        # If it wasn't parsed as a tag, it may be a NavigableString
        if isinstance(c, bs4.element.NavigableString):
            if res := c.strip():
                extracted_blocks_texts.append(res)
    
    return extracted_blocks_texts[3:-2]  

def get_unique_games(games):
    unique_games = set()
    for game in games:
        unique_games.add(game)
    return unique_games

def get_games_data(games):
    games_data = dict()
    for index, game in enumerate(games):
        if ":" in game:
            get_game = games_data.get(game)
            if get_game:
                get_game[0] += 1
                get_game.append(index)
            else:
                games_data[game] = [1]
                games_data[game].append(index) 

    return games_data

all_games = get_games(html)
unique_games = get_unique_games(all_games)
games_data = get_games_data(all_games)

def predict():
    for index, i in enumerate(unique_games):
        data = games_data.get(i)
        if isinstance(data, list):
            game_len = data[0]
            if data:
                pred_to_dist = []
                pred_len = 0 
                while pred_len != game_len: 
                    try:
                        pred = input(f"{i} is repeated {game_len} times\n")
                        if ":" in pred:
                            preds = pred.split(":")
                            for each_pred in preds:
                                each = each_pred.split("-")
                                if len(each) > 1:
                                    each = each_pred.split("-")
                                    no = each[1]
                                    # print("no -> ", no)
                                    pred_len += int(no)
                                    pred_to_dist.append([each[0],  int(each[1])])
                                else:
                                    pred_len += 1
                                    pred_to_dist.append([each[0],  1])
                        else:
                            each = pred.split("-")
                            if len(each) > 1:
                                no = each[1]
                                pred_to_dist.append([each[0],  int(no)])
                                pred_len += int(no)

                        if game_len != pred_len:
                            pred_len = 0
                            pred_to_dist = []
                            print("\nEnter your prediction for predictions in this format => 1x-2:BTS-2, make sure the number lenght of total predictions are the same. \n")

                        games = data[1:]
                        for d in pred_to_dist:
                            pred_num = d[1]
                            prediction = d[0]
                            for r in range(pred_num):
                                game = choice(games)
                                team_name = all_games[game]
                                all_games[game] = [ team_name, prediction]
                                games.remove(game)
                                
                    except Exception as e:
                        print("\nEnter your prediction for predictions in this format => 1x-2:BTS-2, make sure the number lenght of total predictions are the same. \n")
                        continue

        print("Remaining numbers of games - {index}".format(index=len(unique_games) - index))
    return all_games

def main():
    print("Enter your predictions for each games in this format e.g. => 1x-2:BTS-2:X-1:1.5-2\n")
    predictions = predict()
    make_pdf(predictions)
    email = input("Enter your email to send pdf...\n")
    while "@" not in email:
        email = input("Enter your email to send pdf...")
    
    send_email_with_attachment(email)

main()