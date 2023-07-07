# Building-Materials-Carbon-Morocco-Africa

Flask Carbon Footprint Calculator
This is a Python Flask application that calculates the carbon footprint and cost of different materials based on user input. It provides visualizations of the data using charts and allows users to compare the environmental impact and cost of various materials.

Features
Calculates carbon footprint and cost based on user input for different materials
Allows users to input the volume and distance for each material
Provides feedback on invalid input
Displays the total carbon footprint and cost
Generates bar charts to visualize the carbon footprint and cost for each material
Generates a pie chart to show the percentage contribution of each material to the total carbon footprint and cost
Calculates ratios of carbon footprint to cost and carbon footprint to distance
Generates charts to visualize these ratios
Prerequisites
Python 3.x
Flask
Flask-WTF
Chart.js (included in the template)
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/repository-name.git
Change into the project directory:
bash
Copy code
cd repository-name
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Usage
Run the Flask application:
bash
Copy code
python app.py
Open your web browser and go to http://localhost:5000 to access the application.

Enter the volume and distance for each material in the provided input fields.

Select the transportation method for each material from the dropdown menu.

Click the "Calculate" button to calculate the carbon footprint and cost.

The total carbon footprint and cost will be displayed at the top of the page.

The bar charts show the carbon footprint and cost for each material. The colors of the bars indicate the environmental impact level: green for low impact, yellow for moderate impact, and red for high impact.

The pie charts show the percentage contribution of each material to the total carbon footprint and cost.

The ratio charts show the carbon footprint to cost ratio and the carbon footprint to distance ratio for each material.

Customization
You can customize the application by modifying the following parts of the code:

material_data: This dictionary contains the data for each material, including the carbon footprint and cost per square meter. You can add, remove, or update materials and their corresponding data.

get_transportation_footprint_per_km() and get_transportation_cost_per_km(): These functions calculate the transportation footprint and cost per kilometer based on the transportation method. You can modify the calculations or add new methods.

The HTML templates (index.html): You can modify the templates to change the layout or add new visualizations using Chart.js.

Contributing
Contributions are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
This project was inspired by the need to raise awareness about the environmental impact of different construction materials. It aims to provide users with information to make more sustainable choices.

Contact
For any questions or inquiries, please contact elkendi.abderrahmane@hotmail.com
