from urllib.request import urlopen
from bs4 import BeautifulSoup #Documentation: https://pypi.org/project/beautifulsoup4/
import pandas as pd
import matplotlib.pyplot as plt #Documentation: https://matplotlib.org/3.3.2/api/
import numpy as np

plt.style.use('seaborn') #Using a style called seaborn for plots
fig, ax = plt.subplots() #Create a figure and a set of subplots.

annot = ax.annotate("", xy=(0,0), xytext=(-100,-25),textcoords="offset points") #Blank annotation
annot.set_visible(False) #Sets plot annotation to invisible

class PlayerStats():
    def __init__(self, year):
        self.year = year
        self.x  = []
        self.y = []
        self.players = []
        self.teams = []
        self.xyColorIntensity = []
        self.url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
        try:
            self.html = urlopen(self.url)
            self.soup = BeautifulSoup(self.html, features="lxml") #parses webpage content
        except:
            print('Invalid year. Please try again')
            return
        try:
            headers = [th.getText() for th in self.soup.findAll('tr', limit=2)[0]
                      .findAll('th')][1:] #Finds the header cells of the table the table
            data = self.soup.findAll('tr')[1:]
            self.player_stats = [[td.getText() for td in data[i].findAll('td')]
                        for i in range(len(data))] #A list containing arrays representing each player's row
            self.stats = pd.DataFrame(self.player_stats, columns = headers) #Stores the data as a DataFrame
            for player in self.player_stats:
                try:
                    print([player[0], player[28], player[23]])
                    self.x.append(float(player[28]))
                    self.y.append(float(player[23]))
                    self.players.append(player[0])
                    self.teams.append(player[3])
                    self.xyColorIntensity.append(float(player[28]) * float(player[23])) #color intensity for the plot marker
                except Exception as e:
                    print('Warning:', e)
        except Exception as err:
            print("Error:", err)
            main()

    def update_annot(self, ind):
        pos = self.scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, {}".format(" ".join(self.players[p] for p in ind["ind"]),
                           " ".join([self.teams[t] for t in ind["ind"]]))
        annot.set_text(text)

    def hover(self, event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = self.scatter.contains(event)
            if cont:
                self.update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    def plotPointsVsAssists(self):
        plt.title(str(self.year-1)+'-'+str(self.year)[-2:]
                 +' NBA Season Points vs Assists')
        plt.xlabel('Points per game')
        plt.ylabel('Avg. Assists per game')
        self.scatter = plt.scatter(self.x, self.y, s=60, c=self.xyColorIntensity,
                    edgecolor='darkgrey', cmap='Blues')
        colorBar = plt.colorbar()
        colorBar.set_label('Ratings Level')
        fig.canvas.mpl_connect("motion_notify_event", self.hover) #Processes mouse motion events
        plt.show()

def main():
    year = int(input('NBA Year: '))
    nbaStats = PlayerStats(year)
    nbaStats.plotPointsVsAssists()

#Application starts
main()
