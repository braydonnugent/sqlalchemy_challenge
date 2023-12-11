sqlalchemy_challenge (MODULE 10)

PLEASE FIND ATTACHED,
WITHIN SurfsUp FOLDER,

climate_starter: initial guiding notebook for part 1
climate_main: Jupyter Notebook for part 1
app.py: Python script for part 2

All additional files (Within resources file) are all assignment material

PLEASE NOTE:
An issue occured & many methods were attempted to resolve the issue.

The issue was that the local link 'http://127.0.0.1:5000' would fail to update upon changes to the script.

The eventual solution uncovered was to create an external link via...
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

This resulted in the external link 'http://192.168.0.214:5000' to be generated & is the one to be used.

Please ignore the local link & analyse the content within the external link provided.
Thank you!
