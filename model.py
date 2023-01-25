import openai
import pandas as pd
import random
from config import connect_to_google_sheets, connect_to_db #you need to create a file named config.py and add the functions connect_to_google_sheets and connect_to_db

# Create a mapping of pandas data types to their corresponding Postgres data types
type_mapping = {
    'object': 'text',
    'int64': 'integer',
    'float64': 'float',
    'datetime64[ns]': 'timestamp',
    'bool': 'boolean',
}

# Create the table in Postgres
def create_table(data, file_name, source):
    # Connect to the database
    conn = connect_to_db()
    cur = conn.cursor() 
    # Generates a random number to append to the file name to make the table name unique
    rand_num = random.randint(1, 100000)
    # Sets the table name as the file name + the random number
    table_name = f"{file_name}_{rand_num}"
    column_defs = []
    # Iterates through the columns of the dataframe
    for i, col in enumerate(data.columns):
        # Gets the number of unique values in the column
        unique_values = data[col].nunique()
        # Gets the total number of values in the column
        total_values = len(data)
        # Checks if the column is mostly unique values
        if (unique_values / total_values) < 0.5:
            try:
                # Tries to convert the column to numeric
                data[col] = pd.to_numeric(data[col])
            except ValueError:
                pass
        # Gets the appropriate data type for the column based on the column data type
        col_type = type_mapping.get(str(data[col].dtype), 'text')
        column_defs.append(f"{col} {col_type}")
    # creates the table with the desired columns and data types
    cur.execute(f"CREATE TABLE {table_name} ({', '.join(column_defs)})")
    # insert data into the table
    data_values = [tuple(row) for _, row in data.iterrows()]
    cur.executemany(f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(data.columns))})", data_values)
    print("Local Table created - Data Migration Complete!")
    #commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()
    #return the table name and columns
    return table_name, ', '.join(column_defs)


# Get the data from your file (Sheet or File)       
def get_data_source():
    while True:
        # Asks the user to select the data source, Google Sheet or local file
        source = input("Would you like to use a Google Sheet or a local file as your data source? (Sheet/File) ")
        if source == "Sheet":
            # Asks the user to input the URL of the Google Sheet and the sheet name
            sheet_name = input("Please enter the URL of the Google Sheet: ")
            sheet_name_2 = input("Please enter the sheet name: ")
            # Connects to the Google Sheet API
            client = connect_to_google_sheets()
            # Opens the workbook and sheet specified by the user
            wb = client.open_by_url(sheet_name)
            sheet = wb.worksheet(sheet_name_2)
            # Retrieves all data from the sheet
            original_df = sheet.get_all_values()
            # Creates a dataframe from the retrieved data and assigns the first row as column headers
            data = pd.DataFrame(original_df[1:], columns=original_df[0])
            file_name = sheet_name_2
            return data, file_name, source
        elif source == "File":
            # Asks the user to input the file path
            file_path = input("Please enter the file path: ")
            # Reads in the data from the file
            data = pd.read_csv(file_path, low_memory=False)
            # Gets the file name from the file path and removes the file extension
            file_name = file_path.split("/")[-1].split(".")[0]
            return data, file_name, source
        else:
            # If the user inputs an invalid source, prompts them to enter a valid source
            print("Invalid source. Please enter 'Sheet' or 'File'.")


# Generate the Query to OpenAI
def generate_queryAI(prompt, table_name, table_structure):
    try:
        # Creating a query prompt using the provided prompt, table name, and table structure
        query_prompt = f"Write a full SQL query that will fulfill the user's request of '{prompt}' using the table '{table_name}' with the following table structure: {table_structure}. Make sure to handle missing data or null values and consider more complex queries. Respond with only a valid syntax SQL query, no explanation."
        # Using OpenAI API to generate a query based on the prompt
        query = openai.Completion.create(engine="text-davinci-002", prompt=query_prompt, temperature=0.4, max_tokens=500)
        # Storing the generated query as a string
        query_str = query.choices[0].text
        # Returning the query
        return query_str
    except Exception as e:
        # In case of any error, returning the exception message
        return e

