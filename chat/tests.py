import time

from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cls.driver = webdriver.Chrome()
        except Exception:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + "/chat/")
        self.driver.find_element(
            By.ID, "room-name-input"
        ).send_keys(room_name + Keys.ENTER)

    def _send_message(self, message):
        self.driver.find_element(
            By.ID, "chat-message-input"
        ).send_keys(message + Keys.ENTER)

    def _get_chat_log(self):
        return self.driver.find_element(By.ID, "chat-log").get_attribute("value")

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room("room1")

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self._enter_chat_room("room1")

            self._send_message("hello")
            time.sleep(1)
            self.assertIn("hello", self._get_chat_log())

            self.driver.switch_to.window(self.driver.window_handles[0])
            self.assertIn("hello", self._get_chat_log())
        finally:
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room("room1")

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self._enter_chat_room("room2")

            self._send_message("hello")
            time.sleep(1)
            self.assertIn("hello", self._get_chat_log())

            self.driver.switch_to.window(self.driver.window_handles[0])
            self.assertNotIn("hello", self._get_chat_log())
        finally:
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])