import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json



df = pd.read_csv('input.csv', index_col='Country')

#   First impressions dataframe
# print(df.columns)
# print(df.dtypes)
#   Calculate missing values(NANs) per column
# print(df.isnull().sum())
#   Delete all completely empty rows
df = df.dropna(axis=0, how='all')
#   Create copy of df in which values can be mutated or deleted
df2 = df.copy()



#   Clean GDP data
# Values in GDP per capita are of type object.
# Create new column with the cleaned values (numbers only) and convert to numeric
GDP_object = df2.loc[:,"GDP ($ per capita) dollars"]
GDP_cleaned = []
for gdp in GDP_object:
    try:
        nr_dollars = gdp.split()
    except:
        pass
    nr = nr_dollars[0]
    GDP_cleaned.append(nr)
# insert new column into df2
df2['GDP cleaned'] = GDP_cleaned
# make all these values numeric, except for unknowns, coerce these to nan
df2['GDP cleaned'] = pd.to_numeric(df2['GDP cleaned'], errors='coerce')

#   Calculate statistics
GDP_mean = df2["GDP cleaned"].mean()
GDP_median = df2["GDP cleaned"].median()
GDP_mode = df2["GDP cleaned"].mode()
GDP_stdv = df2["GDP cleaned"].std()
GDP_min = int(df2["GDP cleaned"].min())
GDP_max = int(df2["GDP cleaned"].max())
print("GDP mean median mode:")
print(GDP_mean, GDP_median, GDP_mode)
print("GDP miniumum and maximum:")
print(GDP_min, GDP_max)

#   Plot Histogram for GDP
# Exclude outliers prior to histogram plotting
# Outliers definition = everything outside: q1-1.5*interqtrange and q3+1.5*interqtrange
q1 = df2["GDP cleaned"].quantile(0.25)
q3 = df2["GDP cleaned"].quantile(0.75)
interqtrange = q3-q1
border_min = q1 - (1.5 * interqtrange)
border_max = q3 + (1.5 * interqtrange)
# df3 is free from GDP outliers
df3 = df2.loc[(df2["GDP cleaned"] < border_max) & (df2["GDP cleaned"] > border_min)]


#   Plot GDP in a histogram
plt.hist(df3.loc[:,"GDP cleaned"], bins=50)
plt.title('GDP spread')
plt.xlabel('GDP in $ per capita')
plt.ylabel('Number of Countries')
plt.xticks(np.arange(0, 39000, step=2000), rotation=50)
plt.grid(axis='y')
plt.show()


#   Five number summary infant mortality
#   First make data usable by replacing commas(,) for dots(.) and numeric
floats = []
for x in df2['Infant mortality (per 1000 births)']:
    value = x
    try:
        float = value.replace(',', '.')
        floats.append(float)
    except:
        floats.append(value)
df2['Infant mortality cleaned'] = floats
df2['Infant mortality cleaned'] = pd.to_numeric(df2['Infant mortality cleaned'], errors='coerce')

#   Five numbers = Minimum, First Quartile, Median, Third Quartile and Maximum
infant_min = df2['Infant mortality cleaned'].min()
infant_firstq = np.nanpercentile(df2['Infant mortality cleaned'], 25)
infant_median = np.nanpercentile(df2['Infant mortality cleaned'], 50)
infant_thirdq = np.nanpercentile(df2['Infant mortality cleaned'], 75)
infant_max = df2['Infant mortality cleaned'].max()
print("Five number summary:")
print(infant_firstq, infant_median, infant_thirdq, infant_max)


boxplot = df2.boxplot(column='Infant mortality cleaned', return_type='dict', grid=True)
plt.title('Infant mortality')
plt.xlabel('boxplot')
plt.ylabel('mortality')
plt.show()

#   Clean extra white space in Region column
stripped = []
for x in df2['Region']:
    value = x
    value = value.strip()
    stripped.append(value)
df2['Region'] = stripped


#   Write cleaned columns Country {Region, Pop density, Inf mortality and GDP} to a JSON file
#   First make a new pandas dataframe containing only these Values
df4 = df2[[ 'Region', 'Pop. Density (per sq. mi.)', 'Infant mortality cleaned', 'GDP cleaned']]

outfile = open('Final.json','w')
outfile.write(df4.to_json(orient='index'))
outfile.close()
