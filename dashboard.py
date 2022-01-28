import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import App1
import App2
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import subprocess
from subprocess import Popen, PIPE
import os


st.sidebar.title('Tableau de bord pour prédiction de crédit ')
st.sidebar.subheader("Navigation")

PAGES = {"Vue Générale": App1,
         "Prédiction client": App2}

selection = st.sidebar.radio("Aller à", list(PAGES.keys()))
page = PAGES[selection]
page.app()

