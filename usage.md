# Software Usage


# Project README

## Description
This repository contains the documentation for our project.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Installation
To install the project, follow these steps:
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Run the Docker containers explained in README.md file.

## Usage
To use the application:
1. Access the application at `http://0.0.0.0:8080`.
2. Register with your username, email, and password.
3. Use the returned access token to query Elasticsearch.
4. In Postman, select JWT Bearer and replace "Token" with "Octoxlabs", then add the access token.
5. In the body section of Postman, enter the search query in string format, such as "Hostname = oct".
6. Postman will complete the query and return the first result.

## Testing
To test the application:
1. Access the admin page at `http://0.0.0.0:8080/admin`.
2. Log in with the username "admin" and password "admin123".
3. Add servers and test your queries.

## Logging
Every query made to the application is logged using Celery and Redis. Logging information is stored in `celery.log`.

## Environment Variables
You can find the required environment variables in the `.env` file.

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).
