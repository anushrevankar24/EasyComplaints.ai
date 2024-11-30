EasyComplaints.ai - Complaint Registration System
================================================

Introduction
------------
EasyComplaints.ai is a  web application designed to revolutionize the way complaints are managed. Built using the powerful Django framework, this application seamlessly integrates state-of-the-art text classification and image classification models, providing users with a comprehensive and user-friendly experience.

With EasyComplaints.ai, users can effortlessly register complaints in various formats, including text, and images, ensuring that their concerns are accurately captured and processed. The intuitive user interface offers a dynamic dashboard, providing a clear overview of complaint categories such as Resolved, Pending, and Rejected, as well as the ability to view all registered complaints.

For staff members, EasyComplaints.ai offers a dedicated dashboard that categorizes complaints based on departmental divisions, ensuring efficient and streamlined management. Complaints are automatically sorted into their respective departments, allowing staff to review, process, and mark them as resolved or rejected with ease.

Requirements
------------
- Python 3.10.11
- pip (Python package installer)

Installation
------------
1. Extract the EasyComplaints.zip folder to a location of your choice.
2. Open a terminal or command prompt and navigate to the extracted folder.
3. Install the required Python packages by running the following command:

   pip install -r requirements.txt

   This command will install all the necessary dependencies listed in the requirements.txt file, ensuring a smooth setup process.

Running the Application
-----------------------
1. After installing the required packages, navigate to the "EasyComplaints" folder inside the extracted folder using the following command:

   cd EasyComplaints

2. Run the following command to start the Django development server:

   python manage.py runserver

   This will start the development server and provide you with a URL (e.g., http://localhost:8000) where you can access the application.

3. Open a web browser and visit the provided URL to access the EasyComplaints.ai application.

Usage
-----
- Upon visiting the application, you will be prompted to register a new account or log in with an existing account.
- After successful authentication, users will be directed to their personalized dashboard, where they can view their registered complaints and their corresponding statuses.
- To lodge a new complaint, click on the "Lodge a New Complaint" option and follow the intuitive prompts to submit your complaint in text, voice, or image format.
- Staff members can access the dedicated staff dashboard by logging in with their staff credentials. Here, they can view and process complaints categorized by department, ensuring efficient management and resolution.

Note
----
- Ensure that you have Python 3.10.11 installed on your system before proceeding with the installation. Using a different version of Python may result in compatibility issues.
- If you encounter any issues during the installation or running the application, please refer to the project documentation or seek assistance from the project maintainers.

Contributing
------------
Contributions to the EasyComplaints.ai project are highly appreciated and welcomed. If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please open an issue or submit a pull request on the project's repository.

When contributing, please follow the established coding conventions and guidelines outlined in the project's documentation to ensure consistency and maintainability.
