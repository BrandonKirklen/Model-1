import orbitalDebris


# Imports csv file and creates a list of objects of type orbital debris
def junkList(fileName):
    orbitalObjects = []
    import csv                      # imports the csv module
    f = open(fileName, 'rU')        # opens the csv file
    try:
        reader = csv.reader(f, dialect=csv.excel_tab, delimiter=',')
        parsed = ((row[0], row[1], float(row[2]), float(row[3]), int(row[4]),
                   int(row[5])) for row in reader)
        for row in parsed:          # iterates the rows of the file in orders
            if "DEB" in row[1]:     # Adds piece of debris if labled as DEB
                orbitalObjects.append(orbitalDebris.orbitalDebris(row[0], row[1], row[2], row[3], row[4], row[5]))
    finally:
        f.close()      # closing
    return orbitalObjects
