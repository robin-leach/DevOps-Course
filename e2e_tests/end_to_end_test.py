from trello_requests.boards import create_board, delete_board
from app import create_app
import os
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
from dotenv import find_dotenv, load_dotenv
import logging

log = logging.getLogger('app')


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv()
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    board_id = create_board('test-name')
    os.environ['TRELLO_BOARD_ID'] = board_id

    # construct the new application
    application = create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    delete_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    new_item_title_input = driver.find_element_by_name("title")
    new_item_title_input.send_keys("New element")
    new_item_title_input.send_keys(Keys.RETURN)

    to_do_item = driver.find_element_by_id("to-do-item-New element")
    assert to_do_item.text == "New element"

    mark_done_button = driver.find_element_by_id("mark-done-New element")
    mark_done_button.click()
    
    done_item = driver.find_element_by_id("done-item-New element")
    assert done_item.text == "New element"
