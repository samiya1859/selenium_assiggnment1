import xlsxwriter

def generate_excel(key, url, test, test_results, filename="test_results.xlsx"):
    """
    Generates an Excel file summarizing the test results.

    Args:
    key (str): The test key, typically the domain name.
    url (str): The base URL used for the test.
    test (str): The test case name or description.
    test_results (list): A list of dictionaries, each containing a result.
    filename (str): The name of the output Excel file.
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Define headers
    headers = ["Key", "URL", "Page", "Test Case", "Passed", "Comments"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data rows
    for row_idx, result in enumerate(test_results, start=1):
        worksheet.write(row_idx, 0, key)
        worksheet.write(row_idx, 1, url)
        worksheet.write(row_idx, 2, result.get("page", "Unknown"))
        worksheet.write(row_idx, 3, test)
        worksheet.write(row_idx, 4, result.get("status", "Unknown"))
        worksheet.write(row_idx, 5, result.get("message", "No message"))
        
    workbook.close()
