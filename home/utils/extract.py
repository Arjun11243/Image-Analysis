import re

mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]

def verify_validate(aadharNum):
    


    aadharNum=aadharNum.replace(" ","")
    try:
        i = len(aadharNum)
        j = 0
        x = 0

        while i > 0:
            i -= 1
            x = mult[x][perm[(j % 8)][int(aadharNum[i])]]
            j += 1
        if x == 0:
            return True
        else:
            return False

    except ValueError:
        return False
    except IndexError:
        return False


def read_entities_file(file_path):
    """
    Reads the entities.txt file and returns a dictionary with the fields.
    """
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into label and value
            parts = line.strip().split(':', 1)
            if len(parts) == 2:
                label = parts[0].strip()
                value = parts[1].strip()
                
                # Map the label to a standard key name
                if label == "AadhaarNumber":
                    data['Adhaar Number'] = value
                elif label == "Name":
                    data['Name'] = value
                elif label == "DOB":
                    data['Date of Birth'] = value
                elif label == "Gender":
                    data['Sex'] = value
                elif label == "ID Type":
                    data['ID Type'] = value
    return data

def process_aadhaar_number(entities_data, aadhar_number):
    """
    Validates the Aadhaar number and returns the entities data if valid.
    """
    if not verify_validate(aadhar_number):
        print("Invalid Aadhaar Number")
        return None
    return entities_data

# Example usage
# file_path = 'entities.txt'

# Read the entities file and extract the Aadhaar number
# entities_data = read_entities_file(file_path)
# aadhar_number = entities_data.get('Adhaar Number', '')

# # Validate the Aadhaar number
# validated_data = process_aadhaar_number(entities_data, aadhar_number)

# if validated_data:
#     print(validated_data)
# else:
#     print("No data returned due to invalid Aadhaar number.")
