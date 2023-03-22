"""
Dew on radiometers
==================

Dew on radiometers cause a deviation of the measured irradiance compared to
the true value.

This issue is most often observed during the morning on cold days for
unventilated and unheated pyranometers.
"""

# %%
# First, check out the image below of a shaded and unshaded pyranometer
# at the DTU Climate Station in Copenhagen (January 12th 2021). Note how the
# shaded pyranometer is covered in dew drops, whereas the unshaded is not.
# The reason for this is that the direct irradiance on the unshaded
# pyranometer has already evaporated the dew on the unshaded pyranometer,
# although this process is not instantaneous and the unshaded pyranometer has
# also been affected for some time during the day.
#
# .. image:: ../graphics/dew_pyranometers_dtu_20210112.jpg
#   :alt: Image of two pyranometers, one with dew and one without.
#   :width: 400
#
# Detecting dew
# -------------
# Let's take a look at some irradiance measuremens from DTU's Climate Station
# and see if we can observe this pheonmena.
import numpy as np
import pandas as pd

filename = '../notebooks/data/solar_irradiance_dtu_2019.csv'
df = pd.read_csv(filename, index_col=0, parse_dates=True)

# Calculate Global Horizontal Irradiance (GHI) from Diffuse Horizontal
# Irradiance (DHI) and Direct Normal Irradiance (DNI) using the closure
# equation.
df['GHI_calc'] = df['DHI'] + df['DNI']*np.cos(np.deg2rad(df['zenith']))
df['hourofday'] = df.index.hour

# Compare the calculated and measured GHI:
df.plot.scatter(x='GHI', y='GHI_calc', s=1, alpha=0.5, grid=True)

# Zooming in at the low irradiance region, it is possible to detect swirling
# lines, where measured GHI is initially higher than GHI_calc and then the
# reverse occurs.
df.plot.scatter(x='GHI', y='GHI_calc', s=1, alpha=0.5, grid=True,
                xlim=(-10, 400), ylim=(-10, 400))

# A closer inspection of the data, let's us find a specific day where this
# phenomena is pronounced.
ax = df['2019-05-11 00':'2019-05-11 23'].plot.scatter(
    x='GHI', y='GHI_calc', s=1, grid=True, c='hourofday', cmap='plasma',
    sharex=False)
ax.set_title('2019-05-11')

# From the above plot, it's clear that this phenomena occurs in the morning.

# Let's see if we can also see the issue in the raw measurements for the same
# day:
ax = df.loc['2019-05-11 00':'2019-05-11 23',
            ['DNI', 'GHI_calc', 'GHI', 'DHI']].plot(grid=True, alpha=0.5)
ax.set_title('2019-05-11')
