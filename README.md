Learning Behavior Analysis
Overview
This project aims to analyze learning behavior using data from educational platforms. It provides functions to process input data, calculate various metrics, and analyze behavior trends over time.

Dependencies
Python 3.x
pandas
numpy
matplotlib (optional, for visualization)
Installation
Clone the repository to your local machine:
bash
Copy code
git clone https://github.com/your_username/learning-behavior-analysis.git
Install the required dependencies:
Copy code
pip install -r requirements.txt
Usage
Prepare your input data:

Ensure you have three CSV files containing the following data:
datatotal.csv: Total data including user ID, page information, and behavior count.
page_duration.csv: Page duration data.
text_count.csv: Text count data.
Place these files in the project directory.
Run the main script:

css
Copy code
python main.py
View the output:

Summary statistics will be saved to summary_statistics.csv.
Behavior trends over time will be visualized (optional, requires matplotlib).
Functions
calculate_text_count: Calculate the word count of text content.
merge_dataframes: Merge multiple DataFrames into a single DataFrame.
calculate_seconds: Convert time duration columns to seconds.
fill_nan_text_duration: Fill NaN values in 'text_duration_seconds' column with zeros.
calculate_text_operation_time: Calculate cumulative text operation time for each page.
calculate_text_count_total: Calculate total text count for each page.
analyze_learning_behavior: Analyze learning behavior trends over time.
generate_summary_statistics: Generate summary statistics for each user.
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
