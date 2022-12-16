# Hawaii Climate Analysis & Application

## Contributor: Sam Espe

### Overview
This is my submission for Homework #10 for Data Science Bootcamp. There is one Jupyter Notebook, `hawaii_climate_analysis.ipynb`, and one Python file with the code for the Flask app, `app.py`. The SQLite database and the data to create it are located in the `Resources` folder.

This project is divided into two sections: Climate Analysis and Exploration, and Climate App. The Climate Analysis and Exploration is itself divided into two parts: Precipitation Analysis and Station Analysis.

#### Climate Analysis and Exploration

This section uses the Jupyter Notebook `hawaii_climate_analysis.ipynb`. I used SQLAlchemy to connect my Jupyter Notebook to the SQLite database that was provided. 

##### Precipitation Analysis
I used SQLAlchemy to construct a query to obtain the precipitation data from 9 weather stations in Hawaii for the last year of data available. I used the precipitation data to create a graph of the measured precipitation over that timeframe. Many thanks to John Torgerson from class in helping me format the graph so the x-axis presented properly.

##### Station Analysis
I used SQLAlchemy to query the database to obtain information about the weather stations that collected the data. I used a SQLAlchemy query to identify the most active station, and created queries to calculate the minimum, maximum, and average temperature observed at that station. I also used a query to extract the last 12 months of temperature data from that station, and graph it as a histogram to see the temperature distribution.

#### Climate App
I created a Flask app to make an API to present my findings from the Climate Analysis and Exploration section. I created 4 routes, not including the homepage. The first route executes a SQLAlchemy query to the SQLite database to obtain the precipitation data for the last year of data, in the same way as I did it in the previous section. I then created a dictionary of that precipitation data, and present a JSONified version of that dictionary to the viewer. The second route executes a SQLAlchemy query to identify the weather stations that provided data to the database, and presents them to the viewer. The second route queries the database for the last 12 months of temperature data from the most active station (as I had done in the Jupyter Notebook) and returns a JSONified dictionary of the temperature measured for each day.

The third and fourth non-homepage routes offer some interactability to the app. When the user provides a start date to the app via the URL, the app generates a query to the database, returning a JSONified dictionary containing the minimum, maximum, and average temperatures measured at the most active station between the start date and the end of the data in the database. When the user provides a start and an end date, the app generates a query to the database, returning the same information for the time period specified by the provided dates.
