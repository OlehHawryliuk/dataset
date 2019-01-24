import re
import plotly
import plotly.graph_objs as go
input_file = 'C:\\mydataset\\Sourse\\athlete_events.csv'


def get_element(string, index):
    string = string.strip().split(',')
    if string[index]:
        element = string[index]
    return element

def get_city(string, keys):
    city_index = keys.index("City")
    city = get_element(string, city_index)
    city = re.findall(r"\w+\ {0,1}\w+\ {0,1}\w+", city)[0]
    return city

def get_date(string, keys):
    date_index = keys.index("Year")
    date = get_element(string, date_index)
    date = re.findall(r"\d{4}", date)[0]

    return  date

def get_sport(string, keys):
    sport_index = keys.index("Sport")
    sport = get_element(string, sport_index)
    sport = re.findall(r"\w+\ {0,1}\w+\ {0,1}\w+", sport)[0]
    return  sport

def add_city(City,dataset):
    if City not in dataset:
        dataset[City] = {}
    return dataset

def add_date(City, Date, dataset):
    if Date not in dataset[City]:
        dataset[City][Date] = set()
    return dataset

def add_sport(City, Date, Sport, dataset):
    if Sport not in dataset[City][Date]:
        dataset[City][Date].add(Sport)
    return dataset

def get_scatter_lists(dataset, list_data = [], list_counts= []):
    for keys in dataset:
        for values in dataset[keys]:
            if values not in list_data:
                list_data.append(values)
                list_counts.append(len(dataset[keys][values]))
            else:
                list_counts.insert(list_data.index(values),list_counts.pop(list_data.index(values)) + int(len(dataset[keys][values])))
    list_data.sort()
    list_counts.sort()
    return list_data , list_counts

def get_bar_list(dataset, list_country = [], list_sport_counts = []):
    for keys in dataset:
        for values in dataset[keys]:
            if keys not in list_country:
                list_country.append(keys)
                list_sport_counts.append(len(dataset[keys][values]))
            else:
                list_sport_counts.insert(list_country.index(keys), list_sport_counts.pop(list_country.index(keys)) + int(len(dataset[keys][values])))
    return list_country, list_sport_counts

def get_pie_list(dataset, sport_list = [], fame_sport = [] ):
    for country in dataset:
        for data in dataset[country]:
            for sport in dataset[country][data]:
               if sport not in sport_list:
                   sport_list.append(sport)
                   fame_sport.append(1)
               else:
                   fame_sport.insert(sport_list.index(sport), fame_sport.pop(sport_list.index(sport)) + 1)
    return sport_list , fame_sport

def build_scatter(list_counts, list_data):
    Scatter = go.Scatter(
        x = list_data,
        y = list_counts
    )
    plotly.offline.plot([Scatter])
    pass

def build_bar(list_country,list_sport_counts):
    Bar = go.Bar(
        x = list_country,
        y = list_sport_counts
    )
    plotly.offline.plot([Bar])

def build_pie(sport_list , fame_sport):
    Pie = go.Pie(
        labels = sport_list,
        values = fame_sport
    )
    plotly.offline.plot([Pie])

with open(input_file, encoding = 'utf-8', mode = 'r') as file:
    keys = file.readline()
    keys = keys.replace('"','').split(',')
    dataset = dict()
    count = 1
    while count < 100 :

        City = get_city(file.readline(), keys)
        Date = get_date(file.readline(), keys)
        Sport = get_sport(file.readline(), keys)
        #print(City, Sport, Date)
        dataset = add_city(City, dataset)
        dataset = add_date(City, Date, dataset)
        dataset = add_sport(City, Date, Sport, dataset)
        count += 1

#list_data, list_counts = get_scatter_lists(dataset)
#build_scatter(list_counts, list_data)

#list_country , list_sport_counts = get_bar_list(dataset)
#build_bar(list_country , list_sport_counts)

#sport_list , fame_sport = get_pie_list(dataset)
#build_pie(sport_list , fame_sport)

#print(dataset)