import unittest
from unittest.mock import MagicMock, patch
from aiogram import types
from bot_telegram import echo_send

#Для работы с тестами, необходимо задать токен напрямую, чтобы это выглядело так: bot = Bot(token='ваш токен')
class TestEchoSend(unittest.TestCase):

    def setUp(self):
        self.msg = MagicMock(spec=types.Message)

    @patch('bot_telegram.load_regex_patterns')
    @patch('bot_telegram.bot.send_message')
    async def test_echo_send_no_match(self, mock_send_message, mock_load_regex_patterns):
        mock_load_regex_patterns.return_value = ['pattern1', 'pattern2']
        self.msg.text = "Some random text"
        await echo_send(self.msg)
        mock_send_message.assert_not_called()
        self.msg.delete.assert_not_called()

    @patch('bot_telegram.load_regex_patterns')
    @patch('bot_telegram.bot.send_message')
    async def test_echo_send_with_match(self, mock_send_message, mock_load_regex_patterns):
        mock_load_regex_patterns.return_value = ['pattern1', 'pattern2']
        self.msg.text = "Text with pattern2"
        await echo_send(self.msg)
        mock_send_message.assert_called_once()
        self.msg.delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()