## Introduction
This project was made after the signings of Iker Losada and Peque for Real Betis and Sevilla FC respectively, the goal was to make a study of how the stats of players changue when they get promoted to the 1st division. I took the stats of the midfilders and fowards that got promoted and played in the 1st division this season, in this case the players from UD Las Palmas, Granada CF and Deportivo Alaves. I got the stats by scrapping https://fbref.com/en/ and decided to use following stats:
- Expected Goals (xG)
- Expected Assits (xA)
- Progressive Carries (PrgC)
- Progressive Passes (PrpP)
- Offensive Actions (OffAct)

Then normalized the stats by 90 and discarded the players with less than 360 minutes (4 full matches).
After getting all the stats i needed i made a linear regression for each stat, then used a linear regression to predict the stats that Iker Losada and Peque would get in the first division.
## How it works
There are four python classes in this project:
- get_data.py: This is the class that scraps the FBref website and writes the stats in the file promoted_players.csv
- regrelim.py: Calculates the linear regression of each stats and plots it with the prediction for the players, example:
  ![regre](/images/xGregre.png)  
- radar_plot.py: Shows a radar plot comparing the stats of Peque and Iker Losada in the 2nd division, this is the result:
-  ![radar](/images/radar.png)  
- bar_plot.py: Shows a bar plot for Peque and Iker Losada comparing their stats in the 2nd division and the predicted ones in the 1st division, example:
-  ![bar](/images/LosadaBar.png)  
## More info
Here is a link for a longer document in spanish explaining how i developed the project: https://drive.google.com/file/d/1bk0vC9yPAAFy4EsD34WSgXEu2LUqFUqc/view?usp=drive_link
