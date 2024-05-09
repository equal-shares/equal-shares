import json
import logging
import os
import sys

sys.path.append("..")
import time
from datetime import datetime
from threading import Thread

from algorithms import (
    calculate_totals,
    convert_structure,
    generalized_median_algorithm,
    median_algorithm,
    unite_votes,
    update_dict_ids,
)
from calculator import Calculator
from counter import Counter
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from user import User
from utilities_component import UtilitiesComponent
from waitress import serve

from server.database.data_handler import data_handler
from server.database.sql_database import SQL_database

sys.path.append("..")

LOGֹ_FORMAT = "%(levelname)s, time: %(asctime)s , line: %(lineno)d- %(message)s "
# Create and configure logger
logging.basicConfig(filename="server_logging.log", level=logging.INFO, filemode="w")
logger = logging.getLogger()

app = Flask(__name__)
CORS(app)

# Initialize modules and variables
load_dotenv(find_dotenv(".env"))
port = os.environ.get("PORT", 5002)
mode = os.environ.get("MODE", "DEV")

# DB
database = data_handler(SQL_database(SQL_database.create_config()))
batch_database = data_handler(SQL_database(SQL_database.create_config()))

# Logic side
component = UtilitiesComponent()

# Batch calculate results
algorithms_results = None
converted_current_budget = None

# Current budget
current_budget_voting_page = None
current_budget_login_page = None

# Last vote
last_calculate_results_time = datetime.now()
last_voting_change = datetime.now()

def calculate_results():
    global last_calculate_results_time
    global algorithms_results
    logger.info("calculate_results")

    while True:
        # Check if there is a new votes
        if last_calculate_results_time < last_voting_change:
            logger.info("New vote received")
            batch_database.handler.connect()
            votes = batch_database.handler.load_user_votes()

            if not isinstance(votes, list):
                logger.error("Failed to load votes from the database")
                return jsonify({"status": "Failed to load votes from the database"})

            logger.info("Loaded user votes successfully from the database")
            voted_dict = unite_votes(votes)

            # Algo 1:
            median_algorithm_result: dict = median_algorithm(voted_dict)
            logger.info("Got the median algorithm result")

            # Algo 2:
            generalized_median_result: dict = generalized_median_algorithm(voted_dict)
            logger.info("Got the generalized median algorithm result")

            # Get current budget
            global converted_current_budget
            if converted_current_budget == None:
                tree = batch_database.handler.build_tree_from_current_budget()
                current_budget = tree.to_dict()
                # updates the 'total' values in the budget dictionary
                calculate_totals(current_budget)
                count = Counter()
                update_dict_ids(count, current_budget)
                converted_current_budget = convert_structure(current_budget)

            last_calculate_results_time = datetime.now()
            logger.info("Updated the results time")
            algorithms_results = {
                "median_algorithm": json.dumps(
                    median_algorithm_result, ensure_ascii=False
                ),
                "generalized_median_algorithm": json.dumps(
                    generalized_median_result, ensure_ascii=False
                ),
                "current_budget": json.dumps(
                    converted_current_budget, ensure_ascii=False
                ),
                "time": last_calculate_results_time,
            }

            logger.info("Calculations and results updated")

        time.sleep(100)


def start_background_thread():
    global batch_thread
    batch_thread = Thread(target=calculate_results)
    batch_thread.daemon = True
    batch_thread.start()


# Routes
#  -------------------------------- Login -----------------------------------------------------


@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Hello from people's Budget server!"})


@app.route("/peoples_budget/server/login", methods=["POST"])
def login():
    try:
        id = request.json["id"]
        password = request.json["password"]

    except:
        logger.error("ERROR! : login args")
        return jsonify({"status": "Faild"})

    # Guest user
    if component.is_guest_user(id):
        return jsonify({"status": "Succeeded"})

    result = component.check_if_user_exists(id, password)

    if result:
        return jsonify({"status": "Succeeded"})

    return jsonify({"status": "Faild"})


@app.route("/peoples_budget/server/login", methods=["GET"])
def table_tree():
    global current_budget_login_page

    if current_budget_login_page == None:
        current_budget_login_page = component.build_current_budget()

    return jsonify(current_budget_login_page)


# ------------------------------ Sign up -------------------------------------


@app.route("/peoples_budget/server/sign_up", methods=["POST"])
def signup():
    try:
        first_name = request.json["firstName"]
        last_name = request.json["lastName"]
        id = request.json["id"]
        birth_date = request.json["birthDate"]
        gender = request.json["gender"]
        email = request.json["email"]
        password = request.json["password"]

    except:
        logger.error("ERROR! : sign_up args")
        return jsonify("ERROR! : sign_up args")

    database.handler.connect()

    new_user: User = component.create_user(
        id, first_name, last_name, birth_date, email, password, gender, False
    )

    if new_user == None:
        return jsonify({"status": "Faild"})

    check_mail = component.is_mail_exists(new_user.get_mail())

    if check_mail:
        return jsonify(
            {"status": "The email already exists in the system - try another email"}
        )

    check_id = database.handler.user_id_exeisting(new_user)
    if check_id:
        return jsonify({"status": "The ID already exists in the system"})

    insert_result = database.handler.insert_new_user(new_user)
    if insert_result:
        return jsonify({"status": "Succeeded"})

    return jsonify({"status": "Faild"})


# --------------------------------- Forget Password ----------------------------------


@app.route("/peoples_budget/server/forget_password", methods=["POST"])
def forget_password():
    try:
        request_data = request.get_json()

    except:
        logger.error("ERROR! : in forget_password args")
        return jsonify({"status": "Faild"})

    if (
        "firstName" in request_data
        and "lastName" in request_data
        and "birthDate" in request_data
        and "id" in request_data
    ):
        first_name = request_data["firstName"]
        last_name = request_data["lastName"]
        id = request_data["id"]
        birth_date = request_data["birthDate"]

        database.handler.connect()

        user_details = database.handler.get_user_details(id)

        if type(user_details) != tuple:
            return jsonify({"status": "Faild"})

        # -- Verify user details --
        first_name_db = user_details[1]
        last_name_db = user_details[2]
        birth_date_db = str(user_details[3])

        if first_name != first_name_db:
            return jsonify("Invalid first name")

        if last_name != last_name_db:
            return jsonify("Invalid last name")

        if birth_date != birth_date_db:
            return jsonify("Invalid birth date")

        return jsonify({"status": "Succeeded"})

    #  -- Reset password --
    elif "newPassword" in request_data:
        user_id = request_data["id"]
        new_password = request_data["newPassword"]

        is_saved = database.handler.save_new_password(user_id, new_password)

        if is_saved:
            return jsonify({"status": "Succeeded"})

        # if not saved successfully
        return jsonify({"status": "Faild"})

    else:
        # The request does not contain the appropriate details
        return "Invalid request"


@app.route("/peoples_budget/server/forget_password", methods=["POST"])
def newpassword():
    try:
        new_password = request.json["newPassword"]

    except:
        logger.error("ERROR! : New password args")
        return jsonify({"status": "Faild"})

    # database.handler.connect()

    return jsonify({"status": "Succeeded"})


# --------------------------------- Home ---------------------------------------------


@app.route("/peoples_budget/server/home", methods=["GET"])
def home():
    try:
        id = request.args.get("user_id")
    except:
        return jsonify({"status": "Error!, id args"})

    try:
        database.handler.connect()

    except:
        return jsonify({"status": "Error!, can not connect to db"})

    full_name = database.handler.get_user_full_name(id)
    first_name = full_name[0]

    if first_name == "Faild":
        return jsonify({"status": f"There is no user in db with id: {id}"})

    if first_name == "Error!":
        return jsonify({"status": "Error!, Faild to execute get full name query"})

    last_name = full_name[1]

    user_gender = database.handler.get_user_gender(user_id=id)

    if user_gender == "Error!":
        return jsonify({"status": "Error!, Faild to execute get user gender query"})

    if user_gender == "Faild":
        return jsonify({"status": f"There is no user in db with id: {id}"})

    if user_gender == "1":
        user_gender = "Male"

    if user_gender == "2":
        user_gender = "Female"

    return {"first_name": first_name, "last_name": last_name, "gender": user_gender}


# -------------------------------- Information ---------------------------------------


@app.route("/peoples_budget/server/information", methods=["GET"])
def information():
    database.handler.connect()
    dictionary = database.handler.get_information()

    if dictionary.get("e") == "Error!":
        return jsonify({"status": "Faild"})

    json_information = json.dumps(dictionary, ensure_ascii=False)

    return jsonify(json_information)


# ---------------------------------- Dashborad --------------------------------------------


@app.route("/peoples_budget/server/dashboard", methods=["GET"])
def dashboard():
    database.handler.connect()

    voter_count = Calculator.get_voter_count(database.handler)
    ages = Calculator.get_voter_count_by_age(database.handler)
    genders = Calculator.get_voter_count_by_gender(database.handler)

    return jsonify({"voter_count": voter_count, "ages": ages, "genders": genders})


# ------------------------------------ Voting -------------------------------------------


@app.route("/peoples_budget/server/voting", methods=["GET"])
def subjects_and_projects_tree():
    database.handler.connect()
    try:
        user_id = request.args.get("user_id")
    except:
        return jsonify({"status": "Did not receive a user id"})

    # Guest user
    if user_id != "000000000":
        # Check if user already voted
        check_result = database.handler.check_voting_option(user_id=user_id)

        if check_result == "false":
            user_vote = database.handler.get_user_vote(user_id)

            if user_vote == "ERROR!":
                return jsonify({"status": "Faild to get old user_vote"})

            return user_vote

        elif check_result == "Error!":
            return jsonify({"status": "Error!, check_voting_option execute query"})

    global current_budget_voting_page
    if current_budget_voting_page == None:
        tree = database.handler.build_tree_from_current_budget()

        dictionary = tree.to_dict()
        # updates the 'total' values in the budget dictionary
        calculate_totals(dictionary)

        count = Counter()
        update_dict_ids(count, dictionary)
        current_budget_voting_page = json.dumps(dictionary, ensure_ascii=False)
    return current_budget_voting_page


@app.route("/peoples_budget/server/voting", methods=["POST"])
def voting_tree():
    try:
        database.handler.connect()
        data = request.json
        user_id = data["id"]
        vote = data["table"]
    except:
        return jsonify({"status": "failed"})

    # Guest user
    if user_id == "000000000":
        return jsonify({"status": "Succeeded"})

    vote_str = json.dumps(vote, ensure_ascii=False).replace("'", "''")

    # Check if user already voted
    check_result = database.handler.check_voting_option(user_id=user_id)

    global last_voting_change

    if check_result == "false":
        result = database.handler.update_user_vote(user_id=user_id, vote=vote_str)
        if not result:
            return jsonify({"status": "Error!, voting does not saved"})

        else:
            last_voting_change = datetime.now()
            return jsonify({"status": "Succeeded"})

    elif check_result == "Error!":
        return jsonify(
            {"status": "Error!, check_voting_option function faild to execute query"}
        )

    # update user option voting
    update_result = database.handler.update_voting_option(
        user_id=user_id, is_allowed=False
    )

    if not update_result:
        return jsonify(
            {"status": "Error!, Voting permission has not been updated, vote not saved"}
        )

    result = database.handler.store_vote(vote=str(vote_str), user_id=user_id)

    if not result:
        # update user option voting
        update_result = database.handler.update_voting_option(
            user_id=user_id, is_allowed=True
        )
        return jsonify({"status": "Error!, voting does not saved"})

    last_voting_change = datetime.now()
    return jsonify({"status": "Succeeded"})


# --------------------------------- Results -------------------------------------------


@app.route("/peoples_budget/server/results", methods=["GET"])
def get_algorithms_results():
    # global algorithms_results
    return jsonify(algorithms_results)

start_background_thread() # Start the background thread

if __name__ == "__main__":
    print(f"Server started on port: {port}")
    logger.info(f"Server started on port: {port} | mode: {mode}")

    if mode == "DEV":
        app.run(port=port, debug=True)
    else:
        serve(app, host="0.0.0.0", port=port)