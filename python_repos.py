import requests
import pygal
from pygal.style import LightColorizedStyle, LightenStyle

url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
r = requests.get(url)
print("status code:", r.status_code)

response_dict = r.json()

print(response_dict.keys())

# 研究有关仓库的信息
repo_dicts = response_dict['items']
print("Repositories returned:", len(repo_dicts))
#print("\nSelected information about each repository:")

names, plot_dicts = [], []

for repo_dict in repo_dicts:
    names.append(repo_dict["name"])
    #plot_dict=repo_dict["stargazers_count"]
    if repo_dict["description"]:
        plot_dict = {'value':repo_dict["stargazers_count"],
                     'label':repo_dict["description"],
                     'xlink':repo_dict['html_url']}
    else:
        plot_dict = {'value':repo_dict["stargazers_count"],
                     'label':"None",
                     'xlink':repo_dict['html_url']}
    plot_dicts.append(plot_dict)

    #print('Name:', repo_dict['name'])
    #print('Owner:', repo_dict['owner']['login'])
    #print('Stars:', repo_dict['stargazers_count'])
    #print('Repository:', repo_dict['html_url'])
    #print('Created:', repo_dict['created_at'])
    #print('Updated:', repo_dict['updated_at'])
    #print('Description:', repo_dict['description'])

my_style = LightenStyle("#336699", base_style = LightColorizedStyle)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 20
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style = my_style)
chart.title = "Most-Starred Python Projects on GitHub"
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file("python_repos.svg")

