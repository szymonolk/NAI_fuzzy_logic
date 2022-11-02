import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

"""
Requirements

Before running the script, install the required libraries included in the 'requirements.txt' file

pip install -r requirements.txt


==========================================
Lighting control system
==========================================
Our simple application control the bulb based on environmental parameters.
Such as the size of the room, the intensity of the sun and the time of day.

The team responsible for the code:
Szymon Olkiewicz s18629
Kamil Kaczówka s21790
"""

# New objects that hold universe variables
time_of_day = ctrl.Antecedent(np.arange(0, 11, 1), 'time')
sun_intensity = ctrl.Antecedent(np.arange(0, 11, 1), 'intensity')
room_size = ctrl.Antecedent(np.arange(0, 50, 1), 'size')
bulb_intensity = ctrl.Consequent(np.arange(0, 100, 1), 'bulb')

#Custom membership functions
time_of_day['night'] = fuzz.trimf(time_of_day.universe, [0, 0, 2])
time_of_day['morning'] = fuzz.trimf(time_of_day.universe, [2, 3, 4])
time_of_day['midday'] = fuzz.trimf(time_of_day.universe, [4, 6, 8])
time_of_day['evening'] = fuzz.trimf(time_of_day.universe, [8, 9, 10])

room_size['small'] = fuzz.trimf(room_size.universe, [0, 0, 6])
room_size['average'] = fuzz.trimf(room_size.universe, [6, 13, 25])
room_size['big'] = fuzz.trimf(room_size.universe, [25, 35, 49])

# Auto-membership function
sun_intensity.automf(3)
bulb_intensity.automf(3)

"""
Fuzzy rules
----------------
Defining relationships between input and output variables. 
Simple example:
1. If the timme of day is night and sun intensity is poor and room size is small,
    then bulb intensinity is average.

"""

rule1 = ctrl.Rule(time_of_day['night'] & sun_intensity['poor'] & room_size['small'], bulb_intensity['average'])
rule2 = ctrl.Rule(time_of_day['night'] & sun_intensity['poor'] & room_size['average'], bulb_intensity['average'])
rule3 = ctrl.Rule(time_of_day['night'] & sun_intensity['poor'] & room_size['big'], bulb_intensity['good'])
rule4 = ctrl.Rule(time_of_day['morning'] & sun_intensity['poor'] & room_size['small'], bulb_intensity['average'])
rule5 = ctrl.Rule(time_of_day['morning'] & sun_intensity['poor'] & room_size['average'], bulb_intensity['average'])
rule6 = ctrl.Rule(time_of_day['morning'] & sun_intensity['poor'] & room_size['big'], bulb_intensity['good'])
rule7 = ctrl.Rule(time_of_day['midday'] & sun_intensity['poor'] & room_size['small'], bulb_intensity['average'])
rule8 = ctrl.Rule(time_of_day['midday'] & sun_intensity['average'] & room_size['small'], bulb_intensity['poor'])
rule9 = ctrl.Rule(time_of_day['midday'] & sun_intensity['good'] & room_size['small'], bulb_intensity['poor'])
rule10 = ctrl.Rule(time_of_day['midday'] & sun_intensity['poor'] & room_size['average'], bulb_intensity['average'])
rule11 = ctrl.Rule(time_of_day['midday'] & sun_intensity['average'] & room_size['big'], bulb_intensity['good'])
rule12 = ctrl.Rule(time_of_day['midday'] & sun_intensity['average'] & room_size['average'], bulb_intensity['poor'])
rule13 = ctrl.Rule(time_of_day['midday'] & sun_intensity['good'] & room_size['average'], bulb_intensity['poor'])
rule14 = ctrl.Rule(time_of_day['evening'] & sun_intensity['poor'] & room_size['small'], bulb_intensity['average'])
rule15 = ctrl.Rule(time_of_day['evening'] & sun_intensity['poor'] & room_size['average'], bulb_intensity['average'])
rule16 = ctrl.Rule(time_of_day['evening'] & sun_intensity['poor'] & room_size['big'], bulb_intensity['good'])
rule17 = ctrl.Rule(time_of_day['evening'] & sun_intensity['average'] & room_size['small'], bulb_intensity['average'])
rule18 = ctrl.Rule(time_of_day['evening'] & sun_intensity['average'] & room_size['average'], bulb_intensity['average'])
rule19 = ctrl.Rule(time_of_day['evening'] & sun_intensity['average'] & room_size['big'], bulb_intensity['average'])

"""
After define our rules we creating a control system.
"""


light_control = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12,
     rule13, rule14, rule15, rule16, rule17, rule18, rule19])

control = ctrl.ControlSystemSimulation(light_control)

"""
Now we can simulate our control system by specifying three inputs and calling 'compute' method.
"""

#pass all inputs to the control system.
control.input['time'] = 5
control.input['intensity'] = 5
control.input['size'] = 13.5


bulb_intensity.view()

#Calculate all this stuff
control.compute()

"""
Print result and visualize it.
"""
print(control.output['bulb'])
bulb_intensity.view(sim=control)
