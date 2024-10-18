import json
import os


class GestureParser:
    def __init__(self):
        """
            Initialize the GestureParser instance.
        """
        super().__init__()

    @staticmethod
    def gesture_json_to_file(gestures, filename):
        """
        Append the new detected gestures to the JSON file.
        """
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = {"gestures": []}

            data["gestures"].extend(gestures.values())

            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        except Exception as e:
            print(f"Error appending gestures to file: {e}")

    @staticmethod
    def read_gesture_from_json(filename):
        """
        Read the last gesture from the JSON file.
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as json_file:
                    data = json.load(json_file)
                    if "gestures" in data and len(data["gestures"]) > 0:
                        return data["gestures"][-1]
                    else:
                        return None
            except Exception as e:
                print(f"Error reading gestures from JSON: {e}")
                return None
        else:
            print(f"File {filename} not found.")
            return None
