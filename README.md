# Face Recognition Bot for Finding Missing People

This project is a telegram bot that helps find missing people by matching their faces with images in a database. Users can upload their own images and contact details, and the bot will search for matches within the database. The bot was built using the Aiogram framework and deepface.py for facial recognition.

## Features

- Facial recognition: The bot uses deepface.py to compare images and identify matches.
- Database: The bot stores the uploaded images and contact details in a database (either PostgreSQL or SQL, depending on the implementation).
- Automated matching: The bot automatically searches for matches within the database and provides contact information for similar faces.
- User-friendly interface: The bot is designed to be simple and intuitive, making it accessible to a wide range of users.

## Usage

To use the bot, you can:

1. Start a private chat with the bot on Telegram.
2. Upload an image of the missing person and provide contact details (phone number).
3. The bot will automatically search for matches within the database and provide contact information for similar faces.

## Known Issues

The bot may make mistakes when matching faces, as facial recognition algorithms are not 100% accurate. However, the bot will still provide contact information for similar faces to aid in the search for missing persons.

## Credits

This project was created by Abduqosim. 

Feel free to contribute or use this project as a template for your own facial recognition bots.


