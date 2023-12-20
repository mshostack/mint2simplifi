import os
import pandas as pd
from datetime import datetime

def process_mint_csv(input_path):
    try:
        # Normalize the path to handle both forward slashes and backslashes
        input_path = os.path.normpath(input_path)
        
        mint_df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # Group transactions by "Account Name"
    grouped_accounts = mint_df.groupby("Account Name")

    # Create a directory for output files
    output_directory = os.path.join(os.path.dirname(os.path.abspath(input_path)), "Converted CSVs")
    output_log_path = os.path.join(output_directory, "log.txt")
    os.makedirs(output_directory, exist_ok=True)

    # Initialize counters and error flag
    total_files_generated = 0
    errors = 0
    error_messages = []

    # Function to clean and replace invalid characters in filenames
    def clean_filename(name):
        return ''.join(char for char in name if char.isalnum() or char in [' ', '_', '-'])

    # Time and date stamp format
    timestamp_format = "[%m/%d/%y %H:%M]"

    # Add time and date stamp to the log
    with open(output_log_path, "a") as log_file:
        log_file.write(f"\n\n=== {datetime.now().strftime(timestamp_format)} ===\n")

    # Iterate through each account group
    for account_name, group_df in grouped_accounts:
        # Clean the account name for creating directories and filenames
        cleaned_account_name = clean_filename(account_name)

        # Create an output filename based on the cleaned account name
        output_filename = f"{cleaned_account_name} - transactions.csv"

        try:
            # Write the transactions to a new CSV file
            output_path = os.path.join(output_directory, output_filename)
            group_df.to_csv(output_path, index=False)

            # Update counters
            total_files_generated += 1

            # Log the summary information with proper spacing
            with open(output_log_path, "a") as log_file:
                log_file.write(
                    f"{output_filename.ljust(80)} | "
                    f"{str(len(group_df)).ljust(12)} transactions - "
                    f"Oldest Date: {str(group_df['Date'].min())}\n"
                )
        except Exception as e:
            # Log errors
            errors += 1
            error_messages.append(f"Error processing {account_name} - {str(e)}")

    # Log overall summary
    with open(output_log_path, "a") as log_file:
        log_file.write("\nSummary:\n")
        log_file.write(
            f"{total_files_generated} files generated in {output_directory}\n"
            f"Errors: {errors}\n"
        )
        
        if errors > 0:
            log_file.write("\nError Details:\n")
            for error_message in error_messages:
                log_file.write(f"{error_message}\n")

if __name__ == "__main__":
    # Prompt the user for the input CSV file path
    input_path = input("Enter the path of the Mint transactions CSV: ")
    
    # Call the processing function
    process_mint_csv(input_path)
