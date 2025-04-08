import sys
import os
import unittest
from unittest.mock import patch

# Add the src directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.text_processor import read_file, process_text, write_results, is_interactive

class TestTextProcessor(unittest.TestCase):
    def test_process_text(self):
        text = "Hello, world!"
        results = process_text(text)
        self.assertEqual(results["original_text"], "Hello, world!")
        self.assertEqual(results["word_count"], 2)
        self.assertEqual(results["uppercase_text"], "HELLO, WORLD!")
        
    def test_read_write_files(self):
        # Create a temporary test file
        test_input = "test input text"
        with open("test_input.txt", "w") as f:
            f.write(test_input)
        
        # Read the file
        text = read_file("test_input.txt")
        self.assertEqual(text, test_input)
        
        # Process and write results
        results = process_text(text)
        success = write_results(results, "test_output.txt")
        self.assertTrue(success)
        
        # Clean up
        os.remove("test_input.txt")
        os.remove("test_output.txt")
    
    @patch('sys.stdin')
    def test_is_interactive_terminal_mock(self, mock_stdin):
        """Test is_interactive() returns True with mocked terminal."""
        mock_stdin.isatty.return_value = True
        self.assertTrue(is_interactive())

    @patch('sys.stdin')
    def test_is_interactive_non_terminal_mock(self, mock_stdin):
        """Test is_interactive() returns False with mocked non-terminal."""
        mock_stdin.isatty.return_value = False
        self.assertFalse(is_interactive())

    @unittest.skipIf(os.environ.get("CI") or not sys.stdin.isatty(), 
        "Skipping: Not running in an interactive terminal environment (e.g., CI or non-terminal)")
    def test_is_interactive_real_docker_interactive(self):
        """Test is_interactive() returns True in a real interactive environment (e.g., docker run -it), not mocked."""
        self.assertTrue(is_interactive())

if __name__ == "__main__":
    unittest.main()
