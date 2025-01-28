import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the fuzzy variables
traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')  # 0-100
queue_length = ctrl.Antecedent(np.arange(0, 51, 1), 'queue_length')         # 0-50
green_signal_time = ctrl.Consequent(np.arange(0, 61, 1), 'green_signal_time')  # 0-60

# Membership functions for traffic density
traffic_density['low'] = fuzz.trapmf(traffic_density.universe, [0, 0, 30, 50])
traffic_density['medium'] = fuzz.trimf(traffic_density.universe, [30, 50, 70])
traffic_density['high'] = fuzz.trapmf(traffic_density.universe, [50, 70, 100, 100])

# Membership functions for queue length
queue_length['short'] = fuzz.trapmf(queue_length.universe, [0, 0, 10, 20])
queue_length['medium'] = fuzz.trimf(queue_length.universe, [10, 20, 30])
queue_length['long'] = fuzz.trapmf(queue_length.universe, [20, 30, 50, 50])

# Membership functions for green signal time
green_signal_time['short'] = fuzz.trapmf(green_signal_time.universe, [0, 0, 15, 30])
green_signal_time['medium'] = fuzz.trimf(green_signal_time.universe, [15, 30, 45])
green_signal_time['long'] = fuzz.trapmf(green_signal_time.universe, [30, 45, 60, 60])

# Define fuzzy rules
rule1 = ctrl.Rule(traffic_density['low'] & queue_length['short'], green_signal_time['short'])
rule2 = ctrl.Rule(traffic_density['low'] & queue_length['medium'], green_signal_time['medium'])
rule3 = ctrl.Rule(traffic_density['medium'] & queue_length['medium'], green_signal_time['medium'])
rule4 = ctrl.Rule(traffic_density['high'] & queue_length['long'], green_signal_time['long'])
rule5 = ctrl.Rule(traffic_density['high'] & queue_length['medium'], green_signal_time['long'])
rule6 = ctrl.Rule(traffic_density['medium'] & queue_length['short'], green_signal_time['medium'])
rule7 = ctrl.Rule(traffic_density['low'] & queue_length['long'], green_signal_time['medium'])

# Create the control system
green_signal_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
green_signal_sim = ctrl.ControlSystemSimulation(green_signal_ctrl)

# Function to evaluate fuzzy logic
def evaluate_fuzzy(traffic, queue):
    green_signal_sim.input['traffic_density'] = traffic
    green_signal_sim.input['queue_length'] = queue
    green_signal_sim.compute()
    return round(green_signal_sim.output['green_signal_time'], 2)
