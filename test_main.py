import unittest
from unittest.mock import MagicMock, patch
from bot_file import callback_message  # імпортуй функцію звідки вона у тебе

class TestTelegramBotCallback(unittest.TestCase):

    @patch('bot_file.user_print')
    @patch('bot_file.bot.send_message')
    @patch('bot_file.bot.send_photo')
    def test_show_examples_callback(self, mock_send_photo, mock_send_message, mock_user_print):
        # Мокаємо callback з даними
        mock_callback = MagicMock()
        mock_callback.data = 'show_examples'
        mock_callback.message.chat.id = 123456
        mock_callback.message.text = ""

        # Виклик функції
        callback_message(mock_callback)

        # Перевіряємо, що фото і повідомлення відправлені
        self.assertEqual(mock_send_photo.call_count, 3)
        self.assertEqual(mock_send_message.call_count, 3)
        mock_user_print.assert_called_once()

    @patch('bot_file.folderName')
    def test_instax_callback(self, mock_folder_name):
        mock_callback = MagicMock()
        mock_callback.data = 'instax'
        mock_callback.message.text = ''
        
        callback_message(mock_callback)

        self.assertEqual(mock_callback.message.text, '/instax')
        mock_folder_name.assert_called_once_with(mock_callback.message)

    @patch('bot_file.folderName')
    def test_fullPhoto_callback(self, mock_folder_name):
        mock_callback = MagicMock()
        mock_callback.data = 'fullPhoto'
        mock_callback.message.text = ''
        
        callback_message(mock_callback)

        self.assertEqual(mock_callback.message.text, '/fullPhoto')
        mock_folder_name.assert_called_once_with(mock_callback.message)

    @patch('bot_file.folderName')
    def test_3to5_callback(self, mock_folder_name):
        mock_callback = MagicMock()
        mock_callback.data = '3to5'
        mock_callback.message.text = ''
        
        callback_message(mock_callback)

        self.assertEqual(mock_callback.message.text, '/photo3to5')
        mock_folder_name.assert_called_once_with(mock_callback.message)

if __name__ == '__main__':
    unittest.main()
