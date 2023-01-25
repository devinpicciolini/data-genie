import pandas as pd
from config import connect_to_google_sheets, connect_to_db
from model import create_table, generate_queryAI

# Connect to Google Sheets API using the client 
client = connect_to_google_sheets()

# Loop until a valid data source is entered
while True:
    # Ask user if they want to use a Google Sheet or a local file as data source
    source = input("Would you like to use a Google Sheet or a local file as your data source? (Sheet/File) ")
    # If user chooses Google Sheet
    if source == "Sheet":
        # Ask user for the URL of the Google Sheet
        sheet_name = input("Please enter the URL of the Google Sheet: ")
        sheet_name_2 = input("Please enter the sheet name: ")
        try:
            # Open the sheet using the URL and sheet name
            wb = client.open_by_url(sheet_name)
            sheet = wb.worksheet(sheet_name_2)
            # Get all values from the sheet and store in variable original_df
            original_df = sheet.get_all_values()
            # Convert original_df to a pandas dataframe and store in variable data
            data = pd.DataFrame(original_df[1:], columns=original_df[0])
            file_name = sheet_name_2
            break
        except Exception as e:
            print("Invalid URL or sheet name, please try again.")
    # If user chooses local file
    elif source == "File":
        file_path = input("Please enter the file path: ")
        try:
            # Read the file using pandas and store in variable data
            data = pd.read_csv(file_path)
            file_name = file_path.split("/")[-1].split(".")[0]
            break
        except FileNotFoundError:
            print("File not found, please enter a valid file path.")
        except Exception as e:
            print("An error occurred while reading the file, please try again.")
    else:
        print("Invalid option. Please enter 'Sheet' or 'File'.")

# Create the table using the data, file name and source
table_name, table_structure = create_table(data, file_name, source)

# Connect to the database
conn = connect_to_db()
cur = conn.cursor()

# Loop until user enters 'exit'
while True:
    # Ask the user for their query
    prompt = input("Ask away, what do you want to know? (Enter 'exit' to quit) ")
    if prompt.lower() == "exit":
        break
    # Generate the query using the user's prompt, table name and table structure
    query = generate_queryAI(prompt, table_name, table_structure)
    # Execute the query
    cur.execute(query)
    # Fetch and store the results of the query
    query_results = cur.fetchall()
    # Print the query results
    print(query_results)
    print(query)

# Close the cursor and connection to the database
cur.close()
conn.close()
