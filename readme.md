# Songify-"ML"

- This is the source of the machine learning model used in [Songify-App (API)]('https://github.com/G0maa/songify-app')
- Currently, I only use a `cosine similarity matrix` that only saves the top 10 similar tracks.
- The source of the `HDF5` file can be generated using [this](https://colab.research.google.com/drive/1s0da0T2G7sRxZrqDM0-Mj0oxhgwDKHY9?usp=sharing) notebook.
  - This notebook was pretty much generated through long series of questions with `ChatGPT` & with the help of [Jonathan-Monir](https://github.com/Jonathan-Monir)
- Note: The goal is not to create an accurate recommendation model, but to use Message Queues & RPCs.

## What does the code do

- Load `HDF5` containing top 10 similarities to each track.
- Load `csv` file containing tracks data.
- Wait for RPC request from RabbitMQ server.
- Request comes with a list of track ids that the user listened to.
- function returns a list of recommended tracks using the `HDF5` file.

## Requirements
- If you want to test-run the recommendations quickly:
  - Uncomment last few lines in `snippet.py` and run it.
- If you want to try it along side the server then you need to have an instance of [Songify-App]('https://github.com/G0maa/songify-app') running.
  - See the `readme` there.

## How to run?
- create virtual env `python3 -m venv .venv`
- Activate virtual env `source .venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- run `python3 main.py`
