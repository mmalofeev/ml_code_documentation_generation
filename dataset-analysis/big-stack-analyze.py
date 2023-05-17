import ast
import matplotlib.pylab as plt

def build_plots_licence(filepath):
    file = open(filepath, "r")
    lines = file.readlines()
    license_count = {}
    for line in lines:
        data = ast.literal_eval(line)
        license = data['max_stars_licenses'][0]
        if license not in license_count:
            license_count[license] = 0
        license_count[license] += 1
    return license_count

def build_plots_stars(filepath):
    file = open(filepath, "r")
    lines = file.readlines()
    stars_count = {}
    for line in lines:
        data = ast.literal_eval(line)
        count = data['max_stars_count']
        if count // 500 * 500 not in stars_count:
            stars_count[count // 500 * 500] = 0
        stars_count[count // 500 * 500] += 1
    return stars_count

filepath = "/Users/mikhail.malofeev/programm/ml/thesis/the_stack_filtered.txt"
# licenses = build_plots_licence(filepath)

map_entries = sorted(build_plots_stars(filepath).items())
print(map_entries)
stars, count = zip(*map_entries)
plt.plot(stars[0:50], count[0:50])
plt.xlabel("Number of python scripts")
plt.ylabel("Number of stars")
plt.show()


# map_entries = sorted(licenses.items(), key=lambda entry: entry[1], reverse=True)
# license, count = zip(*map_entries)
# plt.plot(license[0:5], count[0:5])
# plt.show()