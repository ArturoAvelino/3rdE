import os
import pandas as pd
import sys


def count_and_export_values(input_file_path, output_directory, column_name):
    """
    Reads a CSV file, counts the occurrences of unique values in a specified column,
    and exports the results to a new CSV file in the output directory.

    Args:
        input_file_path (str): Full path to the source CSV file.
        output_directory (str): Path to the directory where the output file will be saved.
        column_name (str): The name of the column to count values for.
    """
    # Validate input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        return

    try:
        # Read the CSV file
        df = pd.read_csv(input_file_path)

        # Check if the column exists
        if column_name not in df.columns:
            print(
                f"Error: Column '{column_name}' not found in the CSV. Available columns: {list(df.columns)}")
            return

        # Count the values
        # value_counts() returns a Series indexed by the column values
        counts = df[column_name].value_counts().sort_index()

        # Convert to DataFrame for export
        # The index name is the column_name, and we name the count column "count"
        result_df = counts.reset_index()
        result_df.columns = [column_name, 'count']

        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Construct output filename: counts_<original_filename>
        input_filename = os.path.basename(input_file_path)
        output_filename = f"counts_{input_filename}"
        output_path = os.path.join(output_directory, output_filename)

        # Export to CSV (without the pandas index)
        result_df.to_csv(output_path, index=False)

        print(f"Success! Counts for '{column_name}' written to: {output_path}")
        print(f"Top 3 results:\n{result_df.head(3)}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# ########################################################60
# if __name__ == "__main__":
#     # Example usage if run as a script
#     # You can replace these with sys.argv or argparse if you want CLI arguments
#
#     # Using dummy defaults for demonstration; replace with actual paths
#     if len(sys.argv) == 4:
#         in_path = sys.argv[1]
#         out_dir = sys.argv[2]
#         col_name = sys.argv[3]
#         count_and_export_values(in_path, out_dir, col_name)
#     else:
#         print(
#             "Usage: python csv_counter.py <input_file_path> <output_directory> <column_name>")
#
# # --------------------------------------------------------60
# # How to use it
# # You can import the function in your other python scripts:
#
# from csv_counter import count_and_export_values
#
# count_and_export_values(
#     input_file_path='datasets/my_annotations.csv',
#     output_directory='output/stats',
#     column_name='label_id'
# )
#
# # Or run it from the terminal:
# python csv_counter.py datasets/my_annotations.csv output/stats label_id