import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Material data (volume per square meter)
material_data = {
    'Rammed Earth': {'Carbon Footprint': 17.5, 'Cost': 650},
    'Stone': {'Carbon Footprint': 125, 'Cost': 950},
    'Concrete': {'Carbon Footprint': 200, 'Cost': 915},
    'Brick': {'Carbon Footprint': 125, 'Cost': 555},
    'Wood': {'Carbon Footprint': 180, 'Cost': 1060},
    'Paint': {'Carbon Footprint': 5, 'Cost': 60},
    'Steel': {'Carbon Footprint': 800, 'Cost': 1200}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        volume_data = {}
        distance_data = {}
        method_data = {}

        try:
            for material in material_data:
                volume = max(0, float(request.form.get(material + '_volume', 0)))
                distance = max(0, float(request.form.get(material + '_distance', 0)))
                method = request.form.get(material + '_method', '')
                volume_data[material] = volume
                distance_data[material] = distance
                method_data[material] = method
        except ValueError:
            flash('Invalid input. Please enter a number for the volume and distance.')
            return render_template('index.html', material_data=material_data)

        if len(volume_data) > 0:
            footprint, cost = calculate_footprint_and_cost(volume_data)
            transportation_footprint = calculate_transportation_footprint(distance_data, method_data)
            total_footprint = footprint + transportation_footprint
            total_cost = cost + calculate_transportation_cost(distance_data, method_data)
            flash(f'Total Carbon Footprint: {total_footprint} kgCO2e\nTotal Cost: {total_cost} MAD')

            # Generate chart data
            materials = list(material_data.keys())
            carbon_footprints = [material_data[material]['Carbon Footprint'] * volume_data[material] for material in materials]
            costs = [material_data[material]['Cost'] * volume_data[material] for material in materials]
            distances = [distance_data[material] for material in materials]

            # Calculate bar colors based on carbon footprint
            colors = []
            for footprint in carbon_footprints:
                if footprint < 100:
                    colors.append('green')
                elif footprint < 500:
                    colors.append('yellow')
                else:
                    colors.append('red')

            chart_data_footprint = {
                'materials': materials + ['Total'],
                'values': carbon_footprints + [total_footprint],
                'unit': 'kgCO2e',
                'colors': colors
            }

            chart_data_cost = {
                'materials': materials + ['Total'],
                'values': costs + [total_cost],
                'unit': 'MAD',
                'colors': 'blue'
            }

            chart_data_distance = {
                'materials': materials,
                'values': distances,
                'unit': 'km'
            }

            # Calculate carbon footprint percentages for pie chart
            total_carbon_footprint = sum(carbon_footprints)
            carbon_footprint_percentages = [(footprint / total_carbon_footprint) * 100 for footprint in carbon_footprints]

            chart_data_pie = {
                'materials': materials,
                'values': carbon_footprint_percentages,
                'unit': '%'
            }

            # Calculate carbon footprint to cost ratios
            carbon_footprint_cost_ratios = [footprint / cost for footprint, cost in zip(carbon_footprints, costs)]

            chart_data_ratio = {
                'materials': materials,
                'values': carbon_footprint_cost_ratios,
                'unit': 'kgCO2e / MAD'
            }

            # Calculate cost percentages for pie chart
            total_cost = sum(costs)
            cost_percentages = [(cost / total_cost) * 100 for cost in costs]

            chart_data_cost_pie = {
                'materials': materials,
                'values': cost_percentages,
                'unit': '%'
            }

            # Calculate carbon footprint to distance ratios
            carbon_footprint_distance_ratios = [footprint / distance if distance > 0 else 0 for footprint, distance in zip(carbon_footprints, distances)]

            chart_data_distance_ratio = {
                'materials': materials,
                'values': carbon_footprint_distance_ratios,
                'unit': 'kgCO2e / km'
            }

            # Convert chart data to JSON for passing to JavaScript
            chart_data_json_footprint = json.dumps(chart_data_footprint)
            chart_data_json_cost = json.dumps(chart_data_cost)
            chart_data_json_distance = json.dumps(chart_data_distance)
            chart_data_json_pie = json.dumps(chart_data_pie)
            chart_data_json_ratio = json.dumps(chart_data_ratio)
            chart_data_json_cost_pie = json.dumps(chart_data_cost_pie)
            chart_data_json_distance_ratio = json.dumps(chart_data_distance_ratio)

            return render_template('index.html', material_data=material_data, chart_data_footprint=chart_data_json_footprint,
                                   chart_data_cost=chart_data_json_cost, chart_data_distance=chart_data_json_distance,
                                   chart_data_pie=chart_data_json_pie, chart_data_ratio=chart_data_json_ratio,
                                   chart_data_cost_pie=chart_data_json_cost_pie, chart_data_distance_ratio=chart_data_json_distance_ratio)

        else:
            flash('Please enter volume for at least one material.')

    return render_template('index.html', material_data=material_data)


# Rest of the code...




def calculate_footprint_and_cost(volume_data):
    total_footprint = 0
    total_cost = 0

    for material, volume in volume_data.items():
        if material in material_data:
            footprint = material_data[material]['Carbon Footprint']
            cost = material_data[material]['Cost']
            material_footprint = footprint * volume
            material_cost = cost * volume

            total_footprint += material_footprint
            total_cost += material_cost

    return total_footprint, total_cost


def calculate_transportation_footprint(distance_data, method_data):
    total_footprint = 0

    for material, distance in distance_data.items():
        if material in material_data:
            footprint_per_km = get_transportation_footprint_per_km(material_data[material]['Carbon Footprint'], method_data[material])
            material_footprint = footprint_per_km * distance
            total_footprint += material_footprint

    return total_footprint


def calculate_transportation_cost(distance_data, method_data):
    total_cost = 0

    for material, distance in distance_data.items():
        if material in material_data:
            cost_per_km = get_transportation_cost_per_km(material_data[material]['Cost'], method_data[material])
            material_cost = cost_per_km * distance
            total_cost += material_cost

    return total_cost


def get_transportation_footprint_per_km(footprint, method):
    if method == 'fossil_fuel':
        return footprint * 1.2
    elif method == 'electric':
        return footprint * 0.5
    elif method == 'flight':
        return footprint * 2.5
    elif method == 'maritime':
        return footprint * 1.8
    else:
        return 0


def get_transportation_cost_per_km(cost, method):
    if method == 'fossil_fuel':
        return cost * 0.8
    elif method == 'electric':
        return cost * 0.5
    elif method == 'flight':
        return cost * 1.5
    elif method == 'maritime':
        return cost * 1.2
    else:
        return 0


if __name__ == '__main__':
    app.run(debug=True)
