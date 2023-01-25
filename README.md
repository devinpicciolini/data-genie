This code allows you to use the OpenAI API to generate SQL queries based on a user's prompt and the structure of a table in a Google Sheet or a CSV file. The code uses the Pandas library to read and convert the data to a DataFrame. Finally, I am using Postgres to create a table and run the AI generated query on the data.

### Getting Started

1. Clone the repository:
git clone https://github.com/devinpicciolini/data-genie.git

2. Install the required dependencies:
```
pip install -r requirements.txt
pip3 install openai pandas gspread oauth2client
```


3. Replace the openai.api_key value in the code with your OpenAI API key. (https://beta.openai.com/account/api-keys)

4. Create a credentials.json file with your Google Sheets API credentials. (https://www.youtube.com/watch?v=vt_PtZ6KYIE)

5. Run the script by executing the following command in your terminal:
```
python3 controller.py
```

6. The script will ask if you would like to use a Google Sheet or a local file as your data source.

7. If you choose a Google Sheet, enter the URL of the sheet and the name of the sheet.

8. If you choose a local file, enter the file path when prompted.

9. Enter your query prompt when prompted. The script will continue to prompt for queries until you exit the script.

10. The generated query will be displayed on the terminal.

### Security

- Remove any hardcoded sensitive information from the code, such as credentials or API keys.

- Use encryption for sensitive information, such as user credentials.

- Make sure to keep all dependencies and libraries up to date to ensure that any known vulnerabilities are patched.

### Built With

- [OpenAI](https://openai.com/) - The AI platform used
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis library for Python

### Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Create a new Pull Request

### Author

- [Devin Picciolini](https://github.com/devinpicciolini)

### License

This project is licensed under the MIT License
