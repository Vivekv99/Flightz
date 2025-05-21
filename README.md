Flightz

Flightz is a flight booking web application designed to provide users with a seamless experience in searching, viewing, and managing flight information. Built using Python, HTML, CSS, and JavaScript, Flightz offers a user-friendly interface and efficient backend processing.

🚀 Features

Flight Search: Easily search for flights based on departure and arrival cities.

Flight Details: View detailed information about each flight, including airline, departure and arrival times, and prices.

Booking Management: Manage your bookings with options to add, update, or delete flight entries.

Responsive Design: Optimized for both desktop and mobile devices.

Data Storage: Utilizes SQLite for efficient data storage and retrieval.


🛠️ Technologies Used

Frontend:

HTML

CSS

JavaScript


Backend:

Python

Flask


Database:

SQLite



📂 Project Structure

Flightz/
│
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── flights.db            # SQLite database file
├── flights.json          # Sample flight data in JSON format
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── add_more_flights.py   # Script to add more flight data
├── create_placeholder_image.py # Script to create placeholder images
├── insert_flights.py     # Script to insert flight data into the database
└── render.yaml           # Render deployment configuration



⚙️ Setup Instructions

1. Clone the Repository

git clone https://github.com/Vivekv99/Flightz.git
cd Flightz



2. Install Dependencies

pip install -r requirements.txt



3. Run the Application

python app.py



The application will be accessible at http://127.0.0.1:5000/. 

🧪 Scripts

add_more_flights.py: Adds additional flight data to the database.

create_placeholder_image.py: Generates placeholder images for flight listings.

insert_flights.py: Inserts flight data from flights.json into the database. 


📄 License

This project is licensed under the MIT License.
