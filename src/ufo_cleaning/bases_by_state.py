import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as sfm
import seaborn as sns
import us

sns.set_style('whitegrid')  # Make those plots pretty


sightings = pd.read_csv("../../data/raw/ufo_sightings.csv")
base_locs = pd.read_csv("../../data/raw/usaf_base_locs.csv")
name_to_abbr = dict()
[name_to_abbr.update({i.name: i.abbr}) for i in us.STATES]
state_pops = pd.read_csv("../../data/raw/state_pops.csv", thousands=',')  # Numbers are defined with comma separators

sightings = sightings[sightings.index < 109088]  # Limits to sightings from >= 1974
sightings = sightings[sightings.state.isin(name_to_abbr.values())]  # Limits sightings to those in valid US states

# Restructure state_pops to limit to valid US states and average from 1970 to 2010
state_pops.Name = state_pops.Name.map(name_to_abbr)
state_pops = state_pops.set_index('Name')
state_pops = state_pops[['1970', '1980', '1990', '2000', '2010']]
state_pops = state_pops.mean(1)
state_pops = state_pops[~state_pops.index.isnull()] 

# Group sightings and base_locs by state and find the number of sightings/bases per state
sightings = sightings.groupby('state').count().max(1)
base_locs = base_locs.groupby('State').count().max(1)

# Combine data into single dataframe for plotting
df = pd.DataFrame({'sightings': sightings, 'base_count': base_locs, 'pops': state_pops}, index=sightings.index)
df.base_count = df.base_count.fillna(0)
df = df[df.index!='DC']
df['sightings_per_thousand'] = (df.sightings/df.pops) * 1000

# Fit an ordinary least squares model using base count per state to predict sightings per thousand people
fit = sfm.ols('sightings_per_thousand ~ base_count', data=df).fit()
print(fit.summary())

# Plot this fit
sns.regplot(x='base_count', y='sightings_per_thousand', data=df, ci=None)
plt.xlabel('Base count by state')
plt.ylabel('UFO sightings per thousand people')
plt.show()
