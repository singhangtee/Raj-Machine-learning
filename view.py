import pickle
import matplotlib.cm as cm
import matplotlib.pyplot as plt

with open('saved_myrl_agent.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)